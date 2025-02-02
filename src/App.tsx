import './index.css'
import { useState } from "react"
import MainPage from './MainPage'
import NoteAnalyzer from './NoteAnalyzer'

function App() {
  const [showResults, setShowResults] = useState(false);
  const [results, setResults] = useState("");

  return (
    <>
    <div>
      {!showResults ? (
          <MainPage setShowResults={setShowResults} setResults={setResults}/>
      ) : <NoteAnalyzer results={results} setShowResults={setShowResults}/>}


    </div>
    </>
    
  )
}

export default App