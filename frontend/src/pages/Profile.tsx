import { useEffect, useState } from 'react';
import { fetchUser, UserData } from '@/lib/api';

export default function Profile() {
    const [userData, setUserData] = useState<UserData | null>(null);

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
                <button className="bg-blue-500 text-white px-4 py-2 rounded">
                    View Recent Questions
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