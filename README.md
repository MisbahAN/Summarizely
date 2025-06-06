# Summarizely - AI-Powered Document Creator

![Summarizely](https://img.shields.io/badge/Summarizely-AI%20Document%20Creator-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

Summarizely is an AI-powered web application that transforms raw text into well-structured Google Docs. Using Google's Gemini AI and Google Docs API, it creates professional documents with proper formatting and styling.

## 🌟 Features

- 🤖 AI-powered text summarization using Google's Gemini AI
- 📝 Automatic document creation in Google Docs
- 🎨 Beautiful, modern UI with glassmorphism design
- 🔒 Secure API key management
- 📱 Responsive design for all devices
- ⚡ Real-time processing and feedback

## 📁 Project Structure

```
Summarizely/
├── streamlit_app.py      # Main application file
├── style.css            # Custom styling and animations
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── summarizely_sa.json  # Google Service Account credentials
```

### File Descriptions

- **streamlit_app.py**: The main application file containing all the Streamlit UI components, API integrations, and business logic.
- **style.css**: Custom CSS styling with modern glassmorphism effects, animations, and responsive design.
- **requirements.txt**: Lists all Python package dependencies required to run the application.
- **summarizely_sa.json**: Google Service Account credentials for Google Docs API integration.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account
- Gemini API key
- Google Service Account credentials

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Summarizely.git
   cd Summarizely
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up Google Cloud:
   - Create a project in Google Cloud Console
   - Enable Google Docs API
   - Create a service account and download credentials
   - Enable Gemini API and get your API key

### Running the Application

1. Start the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

## 📝 Usage Instructions

1. Enter your Gemini API key in the sidebar
2. Upload your Google Service Account JSON file
3. Enter your Gmail address
4. Provide the shared folder ID where documents will be created
5. Enter a title for your document
6. Paste your raw text in the main input area
7. Click "Generate Google Doc" to create your document

## 🔧 Configuration

- **Gemini API Key**: Required for AI text processing
- **Service Account JSON**: Required for Google Docs API access
- **Gmail Address**: The email where documents will be shared
- **Shared Folder ID**: Google Drive folder ID for document storage

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Visit my portfolio at [MisbahAN.com](https://www.misbahan.com/) to see more of my projects and work experience.
