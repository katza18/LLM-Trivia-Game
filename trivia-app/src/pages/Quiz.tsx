import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { fetchQuiz, checkAnswer } from '@/lib/api';

function Quiz() {
    const numberOfQuestions = 10; // Number of questions to fetch
    const location = useLocation();
    const { topic, qtype } = location.state as { topic: string; qtype: string };
    const [quiz, setQuiz] = useState<any>(null);
    const [currentQuestionIdx, setCurrentQuestionIdx] = useState(0);
    const [correctAnswer, setCorrectAnswer] = useState<string>('');
    const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
    const [score, setScore] = useState(0);
    const [reloadKey, setReloadKey] = useState(0); // State to trigger re-fetching of quiz data
    const isAnswered = selectedAnswer !== null;
    const isCorrect = selectedAnswer === correctAnswer;


    const updateAnswerState = (answer: string, correctAnswer: string) => {
        setSelectedAnswer(answer);
        setCorrectAnswer(correctAnswer);
        if (answer === correctAnswer) {
            setScore((prevScore) => prevScore + 1);
        }
    };


    const handleAnswer = async (answer: string) => {
        // Check if answer is correct, send to backend to avoid storing answers in frontend; backend uses qtype to determine what table to check against
        try {
            const result = await checkAnswer(answer, quiz[currentQuestionIdx].id, qtype);
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

    const regenerateQuiz = () => {
        setQuiz(null);
        setCurrentQuestionIdx(0);
        setScore(0);
        setSelectedAnswer(null);
        setCorrectAnswer('');
        setReloadKey((prevKey) => prevKey + 1); // Increment the reload key to trigger re-fetching of quiz data
    }

    useEffect(() => {
        const loadQuiz = async () => {
            try {
                const data = await fetchQuiz(topic, qtype, numberOfQuestions);
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
        <div className="quiz flex flex-col flex-grow">
            <div hidden className="timer flex items-center justify-center flex-grow">
                <p>Time left: 15 seconds</p>
            </div>
            <div className="body grid grid-cols-3 gap-4 h-auto flex-grow">
                <div className="quiz col-start-2 flex flex-col justify-center bg-card gap-2">
                <h2 className="text-center">--- Question #{currentQuestionIdx + 1} ---</h2>
                <p className='text-center'>{quiz[currentQuestionIdx].question}</p>
                {/* Conditionally render multiple choice or short answer */}
                { qtype === 'multi' ? (
                    quiz[currentQuestionIdx].choices.map((answer: string, idx: number) => (
                        <Button
                            variant='outline'
                            key={idx}
                            onClick={() => updateAnswerState(answer, quiz[currentQuestionIdx].answer)}
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
                        <Input 
                            type="text" 
                            placeholder="Enter your answer here" 
                            value={selectedAnswer || ''} 
                            onChange={(e) => setSelectedAnswer(e.target.value)} 
                        />
                        <Button 
                            variant='default' 
                            onClick={() => selectedAnswer && handleAnswer(selectedAnswer)}
                        >
                            Submit Answer
                        </Button>
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
