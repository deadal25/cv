import fitz  # PyMuPDF
import re

# def clean_text(text):
#     text = re.sub(r'\n+', ' ', text)
#     text = re.sub(r'\s+', ' ', text)
#     return text.lower().strip()
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'\r', '\n', text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def extract_text_from_pdf(file):
    text = ""

    try:
        # buka file dari stream (Streamlit uploader)
        pdf = fitz.open(stream=file.read(), filetype="pdf")

        for page in pdf:
            page_text = page.get_text()
            if page_text:
                text += page_text + " "

        pdf.close()
        return clean_text(text)

    except Exception as e:
        print("Error reading PDF:", e)

    return text.lower()