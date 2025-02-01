import cv2
import numpy as np
import google.generativeai as genai
from google.cloud import vision, speech
from pytube import YouTube
from pydub import AudioSegment
from google.cloud import videointelligence, speech_v1p1beta1
from werkzeug.utils import secure_filename
import os
import json
import tempfile
import subprocess
from flask import Flask, request, jsonify, render_template


# Initialize Flask App
app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "intrepid-tape-449619-h9-e42fe89fff7c.json"
vision_client = vision.ImageAnnotatorClient()

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


# Function to generate AI-powered summaries and mind maps

def generate_ai_summary(extracted_text):
    prompt = f"""
    Given the following handwritten notes, extract the key points, summarize them concisely, and generate a structured mind map format.

    Notes:
    {extracted_text}

    Your response should be in the following format:
    
    **Summary:**
    - A brief, well-structured summary of the key takeaways from the notes.

    **Key Points:**
    - Bullet-point list of the most important details.

    **Mind Map Structure (JSON Format):**
    {{
        "main_topic": "Overall Topic",
        "subtopics": [
            {{
                "name": "Subtopic 1",
                "details": ["Key detail 1", "Key detail 2"]
            }},
            {{
                "name": "Subtopic 2",
                "details": ["Key detail 3", "Key detail 4"]
            }}
        ]
    }}
    """
    
    try:
        response = gemini_model.generate_content(prompt)
        return response.text if response and response.text else "AI could not generate a summary."
    except Exception as e:
        return f"Error generating summary: {str(e)}"

@app.route("/next_link", methods=["POST"])
def generate_next_topics():
    data = request.get_json()
    extracted_text = data.get("extracted_text", "")

    if not extracted_text:
        return jsonify({"error": "No extracted text provided"}), 400

    # **Enhanced AI Prompt for Better Topic Suggestions**
    prompt = f"""
    Based on the following study notes, suggest the **next three learning topics** that should logically follow this concept. 

    Notes:
    {extracted_text}

    **Instructions:**
    - Identify knowledge gaps or natural next steps based on the content.
    - Focus on deeper learning within the same subject area.
    - Return a structured JSON response.

    **Expected Response Format:**
    {{
        "topics": [
            {{
                "name": "Next topic 1",
                "reason": "Why this topic is relevant based on the notes",
                "link": "A useful learning resource (if available)"
            }},
            {{
                "name": "Next topic 2",
                "reason": "Why this topic is relevant based on the notes",
                "link": "A useful learning resource (if available)"
            }},
            {{
                "name": "Next topic 3",
                "reason": "Why this topic is relevant based on the notes",
                "link": "A useful learning resource (if available)"
            }}
        ]
    }}
    """

    try:
        response = gemini_model.generate_content(prompt)
        ai_response = response.text.strip() if response and response.text else ""

        # **Ensure AI Response is JSON Valid**
        import json
        topics_data = json.loads(ai_response)
        
        if "topics" in topics_data and len(topics_data["topics"]) >= 3:
            return jsonify(topics_data)

        return jsonify({"error": "AI did not generate valid topics."})

    except Exception as e:
        return jsonify({"error": f"AI error: {str(e)}"}), 500




@app.route("/summarize_video", methods=["POST"])
def summarize_video():
    data = request.get_json()
    video_url = data.get("video_url")

    if not video_url:
        return jsonify({"error": "No video URL provided"})

    try:
        # **🎥 Extract Key Topics from Video**
        client = videointelligence.VideoIntelligenceServiceClient()
        features = [videointelligence.Feature.LABEL_DETECTION]
        operation = client.annotate_video(request={"input_uri": video_url, "features": features})
        result = operation.result(timeout=180)  # Wait for processing

        labels = [annotation.entity.description for annotation in result.annotation_results[0].segment_label_annotations]
        topics = ", ".join(labels) if labels else "No key topics detected"

        # **🔊 Extract Transcript from Audio**
        speech_client = speech_v1p1beta1.SpeechClient()
        audio = {"uri": video_url}
        config = {"language_code": "en-US", "enable_automatic_punctuation": True, "model": "video"}

        operation = speech_client.long_running_recognize(config=config, audio=audio)
        response = operation.result(timeout=300)

        transcript = " ".join([result.alternatives[0].transcript for result in response.results])[:2000]  # Limit to 2000 chars

        # **🧠 AI Summary with Enhanced Prompt**
        ai_summary = generate_ai_summary(f"""
        The following video contains the topics: {topics}.
        
        Here is a short excerpt from the video transcript: "{transcript[:500]}..."
        
        Please summarize the **key learnings** and generate a **mind map structure** that organizes the topics effectively.
        """)

        return jsonify({
            "video_url": video_url,
            "topics": labels,
            "transcript_excerpt": transcript[:500],  # First 500 chars for preview
            "ai_summary": ai_summary
        })

    except Exception as e:
        return jsonify({"error": str(e)})





# Homepage Route
@app.route("/")
def index():
    return render_template("index.html")


# handling image upload
@app.route("/upload", methods=["POST"])
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




# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
