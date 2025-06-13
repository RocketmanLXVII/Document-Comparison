📄 Universal Document Comparison Tool

A free, open-source tool that compares two documents of any type using a local LLM (e.g., Mistral or Llama3 via Ollama).

✅ Features

📂 Supports: .txt, .pdf, .docx, .xlsx, .csv

🧠 Powered by Mistral / Llama3 via Ollama – no API cost

💬 Interactive Q&A interface about document content

🔒 Runs locally – private and secure

Optional Features:

🔄 Model selection

📤 Exportable results (coming soon)

📄 Raw text preview

🧪 Smart input validation

🚀 Setup Instructions

🧱 Step 1: Install Ollama

Download and install from 👉 https://ollama.ai

Then pull your preferred model:

ollama pull mistral
# OR
ollama pull llama3

🐍 Step 2: Install Python Dependencies

Ensure you have Python 3.9+ installed.

pip install streamlit pandas PyPDF2 python-docx openpyxl ollama

Tip: Use a virtual environment for better isolation:

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt

▶️ Step 3: Run the App

streamlit run app.py

Then, open your browser to 👉 http://localhost:8501

📁 File Structure

universal-document-comparison/
├── README.md         # This file
├── requirements.txt  # Python dependencies
├── app.py            # Streamlit application

🧪 Supported File Types

📄 Plain Text — .txt

📄 PDF — .pdf

📝 Word — .docx

📊 Excel — .xlsx

📈 CSV — .csv

✨ Support for .pptx coming soon!

💬 Interactive Q&A

Ask natural language questions like:

"🔍 What is the main topic of Document 1?"

"📑 List the key differences between the two documents"

"📉 Explain the data trends in Document 2"

The app uses AI-powered responses based on the uploaded content.

📝 License

This project is licensed under the MIT License – see the LICENSE file for details.

🤝 Contributions

We welcome your contributions! Consider adding:

📄 Exporting comparison results to PDF/Word

🧩 Supporting more file types (like .pptx)

🌙 Dark mode UI

🔁 Model switching dropdown

Feel free to fork, improve, and submit a PR! 🚀

