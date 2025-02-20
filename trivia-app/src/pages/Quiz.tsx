import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

function Quiz() {
    const location = useLocation();
    const { topic, qtype } = location.state as any || {};
    const [quiz, setQuiz] = useState<any>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchQuiz();
    }, []);

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

    return (
    <div className="quiz flex flex-col flex-grow">
        <div className="timer flex items-center justify-center flex-grow">
            <p>Time left: 15 seconds</p>
        </div>
        <div className="body grid grid-cols-3 gap-4 h-auto flex-grow">
            <div className="quiz col-start-2 flex flex-col justify-center bg-card gap-2">
            <h2 className="text-center">--- Question # ---</h2>
            <p className='text-center'>Question?</p>
            <Button variant='outline'>Answer 1</Button>
            <Button variant='outline'>Answer 2</Button>
            <Button variant='outline'>Answer 3</Button>
            <Button variant='outline'>Answer 4</Button>
            <Input className="hidden" type="text" placeholder="Enter your answer here" />
            <Button variant='default'>Submit Answer</Button>
            <p className="hidden">Correct!</p>
            <p className="hidden">Incorrect! The correct answer was: Answer 2</p>
            </div>
        </div>
        <div className="score flex justify-center items-center flex-grow ">
            <p>100%</p>
        </div>
        <div className="footer grid grid-cols-3 gap-4 h-auto">
            <div className="correction col-start-2 flex justify-center">
            <Button variant='outline'>Submit question correction</Button> {/* This should open a form to be filled out that submits a correction to the questions/answers */}
            </div>
        </div>
    </div>
    );
};

export default Quiz;
