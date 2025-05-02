
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useState } from "react";
import { checkAnswer } from '@/lib/api';

interface QuestionCardProps {
    questionNumber: number;
    question: string;
    choices: string[];
    score: number;
    qtype: string;
    quizLength: number;
    questionId: string;
    setScore: React.Dispatch<React.SetStateAction<number>>;
    setCurrentQuestionIdx: React.Dispatch<React.SetStateAction<number>>;
}

// <Quiz correctAnswer={quiz[currentQuestionIdx].answer}, question={quiz[currentQuestionIdx].question}, choices={quiz[currentQuestionIdx].choices} quizLength={quiz.length} questionId={quiz[currentQuestionIdx].id}/>

export default function QuestionCard(props: QuestionCardProps) {
    const { questionNumber, question, choices, score, qtype, quizLength, questionId, setScore, setCurrentQuestionIdx } = props;
    const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
    const [correctAnswer, setCorrectAnswer] = useState<string>('');
    const isAnswered = selectedAnswer !== null;
    const isCorrect = selectedAnswer === correctAnswer;

    const handleAnswer = async (userAnswer: string) => {
        // Check if answer is correct, send to backend to avoid storing answers in frontend; backend uses qtype to determine what table to check against
        try {
            const result = await checkAnswer(questionId, qtype);
            setCorrectAnswer(result.correctAnswer);
            setSelectedAnswer(userAnswer);
            if (isCorrect) {
                setScore((prevScore) => prevScore + 1);
            }
        } catch (error) {
            console.error("Error checking answer:", error);
        }
    };

    const handleNextQuestion = () => {
        setSelectedAnswer(null);
        setCurrentQuestionIdx((prevIdx) => prevIdx + 1);
        setCorrectAnswer('');
    };

    return (
    <div className="quiz flex flex-col flex-grow">
        <div hidden className="timer flex items-center justify-center flex-grow">
            <p>Time left: 15 seconds</p>
        </div>
        <div className="body grid grid-cols-3 gap-4 h-auto flex-grow">
            <div className="quiz col-start-2 flex flex-col justify-center bg-card gap-2">
            <h2 className="text-center">--- Question #{questionNumber} ---</h2>
            <p className='text-center'>{question}</p>
            {/* Conditionally render multiple choice or short answer */}
            { qtype === 'multi' ? (
                choices.map((answer: string, idx: number) => (
                    <Button
                        variant='outline'
                        key={idx}
                        onClick={() => handleAnswer(answer)}
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
            <p>{score}/{quizLength}</p>
        </div>
        <div className="footer grid grid-cols-3 gap-4 h-auto">
            <div className="correction col-start-2 flex justify-center">
            <Button hidden variant='outline'>Submit question correction</Button> {/* This should open a form to be filled out that submits a correction to the questions/answers */}
            </div>
        </div>
    </div>
    );
}