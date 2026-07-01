import pymupdf
import pymupdf4llm

def extract_text_from_pdf(path):
    doc = pymupdf.open(path)
    full_text = ""
    for page in doc:
        full_text += page.get_text() + "\n"

    return full_text

def extract_text_from_pdf_to_markdown(path):
    md = pymupdf4llm.to_markdown(path)
    return md

def extract_text_from_pdf_to_json(path):
    json = pymupdf4llm.to_json(path)
    return json

def extract_text_from_pdf_to_txt(path):
    json = pymupdf4llm.to_text(path)
    return json