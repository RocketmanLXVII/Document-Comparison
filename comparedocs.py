import os
import json
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader
import csv
import ollama

# --- Helper Functions ---

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return '\n'.join(paragraph.text for paragraph in doc.paragraphs)

def extract_text_from_xlsx(file_path):
    df = pd.read_excel(file_path, sheet_name=None)
    full_text = ""
    for sheet_name, data in df.items():
        full_text += f"Sheet: {sheet_name}\n"
        full_text += data.to_string(index=False) + "\n\n"
    return full_text

def extract_text_from_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        return '\n'.join(['\t'.join(row) for row in reader])

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.txt':
        return extract_text_from_txt(file_path)
    elif ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    elif ext == '.xlsx':
        return extract_text_from_xlsx(file_path)
    elif ext == '.csv':
        return extract_text_from_csv(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

# --- Ollama Interaction ---

def query_ollama(prompt, model="mistral"):
    try:
        response = ollama.generate(model=model, prompt=prompt)
        return response['response']
    except Exception as e:
        print("Error calling Ollama:", str(e))
        return "[Model not found or unreachable. Make sure Ollama is running and the model is pulled.]"

# --- Main Analysis Function ---

def analyze_and_compare(doc1_text, doc2_text, model="mistral"):
    summary_prompt1 = f"Summarize the following document:\n\n{doc1_text[:5000]}"
    summary_prompt2 = f"Summarize the following document:\n\n{doc2_text[:5000]}"

    print("Summarizing Document 1...")
    summary1 = query_ollama(summary_prompt1, model)
    print("Summarizing Document 2...")
    summary2 = query_ollama(summary_prompt2, model)

    compare_prompt = f"""
Compare the following two summaries and describe their similarities and differences:

Document 1 Summary:
{summary1}

Document 2 Summary:
{summary2}

Comparison:
"""

    print("Comparing documents...")
    comparison = query_ollama(compare_prompt, model)

    return {
        "summary1": summary1,
        "summary2": summary2,
        "comparison": comparison
    }

# --- Entry Point ---

if __name__ == "__main__":
    MODEL_NAME = "mistral"

    print(f"Using model: {MODEL_NAME}. Proceeding with analysis...")

    file1 = input("Enter path to first file: ")
    file2 = input("Enter path to second file: ")

    if not os.path.exists(file1):
        print(f"First file does not exist: {file1}")
        exit(1)
    if not os.path.exists(file2):
        print(f"Second file does not exist: {file2}")
        exit(1)

    try:
        text1 = extract_text(file1)
        text2 = extract_text(file2)

        result = analyze_and_compare(text1, text2, model=MODEL_NAME)

        print("\n--- Summary of Document 1 ---")
        print(result["summary1"])

        print("\n--- Summary of Document 2 ---")
        print(result["summary2"])

        print("\n--- Comparison ---")
        print(result["comparison"])

    except Exception as e:
        print("Error during processing:", str(e))