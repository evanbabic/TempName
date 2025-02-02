import { FaFileAlt, FaVideo } from "react-icons/fa";
import { useRef } from "react";
import axios from "axios";
import { useState } from "react";

function MainPage({ setShowResults, setResults }) {
    const imageInputRef = useRef(null);
    const pdfInputRef = useRef(null);
    const [selectedFile, setSelectedFile] = useState(null);

    const handleImageUpload = () => {
        imageInputRef.current.click();
    };

    const handlePdfUpload = () => {
        pdfInputRef.current.click();
    };

    const handleFileChange = async (e) => { 
        const file = e.target.files[0];
        if (!file) return;

        setSelectedFile(file);
        const formData = new FormData();
        formData.append("file", file);

        const isPDF = file.type === "application/pdf";
        const endpoint = isPDF ? "/pdf" : "/image";

        try {
            const response = await axios.post(`http://localhost:5000${endpoint}`, formData, {
                headers: { "Content-Type": "multipart/form-data" }
            });

            console.log("Upload successful:", response.data);
            setResults(response.data.ai_summary || "No summary available.");
            setShowResults(true); // ✅ Now we switch views only after getting API response
        } catch (error) {
            console.error("Upload failed:", error);
        }
    };

    return (
        <div className="container-fluid d-flex flex-column justify-content-center align-items-center vh-100 bg-dark ">
        
        <input
            type="file"
            ref={imageInputRef}
            className="d-none"
            accept="image/*"
            onChange= {handleFileChange}
        />

        <input
            type="file"
            ref={pdfInputRef}
            className="d-none"
            accept="application/pdf"
            onChange= {handleFileChange}
        />
        
        {/* Logo- uncomment later */}
        {/* <img src="src\assets\logo.png" className="img-thumbnail"></img> */}

        <div className="card shadow-lg p-4 mb-4 w-50">
            <div className="card-body text-center">
            <h2 className="card-title mb-3">Enter your notes for summary:</h2>
            <div className="input-group">
                <span className="input-group-text">📝</span>
                <textarea className="form-control" placeholder="Type here.."></textarea>
            </div>
            </div>
        </div>

        <p className="text-light fw-bold">Or:</p>

        <div className="d-flex justify-content-center gap-5">

        <div className="d-flex flex-column align-items-center">
            <button className="btn border-0 bg-transparent" onClick={handleImageUpload}>
            <FaFileAlt size={60} className="text-primary mb-2" />
            </button>
            <p className="fw-semibold text-light">Upload Notes (image)</p>
        </div>

        <div className="d-flex flex-column align-items-center">
            <button className="btn border-0 bg-transparent" onClick={handlePdfUpload}>
            <FaFileAlt size={60} className="text-danger mb-2" />
            </button>
            <p className="fw-semibold text-light">Upload PDF</p>
        </div>

        </div>
    </div>
    )
}

export default MainPage;

