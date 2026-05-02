⚡ Electricity Bill Extraction & Automation System

🚀 Overview

An intelligent automation system that extracts structured data from electricity bills (images & PDFs) using AI and stores it in a centralized dataset.

This tool replaces manual data entry with a fast, scalable pipeline:

👉 Upload bill → 🤖 AI extracts → 📊 Structured data stored automatically

🎯 Problem Statement

Extracting data from electricity bills manually is:

* ⏳ Time-consuming (15–30 minutes per bill)
* ❌ Error-prone
* 📉 Not scalable for bulk processing

This project solves the problem by automating the entire workflow using AI.

🧠 Solution Approach
🔥 AI-Powered Extraction

Instead of relying on traditional parsing, this system use Gemini Multimodal AI to:

* Read images and PDFs directly
* Understand layout and structure
* Extract meaningful fields accurately

📌 Extracted Fields

* Consumer ID
* Customer Name
* Billing Date
* Units Consumed
* Total Amount
* Due Date

---

 🔍 OCR vs AI (Design Decision)

 🧪 OCR-Based Approach (Tesseract)

* Converts image → raw text
* Requires regex/rule-based extraction
  
Limitations:

* ❌ No layout awareness
* ❌ Sensitive to image quality
* ❌ Frequent character errors
* ❌ Requires format-specific rules
* ❌ Hard to scale

---

🧠 AI-Based Approach (Gemini)

Advantages:

* ✅ Works across multiple bill formats
* ✅ Understands document context
* ✅ No rule-based parsing needed
* ✅ Higher accuracy
* ✅ Faster implementation

---

⚖️ Final Decision

OCR was evaluated but not used as the primary method.

👉 Gemini is the main extraction engine, with OCR only as a fallback option.

💡 Key Insight:
OCR reads text. AI understands documents.

🏗️ System Architecture

User Input (File / Multiple / Folder)
                ↓
        FastAPI Backend
                ↓
     Gemini Multimodal API
                ↓
       Structured JSON Output
                ↓
        CSV Storage System
                ↓
         Frontend Display

⚙️ Features

✅ 1. Smart Data Extraction

* AI-based document understanding
* Handles semi-structured bill formats

✅ 2. Unified API

Endpoint:

```
POST /extract-bill
```

Supports:

* Single file upload
* Multiple file upload
* Folder path processing


✅ 3. Batch Processing

* Process entire folders automatically
* Loop → Extract → Store

✅ 4. Centralized CSV Storage

All extracted data is stored in:

```
output/all_bills.csv
```

Includes:

* File name tracking
* Structured fields
* Duplicate handling

---

 ✅ 5. Simple Frontend UI

* Upload bills easily
* Enter folder path
* View extracted results instantly

---

📁 Project Structure

```
bill-extractor/
│
├── app.py
├── config.py
├── batch_processor.py
├── requirements.txt
│
├── extractor/
│   └── gemini_extractor.py
│
├── utils/
│   └── csv_writer.py
│
├── frontend/
│   └── index.html
│
├── uploads/
├── output/
│   └── all_bills.csv
│
└── .env
```

---
🛠️ Setup Instructions

1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd bill-extractor
```

---

2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

* Windows:

```bash
venv\Scripts\activate
```

* Mac/Linux:

```bash
source venv/bin/activate
```

---

3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install fastapi uvicorn pandas pillow python-dotenv google-generativeai openpyxl
```

---

🔑 Gemini API Setup

1. Visit: [https://aistudio.google.com/](https://aistudio.google.com/)
2. Generate an API key
3. Create `.env` file in root:

```
GEMINI_API_KEY=your_api_key_here
```

⚠️ important:

* Do NOT share your API key
* Add `.env` to `.gitignore`

---

▶️ Run the Application

Start Backend

```bash
uvicorn app:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

Run Frontend

Open in browser:

```
frontend/index.html
```

---

🧪 Usage

📄 Single File

Upload one bill → get instant results

📂 Multiple Files

Upload multiple bills → processed together

🗂️ Batch Folder

Provide folder path:

```
C:\Users\YourName\Desktop\bills
```

---

📊 Sample Output

```
file_name,consumer_id,name,billing_date,units,amount,due_date
bill1.png,267767122167,John Doe,01-04-2026,320,1450,15-04-2026
```

---

⚠️ Limitations

* 🌐 Requires internet (Gemini API)
* 📉 Accuracy depends on image quality
* 💻 Folder processing works locally only

---

🚀 Future Improvements

* 📊 Excel-based automation (e.g., solar analysis)
* 🗄️ Database integration
* ☁️ Cloud deployment
* 🎨 UI enhancements
* 📈 Confidence scoring

---

💬 Summary

This project showcases:

* 🤖 AI-driven document processing
* ⚙️ Backend API development
* 📂 Batch automation
* 🌐 Full-stack integration

👉 A complete transformation from manual work to an automated pipeline.

---

## 👨‍💻 Author

**Swapnil Gilbile**
