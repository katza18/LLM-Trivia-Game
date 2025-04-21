import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { fetchQuiz, checkAnswer } from '@/lib/api';

function Quiz() {
    const location = useLocation();
    const { topic, qtype } = location.state as any || {};
    const [quiz, setQuiz] = useState<any>(null);
    const [currentQuestionIdx, setCurrentQuestionIdx] = useState(0);
    const [correctAnswer, setCorrectAnswer] = useState<string>('');
    const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
    const [score, setScore] = useState(0);
    const isAnswered = selectedAnswer !== null;
    const isCorrect = selectedAnswer === correctAnswer;


    const updateAnswerState = (answer: string, correctAnswer: string) => {
        setSelectedAnswer(answer);
        setCorrectAnswer(correctAnswer);
        if (answer === correctAnswer) {
            setScore((prevScore) => prevScore + 1);
        }
    };


    const handleMultipleChoiceAnswer = async (answer: string) => {
        // Check if answer is correct, send to backend to avoid storing answers in frontend
        try {
            const result = await checkAnswer(answer, quiz[currentQuestionIdx].id);
            updateAnswerState(answer, result.correctAnswer);
        } catch (error) {
            console.error("Error checking answer:", error);
        }
    };

    const handleNextQuestion = () => {
        setSelectedAnswer(null);
        setCurrentQuestionIdx((prevIdx) => prevIdx + 1);
        setCorrectAnswer('');
    };

    useEffect(() => {
        const loadQuiz = async () => {
            try {
                const data = await fetchQuiz(topic, qtype, 10);
                setQuiz(data);
            } catch (error) {
                console.error("Error fetching quiz:", error);
                setQuiz([]); // Set quiz to an empty array to trigger the error message
            }
        }

        loadQuiz();
    }, [topic, qtype]);


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
        }
        return (
            <div className="flex flex-col flex-grow items-center justify-center">
                <p>{text}</p>
            </div>
        );
    }


    return (
        <div className="quiz flex flex-col flex-grow">
            <div hidden className="timer flex items-center justify-center flex-grow">
                <p>Time left: 15 seconds</p>
            </div>
            <div className="body grid grid-cols-3 gap-4 h-auto flex-grow">
                <div className="quiz col-start-2 flex flex-col justify-center bg-card gap-2">
                <h2 className="text-center">--- Question #{currentQuestionIdx + 1} ---</h2>
                <p className='text-center'>{quiz[currentQuestionIdx].question}</p>
                {/* Conditionally render multiple choice or short answer */}
                { qtype === 'm' ? (
                    quiz[currentQuestionIdx].answers.map((answer: string, idx: number) => (
                        <Button
                            variant='outline'
                            key={idx}
                            onClick={() => handleMultipleChoiceAnswer(answer)}
                            className={
                                !isAnswered ? '' :
                                answer === correctAnswer ? 'bg-green-500 hover:bg-green-600' :
                                answer === selectedAnswer ? 'bg-red-500 hover:bg-red-600' : ''
                            }
                        >
                            {answer}
                        </Button>
                    ))
                ) : (
                    <>
                        <Input className="hidden" type="text" placeholder="Enter your answer here" />
                        <Button variant='default'>Submit Answer</Button>
                    </>
                )}
                {/* Conditionally render the correct/incorrect message and next question button */}
                {isAnswered ? (
                    isCorrect ? (
                        <p className="text-center">Correct!</p>
                    ) : (
                        <p className="text-center">Incorrect! The correct answer was: {correctAnswer}</p>
                    )
                ) : null }
                {isAnswered ? (
                    <Button variant='default' onClick={handleNextQuestion}>Next Question</Button>
                ) : null }
                </div>
            </div>
            <div className="score flex justify-center items-center flex-grow ">
                <p>{score}/{quiz.length}</p>
            </div>
            <div className="footer grid grid-cols-3 gap-4 h-auto">
                <div className="correction col-start-2 flex justify-center">
                <Button hidden variant='outline'>Submit question correction</Button> {/* This should open a form to be filled out that submits a correction to the questions/answers */}
                </div>
            </div>
        </div>
    );
};

export default Quiz;
