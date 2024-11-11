from docx import Document
import base64
import io

def read_job_description(file_path='job_description.txt'):
    try:
        # Open the text file in read mode with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the content of the file
            job_description = file.read()
        return job_description
    except FileNotFoundError:
        return "Job description file not found."
    

def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)
    
