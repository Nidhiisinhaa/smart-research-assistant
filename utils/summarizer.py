import torch
import fitz  # PyMuPDF
from transformers import pipeline

# Automatically choose GPU if available, else CPU
device = 0 if torch.cuda.is_available() else -1

# Load summarization pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=device)

# Extract full text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Generate a concise summary (<= 150 words)
def summarize_text(text):
    # Truncate to first 1000 characters to stay within token limits
    text = text[:1000] if len(text) > 1000 else text
    summary = summarizer(text, max_length=120, min_length=40, do_sample=False)
    return summary[0]['summary_text']
