import { FaFileAlt } from "react-icons/fa";
import {MdAddAPhoto} from "react-icons/md";
import { useRef } from "react";
import axios from "axios";
import { useState } from "react";

function MainPage({ setShowResults, setResults, setLoading }) {
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

        const isPDF = file.name.toLowerCase().endsWith(".pdf");
        const endpoint = isPDF ? "/pdf" : "/image";

        setLoading(true);

        try {
            const response = await axios.post(`http://localhost:5000${endpoint}`, formData, {
                headers: { "Content-Type": "multipart/form-data" }
            });

            console.log("Upload successful:", response.data);
            setResults(response.data.ai_summary || "No summary available.");
        } catch (error) {
            console.error("Upload failed:", error);
        }

        finally {
            setLoading(false);
            setShowResults(true);
        }
    };

    return (
        <div className="container-fluid d-flex flex-column justify-content-center align-items-center vh-100 ">
        
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

        <div className="card shadow-lg p-4 mb-4 w-50 bg-light">
            <div className="card-body text-center bg-light">
            <h2 className="card-title mb-3 text-dark">Enter your notes for summary:</h2>
            <div className="input-group">
                <span className="input-group-text">📝</span>
                <textarea className="form-control" placeholder="Type here.."></textarea>
            </div>
            <br></br>
            <button type="submit" className="btn btn-success">Submit</button>
            </div>
        </div>

        <p className="text-light text-dark">Or, upload a file containing your notes:</p>

        <div className="d-flex justify-content-center gap-5">

        <div className="d-flex flex-column align-items-center">
            <button className="btn border-0 bg-transparent upload-button" onClick={handleImageUpload}>
            <MdAddAPhoto size={60} className="text-dark mb-2" />
            </button>
            <p className="fw-semibold text-dark">Upload Notes (image)</p>
        </div>

        <div className="d-flex flex-column align-items-center">
            <button className="btn border-0 bg-transparent upload-button" onClick={handlePdfUpload}>
            <FaFileAlt size={60} className="text-primary mb-2" />
            </button>
            <p className="fw-semibold text-dark">Upload PDF</p>
        </div>
        </div>
    </div>
    )
}

export default MainPage;

