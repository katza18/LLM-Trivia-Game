import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

function Quiz() {
    const location = useLocation();
    const { topic, qtype } = location.state as any || {};
    const [quiz, setQuiz] = useState<any>([]);
    const [loading, setLoading] = useState(true);
    const [currentQuestionIdx, setCurrentQuestionIdx] = useState(0);
    const [answered, setAnswered] = useState(false);
    const [correct, setCorrect] = useState(false);
    const [correctAnswer, setCorrectAnswer] = useState('');
    const [selectedAnswer, setSelectedAnswer] = useState('');
    const [score, setScore] = useState(0);

    const fetchQuiz = async () => {
        try {
            const response = await fetch("http://localhost:5000/generate-quiz", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ topic, qtype, numq: 10 }),
            });

            if (!response.ok) {
                throw new Error("Failed to fetch quiz");
            }

            const data = await response.json();

            setQuiz(data.results);
            setLoading(false);
        } catch (error) {
            console.log(error);
            setLoading(false);
        }
    };

    const handleMultipleChoiceAnswer = async (answer: string) => {
        // Check if answer is correct, send to backend to avoid storing answers in frontend
        var result = {correctAnswer: ''};
        try {
            const response = await fetch("http://localhost:5000/check-answer", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ questionId: quiz[currentQuestionIdx].questionId, answer }),
            });

            if (!response.ok) {
                throw new Error("Failed to check answer");
            }

            const data = await response.json();
            result = data.result;
        } catch (error) {
            console.log(error);
            return;
        }

        // Update the selected answer
        setSelectedAnswer(answer);

        // Update correct answer
        setCorrectAnswer(result.correctAnswer);

        // Update correct and score
        if( answer === result.correctAnswer ) {
            setCorrect(true);
            setScore(score + 1);
        }

        // Update answered
        setAnswered(true);
    };

    useEffect(() => {
        fetchQuiz();
    }, []);

    if (loading) {
        return (
            <div className="flex flex-col flex-grow items-center justify-center">
                <p>Loading...</p>
            </div>
        );
    }

    if (quiz.length === 0) {
        return (
            <div className="flex flex-col flex-grow items-center justify-center">
                <p>Failed to fetch quiz. Please try again later.</p>
            </div>
        );
    }

    // If we have answered all questions, show the score
    if (currentQuestionIdx >= quiz.length) {
        return (
            <div className="flex flex-col flex-grow items-center justify-center">
                <p>Quiz complete! Your score is {score}/{quiz.length}</p>
            </div>
        );
    }

    const currentQuestion = quiz[currentQuestionIdx];

    return (
        <div className="quiz flex flex-col flex-grow">
            <div hidden className="timer flex items-center justify-center flex-grow">
                <p>Time left: 15 seconds</p>
            </div>
            <div className="body grid grid-cols-3 gap-4 h-auto flex-grow">
                <div className="quiz col-start-2 flex flex-col justify-center bg-card gap-2">
                <h2 className="text-center">--- Question #{currentQuestionIdx + 1} ---</h2>
                <p className='text-center'>{currentQuestion.question}</p>
                {/* Conditionally render multiple choice or short answer */}
                { currentQuestion.qtype === 'm' ? (
                    currentQuestion.answers.map((answer: string, idx: number) => (
                        <Button
                            variant='outline'
                            key={idx}
                            onClick={() => handleMultipleChoiceAnswer(answer)}
                            className={
                                !answered ? '' :
                                answer === correctAnswer ? 'bg-green-500' :
                                answer === selectedAnswer ? 'bg-red-500' : ''
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
                {answered ? (
                    correct ? (
                        <p>Correct!</p>
                    ) : (
                        <p>Incorrect! The correct answer was: {correctAnswer}</p>
                    )
                ) : null }
                {answered ? (
                    <Button variant='default' onClick={() => {setCurrentQuestionIdx(currentQuestionIdx + 1)}}>Next Question</Button>
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
