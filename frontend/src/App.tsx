import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from './components/theme-provider';
import { ModeToggle } from './components/mode-toggle';
import Quiz from './pages/Quiz';
import Home from './pages/Home';

function App() {
  return (
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
            <Route path="/" element={<Home />} />
            <Route path="/quiz" element={<Quiz />} />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  )
}

export default App
