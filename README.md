# 🚀 Document-Comparison
![GitHub Created At](https://img.shields.io/github/created-at/RocketmanLXVII/Document-Comparison)
![GitHub contributors](https://img.shields.io/github/contributors/RocketmanLXVII/Document-Comparison)
![GitHub License](https://img.shields.io/github/license/RocketmanLXVII/Document-Comparison)

A **universal, local, and secure** open-source tool that **compares any two documents** using a local LLM (e.g., Mistral or Llama3 via Ollama).

## 📖 Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Architecture](#architecture)  
4. [Installation & Setup](#installation--setup)  
5. [Usage](#usage)  
6. [Supported Formats](#supported-formats)  
7. [Performance & Benchmarks](#performance--benchmarks)  
8. [Troubleshooting](#troubleshooting)  
9. [Use Cases](#use-cases)  
10. [Roadmap](#roadmap)  
11. [Contributing](#contributing)  
12. [License](#license)  
13. [Acknowledgments](#acknowledgments)  

## 📌 Overview

Document-Comparison is a **privacy-focused**, **zero-cost** tool designed to help individuals and teams quickly identify differences and insights across any two documents. By running entirely **locally** with no external API calls, it guarantees data security while leveraging state-of-the-art LLMs for contextual comparison and Q&A.

## ✨ Features

| Category               | Feature                                                    | Status       |
|------------------------|------------------------------------------------------------|--------------|
| Core                   | Side-by-side comparison highlighting additions, deletions  | ✅ Implemented |
|                        | Semantic diff with contextual summaries                    | ✅ Implemented |
|                        | Interactive Q&A on document content                        | ✅ Implemented |
| File Formats           | .txt, .pdf, .docx, .xlsx, .csv                             | ✅ Implemented |
|                        | .pptx                                                       | 🔜 Upcoming |
| Model Options          | Mistral (via Ollama)                                       | ✅ Implemented |
|                        | Llama3 (via Ollama)                                        | ✅ Implemented |
| Export                 | JSON/CSV export of comparison results                      | 🔜 Upcoming |
|                        | PDF/Word report generation                                 | 🔜 Upcoming |
| UI                     | Streamlit web interface                                    | ✅ Implemented |
|                        | Dark mode                                                 | 🔜 Upcoming |
| Validation             | File integrity and schema checks                           | ✅ Implemented |
|                        | Smart input validation                                     | 🔜 Upcoming |

## 🏗️ Architecture

```
Document-Comparison/
├── app.py            # Main Streamlit app
├── comparedocs.py    # CLI batch comparison
├── universal_utils.py# File loaders & parsers
├── llm_interface.py  # Ollama integration
├── requirements.txt  # Dependencies
└── README.md         # This file
```

1. **app.py**: Streamlit interface for uploading, comparing, and Q&A.  
2. **comparedocs.py**: Command-line tool for automated batch comparisons.  
3. **universal_utils.py**: Readers and converters for all supported formats.  
4. **llm_interface.py**: Wrapper for Ollama model calls and prompt engineering.  

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.9+  
- Ollama CLI ([Download](https://ollama.ai))  

### 1. Install Ollama & Pull Models

```bash
ollama pull mistral
# OR
ollama pull llama3
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run app.py
```

Open your browser at [http://localhost:8501](http://localhost:8501).

## 🚀 Usage

1. **Upload** two documents.  
2. **Select** your model (Mistral or Llama3).  
3. **Compare** side-by-side diffs or ask questions in the interactive Q&A panel.  
4. **Export** results (JSON/CSV) or generate a PDF/Word report (coming soon).

**Sample Q&A Prompts:**

- “What are the key differences between Document A and B?”  
- “Summarize changes in Section 3.”  
- “Explain the data trends in the uploaded spreadsheet.”  

## 📂 Supported Formats

| Format             | Extension | Details                                        |
|--------------------|-----------|------------------------------------------------|
| Plain Text         | .txt      | Line-level diffs                               |
| PDF                | .pdf      | Text extraction via PyPDF2                     |
| Word Document      | .docx     | Parsing with python-docx                       |
| Excel Spreadsheet  | .xlsx     | Sheet-by-sheet comparison via openpyxl          |
| CSV Data           | .csv      | Row-level diff and summary with pandas         |
| PowerPoint Slides  | .pptx     | 🔜 Support planned                              |

## 📈 Performance & Benchmarks

| Operation              | Sample Time (local)  |
|------------------------|----------------------|
| Load & parse PDF       | ~0.8s                |
| Compare two 100-page docs | ~2.2s             |
| Q&A response latency   | ~1.0s                |

System requirements: 8 GB RAM, 2 GHz CPU, ~200 MB disk.

## 🛠️ Troubleshooting

- **“Model not found”**: Ensure Ollama model is downloaded: `ollama list`.  
- **“Unsupported format”**: Confirm file extension and content type.  
- **Slow performance**: Close other heavy apps or increase virtual environment resources.  
- **Errors parsing .docx/.xlsx**: Verify file integrity; try converting to intermediate format (e.g., PDF).

## 📚 Use Cases

- **Legal Review**: Contract clause changes analysis.  
- **Business Reports**: Version diffs in financial decks.  
- **Academic**: Manuscript revision tracking.  
- **Technical**: Code spec document comparison.

## 🔮 Roadmap

- v1.1: PDF/Word report export, .pptx support  
- v1.2: Dark mode, model-switching dropdown  
- v2.0: Plugin API, collaborative review features

## 🤝 Contributing

We welcome contributions! To get started:

1. Fork this repository.  
2. Create a feature branch: `git checkout -b feature/YourFeature`.  
3. Commit your changes: `git commit -m "Add YourFeature"`.  
4. Push: `git push origin feature/YourFeature`.  
5. Open a Pull Request with detailed description.

Please review our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Thanks to the open-source community and Ollama for enabling **local LLM** support, and to contributors for ongoing improvements!
