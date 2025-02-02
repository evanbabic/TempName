

function NoteAnalyzer( { results, setShowResults } ) {

    const obj = JSON.parse(results);
    
    return (
        <>
        <div className="container-fluid d-flex flex-column justify-content-center align-items-center vh-40 p-3 ">
            <div className="card shadow-lg p-4 mb-4 w-75">
                <div className="card-body">
                    <h2 className="card-title mb-3 text-center">Summary of Notes</h2>
                    <textarea value={obj.summary || "No summary available."}
                    className="form-control border-0 shadow-sm p-3 text-left"
                    style={{ width: "100%", height: "150px", overflowY: "auto", fontSize: "1rem"}
                    }>
                    </textarea>

                    <h2 className="card-title mt-4">Questions & Hints</h2>
                    {obj.questions_hints && obj.questions_hints.length > 0 ? (
                        obj.questions_hints.map((q, index) => (
                            <li key={index} className="list-group-item">
                                <strong>Q {index + 1}: {q.question}</strong>
                                <p className="text-muted">{q.hint}</p>
                            </li>
                        ))
                    ) : (
                        <p className="text-light">No questions available.</p>
                    )}

                    {/* Next Topics Section */}
                    <h2 className="card-title mt-4">Related Topics</h2>

                    {obj.next_topics && obj.next_topics.length > 0 ? (
                        <div className="d-flex flex-wrap gap-2">
                            {obj.next_topics.map((topic, index) => (
                                <span key={index} className="badge bg-primary p-2">
                                {topic.topic} </span>
                            ))}
                        </div>
                        
                    ) : (
                        <p className="text-light">No topics available.</p>
                    )}

                    {/* Links Section */}
                    <h2 className="card-title mt-4">Related Links</h2>

                    {obj.next_topics && obj.next_topics.length > 0 ? (
                        <div className="d-flex flex-wrap gap-2">
                            {obj.next_topics.map((topic, index) => (
                                <a key={index} href={topic.link} target="_blank" rel="noopener noreferrer" className="badge bg-success p-2">
                                    {topic.link}
                                </a>
                            ))}
                        </div>
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