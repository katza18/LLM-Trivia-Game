import './App.css'
import { ModeToggle } from './components/mode-toggle';
import { ThemeProvider } from './components/theme-provider';
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";

function App() {
  return (
    <ThemeProvider defaultTheme='dark' storageKey='vite-ui-theme'>
    <div className="min-h-screen bg-background text-primary flex flex-col p-4">
      <div className="header grid grid-cols-3 gap-4 h-auto">
        <div className="title col-span-1 col-start-2 flex justify-center bg-card">
          <p>Quiz Me!</p>
        </div>
        <div className="theme col-start-3 flex justify-end">
          <ModeToggle />
        </div>
      </div>
      <div className="timer flex items-center justify-center flex-grow">
        <p>Time left: 15 seconds</p>
      </div>
      <div className="body grid grid-cols-3 gap-4 h-auto flex-grow">
        <div className="quiz col-start-2 flex flex-col justify-center bg-card gap-2">
          <h2 className="text-center">--- Question # ---</h2>
          <p className='text-center'>Question?</p>
          <Button variant='outline'>Answer 1</Button>
          <Button variant='outline'>Answer 2</Button>
          <Button variant='outline'>Answer 3</Button>
          <Button variant='outline'>Answer 4</Button>
          <Input className="hidden" type="text" placeholder="Enter your answer here" />
          <Button variant='default'>Submit Answer</Button>
          <p className="hidden">Correct!</p>
          <p className="hidden">Incorrect! The correct answer was: Answer 2</p>
        </div>
      </div>
      <div className="score flex justify-center items-center flex-grow ">
        <p>100%</p>
      </div>
      <div className="footer grid grid-cols-3 gap-4 h-auto">
        <div className="correction col-start-2 flex justify-center">
          <Button variant='outline'>Submit question correction</Button> {/* This should open a form to be filled out that submits a correction to the questions/answers */}
        </div>
      </div>
    </div>
    </ThemeProvider>
  )
}

export default App
