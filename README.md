# Resume Matcher & Enhancer 

A smart tool to analyze resumes, match them with job descriptions, and provide actionable enhancement suggestions.

<br>

##  Features

| Feature | Description |
|---------|-------------|
| **📁 Batch Analysis** | Compare multiple resumes against a job description |
| **🔍 Single Resume Enhancement** | Get personalized improvement suggestions |
| **🧠 NLP-Powered** | Uses spaCy for advanced text processing |
| **📊 Smart Scoring** | Weighted similarity algorithm with domain-specific factors |
| **🛠 Actionable Feedback** | Concrete suggestions for resume improvement |
| **📝 Formatting Checks** | Identifies common resume formatting issues |

<br>

## Demo Walkthrough

### 1. Home Page
<img width="1312" alt="1-home" src="https://github.com/user-attachments/assets/c1ca5956-07d0-4e24-97ab-f2c6be0dce33" />

*Start by choosing between batch analysis (for recruiters) or single resume enhancement (for job seekers).*

---

### 2. Batch Analysis Setup
<img width="1344" alt="2-batch-upload" src="https://github.com/user-attachments/assets/7b4e483b-cc3a-4229-bba0-d842a89ab3d3" />

**Features Highlighted:**
- Paste any job description (lets use *"Jr. SDE @ Amazon"*)
- Upload 4 test resumes (can be 10 total:
  - ✅ `Perfect_Resume.pdf` (Tailored match)
  - ⚠️ `Good_Resume.pdf` (Good match)
  - ❌ `Poor_Resume.pdf` (Low score)
  - 🚫 `Domain_Mismatch.pdf` (Wrong field)

---

### 3. Smart Matching Results
<img width="678" alt="3-results" src="https://github.com/user-attachments/assets/f75e3324-38fd-4fdc-9671-ead1867bfba3" />

**Key Features Demonstrated:**
- Ranked results (100-0% match scores)
- Color-coded quality indicators
- Automatic detection of `Domain_Mismatch.pdf` as non-technical
- Candidate breakdown showing:
  - ✅ 100% match for `Perfect_Resume.pdf`
  - ⚠️ 66.67% match for `Good_Resume.pdf`
  - ❌ 36.67% match for `Poor_Resume.pdf`
  - 🔍 Hover tooltips explaining scores

---

### 4. Single Resume Mode
<img width="837" alt="4-single-mode" src="https://github.com/user-attachments/assets/00f05349-b759-49f2-bf70-1698a7f5af14" />

*Alternative flow for job seekers to optimize one resume against a specific job.*

<br>

## 🧰 Tech Stack

### Backend
- **Python** - Core programming language
- **Flask** - Web framework (handles routing, requests, responses)

### Frontend

- **HTML5** - Page structure
- **Bootstrap 5** - Responsive layout and components
- **Vanilla JavaScript** - Interactive elements
- **Custom CSS** - Styling enhancements 

### Key Libraries
| Library | Purpose | Category |
|---------|---------|----------|
| spaCy | NLP processing and analysis | NLP |
| scikit-learn | Similarity scoring and TF-IDF | ML/Data Science |
| PyPDF2 | PDF text extraction | File Processing |
| docx2txt | Word document parsing | File Processing |

<br>

## 📂 Supported File Formats

| Format | Icon | Notes |
|--------|------|-------|
| **PDF** (.pdf) | 📄 | Best for preserving formatting |
| **Word** (.docx) | 📑 | Supports rich text formatting |
| **Plain Text** (.txt) | 📝 | Most compatible but limited formatting |

<br>

## 🛠 Installation

### Prerequisites
- Python 3.7+
- pip
- Virtual environment (recommended)

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/resume-matcher.git
cd resume-matcher

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run the application
python app.py
