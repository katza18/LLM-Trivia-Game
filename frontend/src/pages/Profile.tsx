import { useEffect, useState } from 'react';
import { fetchUser, UserData, fetchRecentQuestions } from '@/lib/api';
import QuestionCarousel from '@/components/questionCarousel';

export default function Profile() {
    const [userData, setUserData] = useState<UserData | null>(null);
    const [recentQuestions, setRecentQuestions] = useState<any[]>([]); // Adjust type as needed
    const numQuestions = 10; // Number of recent questions to fetch

    useEffect(() => {
        const loadUserData = async () => {
            try {
                const data = await fetchUser();
                setUserData(data);
                console.log("User data:", data);
            } catch (error) {
                console.error("Error fetching user: ", error);
                setUserData(null); // Set to null to indicate an error state
            }

            // Get user 10 most recent questions
            try {
                const questions = await fetchRecentQuestions(numQuestions);
                setRecentQuestions(questions);
                console.log("Recent questions:", questions);
            } catch (error) {
                console.error("Error fetching recent questions: ", error);
            }
        }

        loadUserData();
    }, []);

    if (userData === null) {
        // Show a loading state or an error message while fetching user data
        return (
            <div className="flex flex-col flex-grow items-center justify-center">
                <p>Failed to fetch user data. Please try again later.</p>
            </div>
        );
    }

    return(
        <div className="flex flex-col flex-grow items-center justify-center">
            {/* Add a carousel component for lists, favs, recents. When a user 
            has used their tokens, display a prompt to buy (or request) more. 
            Add payments after MVP release */}
            <p className="text-2xl font-bold">{userData.userName}</p>
            <div>
                <p className="text-lg">Tokens Used: {userData.tokensUsed}</p>
                <p className="text-lg">Tokens Remaining: {userData.tokensRemaining}</p>
            </div>
            <div className="mt-4">
                <h2 className="text-xl font-semibold">Recent Questions</h2>
                {recentQuestions ? 
                    <QuestionCarousel questions={recentQuestions} /> : null}
                <button className="bg-blue-500 text-white px-4 py-2 rounded">
                    View All Recent Questions
                </button>
                <button className="bg-green-500 text-white px-4 py-2 rounded ml-2">
                    View Favorites
                </button>
                <button className="bg-yellow-500 text-white px-4 py-2 rounded ml-2">
                    View Lists
                </button>
            </div>
        </div>
    );
}