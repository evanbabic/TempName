import './index.css'
import { useState } from "react"
import MainPage from './MainPage'
import NoteAnalyzer from './NoteAnalyzer'
import Footer from './Footer'
import Background from './Background'

function App() {
  const [showResults, setShowResults] = useState(false);
  const [results, setResults] = useState("");
  const [loading, setLoading] = useState(false);

  return (
    <>
    <Background/>
      <div>
        { loading ? (
          <div className="d-flex justify-content-center align-items-center vh-100">
            <div className="spinner-border text-primary" role="status">
              <span className="text-dark">Loading...</span>
            </div>
          </div>
        ) : !showResults ? (
          <MainPage setShowResults={setShowResults} setResults={setResults} setLoading={setLoading} />
        ) : (
          <NoteAnalyzer results={results} setShowResults={setShowResults} />
        )}
      </div>
      <Footer />
    </>
  );
}

export default App