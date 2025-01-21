import React, { useState, useEffect } from 'react';

const Chat = () => {
    const [message, setMessage] = useState('');
    const [displayedMessage, setDisplayedMessage] = useState('');
    const [userInput, setUserInput] = useState('');
    const fullMessage = 'What topic would you like to be quizzed on?';

    useEffect(() => {
        if (message) {
            let index = 0;
            const interval = setInterval(() => {
                setDisplayedMessage((prev) => prev + fullMessage[index]);
                index++;
                if (index === fullMessage.length) {
                    clearInterval(interval);
                }
            }, 100); // Adjust the speed of typing here
            return () => clearInterval(interval);
        }
    }, [message]);

    const handleButtonClick = () => {
        setMessage('What topic would you like to be quizzed on?');
        setDisplayedMessage('');
    };

    const handleInputChange = (event) => {
        setUserInput(event.target.value);
    };

    return (
        <div>
            <button onClick={handleButtonClick}>QUIZ ME!</button>
            <div>{displayedMessage}</div>
            <div>
                <input
                    type='text'
                    value={userInput}
                    onChange={handleInputChange}
                    placeholder='Enter a topic'
                />
            </div>
        </div>
    );
};

export default Chat;
