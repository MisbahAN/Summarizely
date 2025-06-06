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

- A Google Cloud Platform project with:
  - Google Docs API enabled
  - Google Drive API enabled
  - Service Account created (with Editor role)
  - Gemini API key

### Using Summarizely

1. Visit [Summarizely Web App](https://summarizely.streamlit.app/)

2. **Gemini API Key**
   - Copy your key from Google Cloud Console
   - Paste into the "🔑 Gemini API Key" field in the sidebar

3. **Service Account**
   - The app will automatically handle service account authentication
   - No manual setup required

4. **Gmail Address or Shared Folder ID**
   - Enter Gmail for direct document sharing
   - Or paste a pre-shared Drive folder ID for inherited permissions

5. **Document Title**
   - Enter custom title (defaults to "AI Summary")

6. **Raw Text**
   - Paste or type your content

7. **Generate & Create**
   - Click "🚀 Generate & Create Google Doc"
   - Watch the progress with real-time feedback
   - Get a link to your new Doc when complete

## 👨‍💻 Author

Misbah Ahmed Nauman
Portfolio: [misbahan.com](https://www.misbahan.com)
