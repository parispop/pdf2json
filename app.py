from flask import Flask, request, jsonify
import fitz  # PyMuPDF for PDFs
import docx  # For Word documents

app = Flask(__name__)

# Extract text from PDF
def extract_pdf_text(pdf_file):
    doc = fitz.open(pdf_file)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Extract text from Word document
def extract_word_text(word_file):
    doc = docx.Document(word_file)
    return "\n".join([para.text for para in doc.paragraphs])

@app.route('/extract', methods=['POST'])
def extract_content():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    filename = file.filename

    if filename.endswith('.pdf'):
        content = extract_pdf_text(file)
    elif filename.endswith('.docx'):
        content = extract_word_text(file)
    else:
        return jsonify({"error": "Unsupported file format"}), 400

    return jsonify({"content": content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
