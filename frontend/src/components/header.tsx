import { ModeToggle } from './mode-toggle';
import { Button } from './ui/button';
import { NavigateFunction, useNavigate } from 'react-router-dom';
import { signOut } from "supertokens-auth-react/recipe/session";

interface HeaderProps {
    isLoggedIn: boolean;
}

export default function Header({isLoggedIn}: HeaderProps) {
    const navigate = useNavigate();
    return (
        <div className="header grid grid-cols-3 gap-4 h-auto">
            <div className="title col-span-1 col-start-2 flex justify-center bg-card">
                <p>QuizGen</p>
            </div>
            <div className="theme col-start-3 flex justify-end gap-2">
                {/* Conditionally render LoginButton */}
                {!isLoggedIn && <LoginButton navigate={navigate}/>}
                {/* Conditionally render profile button */}
                {isLoggedIn && <ProfileButton navigate={navigate} />}
                {/* Conditionally render logout button */}
                {isLoggedIn && <LogoutButton />}
                <ModeToggle />
            </div>
        </div>
    );
}

function LoginButton({ navigate } : {navigate: NavigateFunction}) {
    return (
        <Button variant={'outline'} onClick={() => navigate('/auth')}>
            Sign In
        </Button>
    )
}

function ProfileButton({ navigate } : {navigate: NavigateFunction}) {
    return (
        <Button variant={'outline'} onClick={() => navigate('/profile')}>
            Profile
        </Button>
    )
}

function LogoutButton() {
    return (
        <Button variant={'outline'} onClick={async () => {
            await signOut();
            window.location.href = '/auth'; // Redirect to the login page after signing out forced refresh of state
        }}>
            Logout
        </Button>
    )
}
