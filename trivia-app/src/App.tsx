import './App.css'
import { ModeToggle } from './components/mode-toggle';
import { ThemeProvider } from './components/theme-provider';
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";

function App() {
  return (
    <ThemeProvider defaultTheme='dark' storageKey='vite-ui-theme'>
    <div className="min-h-screen bg-background text-primary flex flex-col items-center justify-center">
      <div className="bg-card p-4 w-100 flex justify-end">
        <ModeToggle />
      </div>
      <div className="bg-card p-4 w-full flex flex-col items-center justify-center">
        <h1>Quiz Me!</h1>
      </div>
      <div className="App-body">
        <h2>--- Question Number will go here ---</h2>
        <p>Question will go here</p>
        <Button variant='outline'>Answer 1</Button>
        <Button variant='outline'>Answer 2</Button>
        <Button variant='outline'>Answer 3</Button>
        <Button variant='outline'>Answer 4</Button>
        <Input type="text" placeholder="Enter your answer here" />
        <Button variant='secondary'>Submit Answer</Button>
        <p>Time left: 15 seconds</p>
        <p>Correct!</p>
        <p>Incorrect! The correct answer was: Answer 2</p>
        <Button variant='secondary'>Submit question correction</Button> {/* This should open a form to be filled out that submits a correction to the questions/answers */}
      </div>
      {/* QA Style ask the user what they'd like to be quizzed on */}
      {/* <Chat /> */}
    </div>
    </ThemeProvider>
  )
}

export default App
