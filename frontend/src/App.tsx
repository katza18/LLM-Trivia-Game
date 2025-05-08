import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from './components/theme-provider';
import Quiz from './pages/Quiz';
import Home from './pages/Home';
import * as reactRouterDom from 'react-router-dom';
import { getSuperTokensRoutesForReactRouterDom } from "supertokens-auth-react/ui";
import SuperTokens, { SuperTokensWrapper } from "supertokens-auth-react";
import EmailPassword from "supertokens-auth-react/recipe/emailpassword";
import Session from "supertokens-auth-react/recipe/session";
import { EmailPasswordPreBuiltUI } from "supertokens-auth-react/recipe/emailpassword/prebuiltui";
import { SessionAuth } from "supertokens-auth-react/recipe/session";
import { useEffect, useState } from 'react';
import Header from './components/header';

// Initialize SuperTokens
SuperTokens.init({
    appInfo: {
        appName: "QuizGen",
        apiDomain: "http://localhost:3000",
        websiteDomain: "http://localhost:5173",
        apiBasePath: "/auth",
        websiteBasePath: "/auth",
    },
    recipeList: [EmailPassword.init(), Session.init()],
});

function App() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    useEffect(() => {
        async function checkSession() {
            const sessionExists = await Session.doesSessionExist();
            setIsLoggedIn(sessionExists);
        }
        checkSession();
    }, []);

    return (
    <SuperTokensWrapper>
        <ThemeProvider defaultTheme='dark' storageKey='vite-ui-theme'>
            <Router>
                {/* MAIN CONTAINER */}
                <div className="min-h-screen bg-background text-primary flex flex-col p-4">
                    {/* HEADER */}
                    <Header isLoggedIn={isLoggedIn} />
                    {/* MAIN CONTENT */}
                    <Routes>
                        {/* Render login UI on /auth route */}
                        {getSuperTokensRoutesForReactRouterDom(reactRouterDom, [EmailPasswordPreBuiltUI])}
                        <Route path="/" element={<Home />} />
                        <Route path="/quiz" element={
                            <SessionAuth>
                                <Quiz />
                            </SessionAuth>
                        } />
                        <Route path="/demo" element={
                            <Quiz isDemo={true} />    
                        } />
                        <Route path="/profile" element={
                            <SessionAuth>
                                <div className="flex flex-col flex-grow items-center justify-center">
                                    <p>Hello.</p>
                                </div>
                            </SessionAuth>
                        } />
                    </Routes>
                </div>
            </Router>
        </ThemeProvider>
    </SuperTokensWrapper>
    );
}

export default App
