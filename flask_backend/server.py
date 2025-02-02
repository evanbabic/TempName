import numpy as np
import google.generativeai as genai
from google.cloud import vision, speech
from google.cloud import videointelligence, speech_v1p1beta1
from werkzeug.utils import secure_filename
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pdfplumber;

# Initialize Flask App
app = Flask(__name__)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "intrepid-tape-449619-h9-e42fe89fff7c.json"
vision_client = vision.ImageAnnotatorClient()
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Configure Google Gemini API
genai.configure(api_key="AIzaSyDyDMkII7Ra-_tMur-ZNXyfzm6QrpMzQrg")
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# Define Upload Folder
UPLOAD_FOLDER = "uploads"  
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to extract text using Google Cloud Vision API
def extract_text_from_image(image_path):
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description if texts else "No text detected"

#Function to generate AI-powered summaries and mind maps
def generate_ai_summary(extracted_text):

    prompt = f"""
    Given the following handwritten notes, extract structured information in JSON format. The response should be divided into 4 sections:

    Notes: {extracted_text}

    Do not include any formatting (ie. including ```json at the start) that could mess with parsing.

    **1 Summary:**
    - Provide a concise, well-structured summary of the key learnings.

    **2 Key Points:**
    - List **5** of the most crucial details in bullet points.

    **3 Questions & Hints:**
    - Generate **three** thought-provoking questions about the topic.
    - Provide a hint for each question along with a related resource link.

    **4 Next Topics & Relations:**
    - Suggest **two** directly related topics.
    - Explain why each is relevant to the current topic.

    Format the response in JSON like this:
    
    {{
        "summary": "A brief but detailed summary of the topic.",
        "key_points": [
            "Key concept 1",
            "Key concept 2",
            "Key concept 3",
            "Key concept 4",
            "Key concept 5"
        ],
        "questions_hints": [
            {{
                "question": "What is the main purpose of using this concept?",
                "hint": "Think about its efficiency compared to alternatives.",
                "link": "https://example.com/resource1"
            }},
            {{
                "question": "How does this topic relate to real-world applications?",
                "hint": "Consider industries that rely on it heavily.",
                "link": "https://example.com/resource2"
            }},
            {{
                "question": "What are some limitations or drawbacks?",
                "hint": "Think about scalability, performance, or restrictions.",
                "link": "https://example.com/resource3"
            }}
        ],
        "next_topics": [
            {{
                "topic": "Advanced Concept 1",
                "reason": "This builds upon the foundational ideas introduced here.",
                "link": "https://example.com/next1"
            }},
            {{
                "topic": "Advanced Concept 2",
                "reason": "Understanding this helps with real-world implementation.",
                "link": "https://example.com/next2"
            }}
        ]
    }}
    """
    
    try:
        response = gemini_model.generate_content(prompt)
        return response.text if response and response.text else "AI could not generate a summary."
    except Exception as e:
        return f"Error generating summary: {str(e)}"
    

# Homepage Route
@app.route("/")
def index():
    return render_template("index.html")

# handling image upload
@app.route("/image", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        extracted_text = extract_text_from_image(filepath)
        ai_summary = generate_ai_summary(extracted_text)
        return jsonify({
            "filename": filename,
            "extracted_text": extracted_text,
            "ai_summary": ai_summary
        })
    
    return jsonify({"error": "Invalid file type"})

@app.route("/pdf", methods=["POST"])
def upload_pdf_to_gemini():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    try:
        extracted_text = ""

        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"

        if not extracted_text.strip():
            return jsonify({"error": "No readable text found in the PDF."}), 400
        
        prompt = f"""Given the following handwritten notes, extract structured information in JSON format. The response should be divided into 4 sections:

    Notes: {extracted_text}

    Do not include any formatting (ie. including ```json at the start) that could mess with parsing.

    **1️⃣ Summary:**
    - Provide a concise, well-structured summary of the key learnings.

    **2️⃣ Key Points:**
    - List **5** of the most crucial details in bullet points.

    **3️⃣ Questions & Hints:**
    - Generate **three** thought-provoking questions about the topic.
    - Provide a hint for each question along with a related resource link.

    **4️⃣ Next Topics & Relations:**
    - Suggest **two** directly related topics.
    - Explain why each is relevant to the current topic.

    Format the response in JSON like this:
    
    {{
        "summary": "A brief but detailed summary of the topic.",
        "key_points": [
            "Key concept 1",
            "Key concept 2",
            "Key concept 3",
            "Key concept 4",
            "Key concept 5"
        ],
        "questions_hints": [
            {{
                "question": "What is the main purpose of using this concept?",
                "hint": "Think about its efficiency compared to alternatives.",
                "link": "https://example.com/resource1"
            }},
            {{
                "question": "How does this topic relate to real-world applications?",
                "hint": "Consider industries that rely on it heavily.",
                "link": "https://example.com/resource2"
            }},
            {{
                "question": "What are some limitations or drawbacks?",
                "hint": "Think about scalability, performance, or restrictions.",
                "link": "https://example.com/resource3"
            }}
        ],
        "next_topics": [
            {{
                "topic": "Advanced Concept 1",
                "reason": "This builds upon the foundational ideas introduced here.",
                "link": "https://example.com/next1"
            }},
            {{
                "topic": "Advanced Concept 2",
                "reason": "Understanding this helps with real-world implementation.",
                "link": "https://example.com/next2"
            }}
        ]
    }}
    """
        # 🔹 Send extracted text to Gemini
        response = gemini_model.generate_content(f"{prompt}")

        print(response)

        return jsonify({
            "filename": filename,
            "extracted_text": extracted_text,
            "ai_summary": response.text if response and response.text else "Gemini could not generate a summary."
        })

    except Exception as e:
        return jsonify({"error": f"Error processing PDF with Gemini: {str(e)}"}), 500


# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)