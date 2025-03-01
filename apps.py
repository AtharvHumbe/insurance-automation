from flask import Flask, request, jsonify
import pytesseract
import spacy
import fitz  # PyMuPDF
from PIL import Image
import re
import os
import io
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Uploads directory
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists

# Supabase credentials (use environment variables)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyMuPDF."""
    extracted_text = ""
    doc = fitz.open(pdf_path)  # Open the PDF
    
    for page_num in range(len(doc)):
        page = doc[page_num]  
        pix = page.get_pixmap()  # Convert to image
        img = Image.open(io.BytesIO(pix.tobytes("png")))  # Convert to PIL image
        extracted_text += pytesseract.image_to_string(img, lang="eng") + "\n"
    
    return extracted_text.strip()

def extract_info(text):
    """Extract relevant details using regex and NLP."""
    extracted_data = {
        "Name": "Not found",
        "Age": "Not found",
        "Address": "Not found",
        "Diagnosis": "Not found",
        "Hospital": "Not found"
    }

    # Regex for structured data extraction
    name_match = re.search(r"Name[:\s]+([A-Za-z ]+)", text)
    age_match = re.search(r"Age[:\s]+(\d+)", text)
    hospital_match = re.search(r"Hospital[:\s]+([A-Za-z ]+)", text)
    diagnosis_match = re.search(r"Diagnosis[:\s]+(.+)", text)
    address_match = re.search(r"Address[:\s]+(.+)", text)

    # Assign extracted values
    if name_match:
        extracted_data["Name"] = name_match.group(1).strip()
    if age_match:
        extracted_data["Age"] = age_match.group(1).strip()
    if hospital_match:
        extracted_data["Hospital"] = hospital_match.group(1).strip()
    if diagnosis_match:
        extracted_data["Diagnosis"] = diagnosis_match.group(1).strip()
    if address_match:
        extracted_data["Address"] = address_match.group(1).strip()

    return extracted_data

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle medical report upload and extract data using OCR."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Extract text from the uploaded PDF
    extracted_text = extract_text_from_pdf(file_path)
    
    # Extract relevant details using NLP
    extracted_data = extract_info(extracted_text)

    # Check if user already exists in Supabase
    existing_user = supabase.table("users").select("*").eq("email", email).execute()
    
    if existing_user.data:
        return jsonify({"error": "User already exists"}), 400

    # Insert user data into Supabase
    data = {"name": name, "email": email, "phone": phone}
    supabase.table("users").insert(data).execute()

    # Delete uploaded file after processing
    os.remove(file_path)

    return jsonify({"message": "Data saved successfully", "extracted_data": extracted_data})

if __name__ == "__main__":
    app.run(debug=True)
