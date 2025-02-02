function NoteAnalyzer( { results, setShowResults } ) {

    const obj = JSON.parse(results);
    

    return (
        <>
        <div className="container-fluid d-flex flex-column justify-content-center align-items-center vh-100 bg-dark ">
            <div className="card shadow-lg p-4 mb-4 w-50">
                <div className="card-body text-center">
                    <h2 className="card-title mb-3">Summary of Notes</h2>
                    <textarea value={obj.summary || "No summary available."}
                    className="form-control border-0 shadow-sm p-3 text-center"
                    style={{ width: "100%", height: "200px", resize: "none", fontSize: "1rem"}
                    }>
                    </textarea>

                    {/* Questions Section
                    <h2 className="card-title mb-3 mt-4">Questions</h2>
                    {obj.questions_hints && obj.questions_hints.length > 0 ? (
                        obj.questions_hints.map((q, index) => (
                            <div key={index} className="mb-3">
                                <strong>Question {index + 1}:</strong>
                                <textarea 
                                    value={q.question} 
                                    className="form-control border-0 shadow-sm p-3 text-center"
                                    style={{ width: "100%", height: "100px", resize: "none", fontSize: "1rem"}}
                                    readOnly
                                />
                            </div>
                        ))
                    ) : (
                        <p className="text-light">No questions available.</p>
                    )} */}

                    {/* Next Topics Section */}
                    <h2 className="card-title mb-3 mt-4">Related Topics</h2>

                    {obj.next_topics && obj.next_topics.length > 0 ? (
                        <p className="text-dark">
                            {obj.next_topics.map((topic) => topic.topic).join(", ")}
                        </p>
                    ) : (
                        <p className="text-light">No topics available.</p>
                    )}
                </div>
            </div> 

            <button className="btn btn-primary" onClick={() => setShowResults(false)}>Back</button>  
            </div>             
        </>   
    )
}

export default NoteAnalyzer;