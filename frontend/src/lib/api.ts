const API_URL = "http://localhost:5000/";
const headers = {
    "Content-Type": "application/json",
}
export const fetchQuiz = async (topic: string, qtype: string, numq: number, isDemo: boolean) => {
    try {
        const route =  isDemo ? "generate-quiz-demo" : "generate-quiz";
        const response = await fetch(API_URL + route, {
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

// User data interface and API calls
export interface UserData {
    userName: string;
    tokensUsed: number;
    tokensRemaining: number;
}
export const fetchUser = async (): Promise<UserData> => {
    try {
        const response = await fetch(API_URL + "user", {
            method: "GET",
            headers,
        });

        if (!response.ok) {
            throw new Error("Failed to fetch user data");
        }

        const data = await response.json();
        return data.user;
    } catch (error: any) {
        console.error("Error fetching user:", error);
        throw error; // Rethrow the error to handle it in the calling function
    }
}

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
