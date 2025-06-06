# Summarizely - AI-Powered Document Creator

![Summarizely](https://img.shields.io/badge/Summarizely-AI%20Document%20Creator-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-red)

Summarizely is a Streamlit-based web app that transforms raw text or meeting notes into well-structured Google Docs. It leverages Google's Gemini AI to generate tutor-style summaries and the Google Docs API to automatically create, format, and share documents in your Google Drive.

## 🌟 Key Features

- 🤖 **AI-Powered Summarization**
  - Uses Google's Gemini (gemini-1.5-flash) to convert raw text into comprehensive, tutor-style study notes

- 📝 **Automated Doc Creation**
  - Instantly creates a new Google Doc with your AI-generated content

- 🔒 **Secure Service Account Handling**
  - Reads a Base64-encoded service-account JSON key at runtime (no manual upload required once deployed)

- 📂 **Shared Folder Integration**
  - Optionally create all documents inside a pre-shared Drive folder (inherits folder permissions)

- ✉️ **Auto-Sharing**
  - If no shared folder is specified, it will share each new Doc directly with your Gmail address

- 🎨 **Modern, Responsive UI**
  - Glassmorphism design, neon accents, and mobile-friendly layout for a polished user experience

- ⚡ **Real-Time Feedback**
  - Streamlit spinners and success/error banners keep you informed throughout the process

## 📁 Project Structure

```
Summarizely/
├── .devcontainer/
│   └── devcontainer.json           # Development container settings (VS Code Remote - Containers)
├── venv/                           # (Optional) Local Python virtual environment
├── .gitignore                      # Files/directories to be ignored by Git
├── README.md                       # This file
├── requirements.txt                # Python dependencies
├── streamlit_app.py                # Main Streamlit application
├── style.css                       # Custom CSS (glassmorphism, neon accents, responsive styles)
├── summarizely_sa.json             # (Optional local) service-account JSON for Google APIs
└── summarizely_sa.json.b64         # Base64-encoded version of service-account JSON (for secrets)
```

## 🔍 File Overview

- **.devcontainer/devcontainer.json**: Configuration for VS Code's "Remote – Containers" extension
- **.gitignore**: Specifies which files/folders Git should ignore
- **requirements.txt**: Lists all Python dependencies including streamlit, google-generativeai, google-api-python-client, etc.
- **streamlit_app.py**: Main application containing page configuration, custom CSS injection, sidebar inputs, and core functionality
- **style.css**: Custom CSS rules for glassmorphism backgrounds, neon accents, and responsive design
- **summarizely_sa.json**: (Optional local) Service-account JSON for Google APIs
- **summarizely_sa.json.b64**: Base64-encoded version of service-account JSON for deployment

## 🚀 Getting Started

### Prerequisites

- Python 3.8+ installed
- Google Cloud Platform project with:
  - Google Docs API enabled
  - Google Drive API enabled
  - Service Account created (with Editor role)
  - Gemini API key

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/MisbahAN/Summarizely.git
   cd Summarizely
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Service Account Setup

#### Local Testing
- Copy your downloaded `summarizely_sa.json` into the project root
- The app will read it directly from disk

#### Production/Streamlit Cloud
- Encode your service account JSON to Base64:
  ```bash
  python3 - << 'EOF'
  import base64
  print(base64.b64encode(open("summarizely_sa.json","rb").read()).decode())
  EOF
  ```
- Store the resulting string in `summarizely_sa.json.b64`

### Running Locally

1. Ensure `summarizely_sa.json` is present in the root
2. Set the environment variable (optional):
   ```bash
   export SERVICE_ACCOUNT_JSON_B64="$(cat summarizely_sa.json.b64)"
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```
4. Open your browser at `http://localhost:8501`

## 📝 Usage Instructions

1. **Gemini API Key**
   - Copy your key from Google Cloud Console
   - Paste into the "🔑 Gemini API Key" field in the sidebar

2. **Service Account**
   - Local: Ensure `summarizely_sa.json` exists in project root
   - Deployed: App will decode `SERVICE_ACCOUNT_JSON_B64` automatically

3. **Gmail Address or Shared Folder ID**
   - Enter Gmail for direct document sharing
   - Or paste a pre-shared Drive folder ID for inherited permissions

4. **Document Title**
   - Enter custom title (defaults to "AI Summary")

5. **Raw Text**
   - Paste or type your content

6. **Generate & Create**
   - Click "🚀 Generate & Create Google Doc"
   - Watch the progress with real-time feedback
   - Get a link to your new Doc when complete

## 👨‍💻 Author

Misbah Ahmed Nauman
Portfolio: [misbahan.com](https://www.misbahan.com)
