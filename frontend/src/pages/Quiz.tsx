import { Button } from '../components/ui/button';
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { fetchQuiz } from '@/lib/api';
import QuestionCard from '@/components/questionCard';

interface QuizProps {
    isDemo?: boolean;
}

function Quiz({isDemo = false}: QuizProps) {
    const numberOfQuestions = 10; // Number of questions to fetch
    const location = useLocation();
    const { topic, qtype } = location.state as { topic: string; qtype: string };
    const [quiz, setQuiz] = useState<any>(null);
    const [currentQuestionIdx, setCurrentQuestionIdx] = useState(0);
    const [score, setScore] = useState(0);
    const [reloadKey, setReloadKey] = useState(0); // State to trigger re-fetching of quiz data

    const regenerateQuiz = () => {
        setQuiz(null);
        setCurrentQuestionIdx(0);
        setScore(0);
        setReloadKey((prevKey) => prevKey + 1); // Increment the reload key to trigger re-fetching of quiz data
    }

    useEffect(() => {
        const loadQuiz = async () => {
            try {
                const data = await fetchQuiz(topic, qtype, numberOfQuestions, isDemo);
                setQuiz(data);
                console.log("Quiz data:", data);
            } catch (error) {
                console.error("Error fetching quiz:", error);
                setQuiz([]); // Set quiz to an empty array to trigger the error message
            }
        }

        loadQuiz();
    }, [topic, qtype, reloadKey]);

    // If the quiz is still loading, show a loading message
    if (!quiz || !quiz.length || currentQuestionIdx >= quiz.length) {
        var text = "";
        if (!quiz) {
            text = "Loading...";
        }
        else if (!quiz.length) {
            text = "Failed to fetch quiz. Please try again later.";
        } else {
            text = "Quiz complete! Your score is " + score + "/" + quiz.length;
            // Add a button here for the user to regenerate a quiz on the same topic or go back to the home page
        }
        return (
            <div className="flex flex-col flex-grow items-center justify-center">
                <p>{text}</p>
                {quiz && currentQuestionIdx >= quiz.length && (
                    <>
                    <Button variant='default' onClick={regenerateQuiz} className="mt-4">
                        Regenerate Quiz
                    </Button>
                    <Button variant='default' onClick={() => window.history.back()} className="mt-4">
                        Go Back to Home
                    </Button>
                    </>
                )}
            </div>
        );
    }


    return (
        <QuestionCard 
            questionNumber={currentQuestionIdx + 1}
            question={quiz[currentQuestionIdx].question}
            choices={quiz[currentQuestionIdx].choices}
            score={score}
            qtype={qtype}
            quizLength={quiz.length}
            questionId={quiz[currentQuestionIdx].id}
            setScore={setScore}
            setCurrentQuestionIdx={setCurrentQuestionIdx}
        />
    );
};

export default Quiz;
