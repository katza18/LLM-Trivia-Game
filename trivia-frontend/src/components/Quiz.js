import React, { useState, useEffect } from 'react';
import './Quiz.css';

const Quiz = ({ question, options, correctAnswer, onAnswerSelected }) => {
    const [timeLeft, setTimeLeft] = useState(10);

    useEffect(() => {
        if (timeLeft > 0) {
            const timerId = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
            return () => clearTimeout(timerId);
        } else {
            onAnswerSelected(null);
        }
    }, [timeLeft, onAnswerSelected]);

    const handleAnswerClick = (answer) => {
        onAnswerSelected(answer);
    };

    return (
        <div className="quiz-container">
            <div className="question-card">
                <h2>{question}</h2>
            </div>
            <div className="progress-bar">
                <div className="progress" style={{ width: `${(timeLeft / 10) * 100}%` }}></div>
            </div>
            <div className="options-container">
                {options.map((option, index) => (
                    <div key={index} className="option-card" onClick={() => handleAnswerClick(option)}>
                        {option}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Quiz;
