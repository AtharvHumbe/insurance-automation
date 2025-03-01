# insurance-automation
Overview

The Insurance Automation Platform is a secure, AI-driven web application designed to automate the insurance verification, claim validation, and submission process. It leverages OCR (Optical Character Recognition) and NLP (Natural Language Processing) to extract key information from uploaded medical documents, reducing paperwork and improving efficiency for hospitals, patients, and insurance providers.

Features

User Form Submission: Users can fill out a form with their name, email, phone number, and upload a medical report.

OCR Processing: Extracts text from uploaded medical reports using PyMuPDF (for PDF text extraction) and Tesseract OCR.

NLP Information Extraction: Uses spaCy to extract key details such as Name, Age, Address, Diagnosis, and Hospital Name.

Data Storage: Stores user details in Supabase, while uploaded files are processed and removed after extraction.

API Endpoints: Exposes a REST API for handling file uploads and processing.

Secure & Scalable: Implements a structured backend using Flask.

Tech Stack

Frontend: HTML, CSS, JavaScript

Backend: Python (Flask)

OCR Engine: PyMuPDF, Tesseract OCR

NLP Model: spaCy (en_core_web_sm)

Database: Supabase (PostgreSQL-based backend)

Cloud Storage: Local storage for uploaded files

Installation & Setup

Prerequisites

Ensure you have the following installed:

Python 3.11+

Tesseract OCR (C:\Program Files\Tesseract-OCR\tesseract.exe)

Virtual Environment (Recommended)

Git

Clone the Repository : git clone https://github.com/AtharvHumbe/insurance-automation.git
cd insurance-automation

Set Up Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Dependencies:
pip install -r requirements.txt

Set Up Environment Variables:
Create a .env file and add the following details:SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_api_key

Run the Flask App:python apps.py


API Endpoints

Upload Medical Report

Endpoint: POST /upload

Request Body: FormData (file, name, email, phone)

Response: JSON with extracted medical details

Example Response:
{
    "message": "Data saved successfully",
    "extracted_data": {
        "Name": "John Doe",
        "Age": "45",
        "Address": "123 Street, NY",
        "Diagnosis": "Diabetes Type 2",
        "Hospital": "City Hospital"
    }
}

Troubleshooting

Common Issues & Fixes

ModuleNotFoundError: No module named 'dotenv'

Run pip install python-dotenv and restart the Flask app.

pdf2image.exceptions.PDFInfoNotInstalledError

Ensure Poppler is installed or switch to PyMuPDF (which is already implemented).

Form Submission Fails (500 Internal Server Error)

Check terminal logs for missing dependencies.

Ensure Tesseract is installed and its path is correctly configured.

Verify that Supabase credentials are correctly set up.

Future Improvements

Implement AI-based document classification.

Enable multi-language support for OCR & NLP.

Enhance security with authentication & authorization.

Deploy on cloud services (AWS, GCP, or Heroku).

Contributors

Atharv Humbe – Developer
Soham Shinde-Developer
Manas Biswas- Developer

License

This project is licensed under the MIT License.
