const API_URL = "http://localhost:5000/";
const headers = {
    "Content-Type": "application/json",
}
export const fetchQuiz = async (topic: string, qtype: string, numq: number) => {
    try {
        const response = await fetch(API_URL + "generate-quiz", {
            method: "POST",
            headers,
            body: JSON.stringify({ topic, qtype, numq }),
        });

        if (!response.ok) {
            throw new Error("Failed to fetch quiz");
        }

        const data = await response.json();
        return data.quiz;
    } catch (error) {
        console.error("Error fetching quiz:", error);
        throw error; // Rethrow the error to handle it in the calling function
    }
};

export const checkAnswer = async (qid: string, qtype: string) => {
    var result = {correctAnswer: ''};
    try {
        const response = await fetch(API_URL + "check-answer", {
            method: "POST",
            headers,
            body: JSON.stringify({ qid, qtype }),
        });

        if (!response.ok) {
            throw new Error("Bad response from server: " + response.statusText);
        }

        const data = await response.json();
        result = data.correct_answer;
    } catch (error) {
        throw error;
    } finally {
        return result;
    }
}
