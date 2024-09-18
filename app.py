from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import os
import docx

app = Flask(__name__)

# Function to extract text from PDF
def extract_pdf_text(pdf_file):
    doc = fitz.open(pdf_file)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Function to extract text from Word
def extract_word_text(word_file):
    doc = docx.Document(word_file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

@app.route('/extract', methods=['POST'])
def extract_content():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename.endswith('.pdf'):
        content = extract_pdf_text(file)
    elif file.filename.endswith('.docx'):
        content = extract_word_text(file)
    else:
        return jsonify({"error": "Unsupported file format"}), 400

    return jsonify({"content": content})

if __name__ == "__main__":
    app.run(debug=True)
