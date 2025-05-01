import { ModeToggle } from './mode-toggle';
import { Button } from './ui/button';
import { useNavigate } from 'react-router-dom';

export default function Header(isLoggedIn: boolean) {
    return (
        <div className="header grid grid-cols-3 gap-4 h-auto">
            <div className="title col-span-1 col-start-2 flex justify-center bg-card">
                <p>QuizGen</p>
            </div>
            <div className="theme col-start-3 flex justify-end gap-2">
                {/* Conditionally render LoginButton */}
                {!isLoggedIn && <LoginButton />}
                <ModeToggle />
            </div>
        </div>
    );
}

function LoginButton() {
    const navigate = useNavigate();
    return (
        <Button variant={'outline'} onClick={() => navigate('/auth')}>
            Sign In
        </Button>
    )
}