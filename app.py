import streamlit as st
import os
import tempfile
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader
import csv
import ollama

# --- Helper Functions ---

def extract_text_from_txt(file):
    return file.getvalue().decode("utf-8")

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    return '\n'.join(paragraph.text for paragraph in doc.paragraphs)

def extract_text_from_xlsx(file):
    df = pd.read_excel(file, sheet_name=None)
    full_text = ""
    for sheet_name, data in df.items():
        full_text += f"Sheet: {sheet_name}\n"
        full_text += data.to_string(index=False) + "\n\n"
    return full_text

def extract_text_from_csv(file):
    content = file.getvalue().decode("utf-8").splitlines()
    reader = csv.reader(content)
    return '\n'.join(['\t'.join(row) for row in reader])

def extract_text(file, file_type):
    if file_type == 'txt':
        return extract_text_from_txt(file)
    elif file_type == 'pdf':
        return extract_text_from_pdf(file)
    elif file_type == 'docx':
        return extract_text_from_docx(file)
    elif file_type == 'xlsx':
        return extract_text_from_xlsx(file)
    elif file_type == 'csv':
        return extract_text_from_csv(file)
    else:
        raise ValueError(f"Unsupported file format: {file_type}")

# --- Ollama Interaction ---

def query_ollama(prompt, model="mistral"):
    try:
        response = ollama.generate(model=model, prompt=prompt)
        return response['response']
    except Exception as e:
        return "[Error: Model not found or unreachable. Make sure Ollama is running.]"

# --- Main Analysis Function ---

def analyze_and_compare(doc1_text, doc2_text):
    summary_prompt1 = f"""Extract and organize all information from this tender PDF document under the following categories:
1. BID PREPARATION AND ELIGIBILITY

Section 7 - Bidder's Eligibility: Technical qualifications, financial criteria, experience requirements, certifications for both Project A & B
Section 23 - Bidding Process: Timeline, deadlines, evaluation methodology, award criteria
Section 22 - Bidding Document: Required forms, formats, amendment procedures
Section 24 - E-Tendering: Registration process, platform details, submission requirements
Section 6 - Facilities Management Services: Warranty deliverables, AMC scope, SLAs, performance metrics

2. SCOPE OF WORK
Project A (Network) - Section 5.1:

5.1.1 Bidder's Scope: Hardware/software, installation, configuration, testing, documentation
5.1.2 OEM's Scope: Manufacturer responsibilities, support, warranty
5.1.4 RACI Matrix: Complete responsibility assignments

Project B (Security) - Section 5.2:

5.2.1 Bidder's Scope: Implementation methodology, integration requirements
5.2.2 OEM's Scope: Vendor responsibilities, licensing
5.2.4 Solution-wise Scope: Extract specifications for NGFW, WAF, DDOS, LB, GSLB, SSL and other security solutions
5.2.5 RACI Matrix: Security project responsibility assignments

3. PROJECT & IMPLEMENTATION RESPONSIBILITIES
Extract: Project management structure, implementation phases, milestones, resource allocation, communication protocols, quality assurance processes
4. FINANCIAL AND LEGAL COMPLIANCE
Extract: Payment terms, price structure, tax requirements, performance bonds, insurance, penalty clauses, legal compliance, dispute resolution, contract terms
5. SUBMISSION FORMS & ANNEXURES
List: All required forms, annexures, declarations, technical compliance sheets, commercial bid formats, certificates
OUTPUT REQUIREMENTS:

Use clear headings matching the sections above
Include specific details: dates, amounts, technical specifications
Note missing information sections
Highlight critical eligibility requirements and deadlines
Provide page references where possible
Flag ambiguous requirements needing clarification
Extract exact text for critical requirements
Distinguish mandatory vs. optional requirements
Include all contact information for queries

Provide comprehensive extraction covering all available information in these categories from the PDF document.:\n\n{doc1_text[:5000]}"""
    summary_prompt2 = f"""
    Extract and organize all information from this tender PDF document under the following categories:
1. BID PREPARATION AND ELIGIBILITY

Section 7 - Bidder's Eligibility: Technical qualifications, financial criteria, experience requirements, certifications for both Project A & B
Section 23 - Bidding Process: Timeline, deadlines, evaluation methodology, award criteria
Section 22 - Bidding Document: Required forms, formats, amendment procedures
Section 24 - E-Tendering: Registration process, platform details, submission requirements
Section 6 - Facilities Management Services: Warranty deliverables, AMC scope, SLAs, performance metrics

2. SCOPE OF WORK
Project A (Network) - Section 5.1:

5.1.1 Bidder's Scope: Hardware/software, installation, configuration, testing, documentation
5.1.2 OEM's Scope: Manufacturer responsibilities, support, warranty
5.1.4 RACI Matrix: Complete responsibility assignments

Project B (Security) - Section 5.2:

5.2.1 Bidder's Scope: Implementation methodology, integration requirements
5.2.2 OEM's Scope: Vendor responsibilities, licensing
5.2.4 Solution-wise Scope: Extract specifications for NGFW, WAF, DDOS, LB, GSLB, SSL and other security solutions
5.2.5 RACI Matrix: Security project responsibility assignments

3. PROJECT & IMPLEMENTATION RESPONSIBILITIES
Extract: Project management structure, implementation phases, milestones, resource allocation, communication protocols, quality assurance processes
4. FINANCIAL AND LEGAL COMPLIANCE
Extract: Payment terms, price structure, tax requirements, performance bonds, insurance, penalty clauses, legal compliance, dispute resolution, contract terms
5. SUBMISSION FORMS & ANNEXURES
List: All required forms, annexures, declarations, technical compliance sheets, commercial bid formats, certificates
OUTPUT REQUIREMENTS:

Use clear headings matching the sections above
Include specific details: dates, amounts, technical specifications
Note missing information sections
Highlight critical eligibility requirements and deadlines
Provide page references where possible
Flag ambiguous requirements needing clarification
Extract exact text for critical requirements
Distinguish mandatory vs. optional requirements
Include all contact information for queries

Provide comprehensive extraction covering all available information in these categories from the PDF document.:\n\n{doc2_text[:5000]}"""

    summary1 = query_ollama(summary_prompt1)
    summary2 = query_ollama(summary_prompt2)

    compare_prompt = f"""
  COMPARE_PROMPT_TEMPLATE = 
You are a legal tender expert. Analyze and compare the two documents in detail based on the following four core categories. For each category, extract full-length content from both documents and provide a **comprehensive, line-by-line distinction** between them.

Ensure that no minor detail is missed. Use a tabular format as shown below and highlight every difference clearly.

---

### Categories to Compare:

1. **Pre Qualification Criteria / Bidder Criteria / Eligibility Criteria**
   - Include: Minimum experience, financial thresholds, certifications, team composition, prior work experience, registration requirements, disqualifying conditions, etc.

2. **Scope of Work**
   - Include: Deliverables, tasks expected from bidder, hardware/software included, service levels, responsibilities, project timelines, maintenance obligations, integration expectations, etc.

3. **Technical Qualifications**
   - Include: Required certifications, past projects, technical capabilities, domain expertise, staffing requirements, infrastructure needs, system compatibility, etc.

4. **Technical Marking**
   - Include: Weightage distribution, scoring criteria, evaluation parameters, minimum qualifying scores, tie-breaking rules, documentation required for proof, etc.

---

### Output Format:

For each category, generate a table like:

#### [Category Name]
| Sub-topic | Document 1 Details | Document 2 Details | Key Differences |
|----------|--------------------|--------------------|------------------|
| [Sub-topic 1] | [Doc1 Info] | [Doc2 Info] | [Difference Summary] |
| [Sub-topic 2] | [Doc1 Info] | [Doc2 Info] | [Difference Summary] |

Repeat for all sub-topics within each category. Ensure **every point mentioned in the original documents is compared**.

If any section is missing or incomplete in either document, clearly state so.

Now analyze and compare the documents:

Document 1:
{doc1_text}

Document 2:
{doc2_text}

Comparison:
"""

    comparison = query_ollama(compare_prompt)

    return {
        "summary1": summary1,
        "summary2": summary2,
        "comparison": comparison
    }

# --- Question Answering Function ---

def answer_question(document_text, question, model="mistral"):
    prompt = f"Based on the following document, answer the question:\n\nDocument:\n{document_text[:10000]}\n\nQuestion: {question}"
    return query_ollama(prompt, model)

# --- Streamlit UI ---

st.set_page_config(page_title="Document Analyzer", layout="wide")
st.title("📄 Document Comparison & Q&A Tool")
st.markdown("Upload two documents and let Ollama analyze them!")

with st.sidebar:
    st.header("Upload Files")
    st.markdown("Supported formats: `.txt`, `.pdf`, `.docx`, `.xlsx`, `.csv`")
    file1 = st.file_uploader("Upload First Document", type=["txt", "pdf", "docx", "xlsx", "csv"])
    file2 = st.file_uploader("Upload Second Document", type=["txt", "pdf", "docx", "xlsx", "csv"])

if file1 and file2:
    try:
        # Extract file extensions
        ext1 = file1.name.split('.')[-1].lower()
        ext2 = file2.name.split('.')[-1].lower()

        # Extract text from both files
        with st.spinner("Extracting text from documents..."):
            text1 = extract_text(file1, ext1)
            text2 = extract_text(file2, ext2)

        # Run analysis
        st.subheader("🔍 Document Analysis")
        with st.spinner("Analyzing and comparing documents with Qwen..."):
            result = analyze_and_compare(text1, text2)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📄 Summary of Document 1")
            st.write(result["summary1"])

        with col2:
            st.markdown("### 📄 Summary of Document 2")
            st.write(result["summary2"])

        st.markdown("### ⚖️ Comparison")
        st.write(result["comparison"])

        # Q&A Section
        st.markdown("---")
        st.subheader("❓ Ask Questions About Documents")
        q_col1, q_col2 = st.columns(2)

        with q_col1:
            user_q1 = st.text_input("Ask something about Document 1:")
            if user_q1:
                ans1 = answer_question(text1, user_q1)
                st.markdown("**Answer:**")
                st.write(ans1)

        with q_col2:
            user_q2 = st.text_input("Ask something about Document 2:")
            if user_q2:
                ans2 = answer_question(text2, user_q2)
                st.markdown("**Answer:**")
                st.write(ans2)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
else:
    st.info("Please upload both documents to begin analysis.")