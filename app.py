from flask import Flask, render_template, request
from docx import Document

app = Flask(__name__)

def has_duplicate_lines(file):
    # Create a set to store unique lines
    unique_lines = set()
    # Create a list to store duplicate lines along with line numbers
    duplicate_lines = []

    doc = Document(file)
    line_number = 0

    for paragraph in doc.paragraphs:
        line_number += 1
        line = paragraph.text.strip() # Remove leading and trailing spaces, convert to lowercase

        if line and not line.isspace():  # Exclude lines that only contain spaces
            start_index = line.find("(") + 1
            end_index = line.find(")")
            if start_index != -1 and end_index != -1:
                prefix = line[:start_index]  # Extract prefix before the number
                postfix = line[end_index+1:].strip()  # Extract postfix after the number, remove leading/trailing spaces
                if postfix in unique_lines:
                    duplicate_lines.append((line_number, line))
                else:
                    unique_lines.add(postfix)

    return duplicate_lines

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    # Pass the file object to the function instead of its filename
    duplicates = has_duplicate_lines(file)
    return render_template('result.html', duplicates=duplicates)

if __name__ == '__main__':
    app.run(debug=True)
