import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from './components/theme-provider';
import { ModeToggle } from './components/mode-toggle';
import Quiz from './pages/Quiz';
import Home from './pages/Home';
import * as reactRouterDom from 'react-router-dom';
import { getSuperTokensRoutesForReactRouterDom } from "supertokens-auth-react/ui";
import SuperTokens, { SuperTokensWrapper } from "supertokens-auth-react";
import EmailPassword from "supertokens-auth-react/recipe/emailpassword";
import Session from "supertokens-auth-react/recipe/session";
import { EmailPasswordPreBuiltUI } from "supertokens-auth-react/recipe/emailpassword/prebuiltui";
import { SessionAuth } from "supertokens-auth-react/recipe/session";

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
  return (
    <SuperTokensWrapper>
        <ThemeProvider defaultTheme='dark' storageKey='vite-ui-theme'>
            <Router>
                {/* MAIN CONTAINER */}
                <div className="min-h-screen bg-background text-primary flex flex-col p-4">
                {/* HEADER */}
                <div className="header grid grid-cols-3 gap-4 h-auto">
                    <div className="title col-span-1 col-start-2 flex justify-center bg-card">
                        <p>QuizGen</p>
                    </div>
                    <div className="theme col-start-3 flex justify-end">
                        <ModeToggle />
                    </div>
                </div>
                {/* MAIN CONTENT */}
                <Routes>
                    {/* Render login UI on /auth route */}
                    {getSuperTokensRoutesForReactRouterDom(reactRouterDom, [EmailPasswordPreBuiltUI])}
                    <Route path="/" element={<Home />} />
                    <Route path="/quiz" element={<Quiz />} />
                </Routes>
                </div>
            </Router>
        </ThemeProvider>
    </SuperTokensWrapper>
  )
}

export default App
