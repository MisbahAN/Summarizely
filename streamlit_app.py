import os
import tempfile
import streamlit as st
import google.generativeai as genai
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ─── Page Configuration (MUST be first) ─────────────────────────────────────
st.set_page_config(
    page_title="Summarizely - AI Document Creator", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# ─── Load CSS ─────────────────────────────────────────────────────────────
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ─── Enhanced Hero Section ────────────────────────────────────────────────
st.markdown(
    """
    <h1 data-text="SUMMARIZELY">SUMMARIZELY</h1>
    <div class="hero-subtitle">
        Your Python-based AI sidekick: Gemini does the heavy lifting,<br>
        then pushes polished summaries into Google Docs with futuristic style.
    </div>
    """,
    unsafe_allow_html=True,
)

# ─── Feature Highlights ──────────────────────────────────────────────────
st.markdown(
    """
    <div class="feature-grid">
        <div class="feature-item">
            <h4>🤖 AI-Powered</h4>
            <p>Advanced Gemini AI for intelligent text summarization</p>
        </div>
        <div class="feature-item">
            <h4>📄 Auto-Documentation</h4>
            <p>Seamless Google Docs integration with sharing</p>
        </div>
        <div class="feature-item">
            <h4>⚡ Lightning Fast</h4>
            <p>Process and summarize content in seconds</p>
        </div>
        <div class="feature-item">
            <h4>🔒 Secure</h4>
            <p>Your data stays protected with enterprise-grade security</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─── Enhanced Sidebar Configuration ──────────────────────────────────────
st.sidebar.markdown("### ⚙️ Configuration Panel")

# Enhanced Gemini API key input
gemini_key = st.sidebar.text_input(
    "🔑 Gemini API Key",
    type="password",
    help="Enter your Google Gemini API key here for AI summarization.",
    placeholder="Enter your Gemini API key..."
)

# Enhanced Service Account upload
st.sidebar.markdown("### 📁 Service Account Authentication")
sa_file = st.sidebar.file_uploader(
    "Upload Service Account JSON",
    type=["json"],
    help="Upload your Google Cloud service account JSON file with Docs & Drive API access."
)

# Enhanced instructions with better styling
with st.sidebar.expander("❓ How to create your service account JSON"):
    st.markdown(
        """
        ### 🚀 Quick Setup Guide
        
        **1. Google Cloud Console**  
        Visit: [console.cloud.google.com](https://console.cloud.google.com/)

        **2. Create/Select Project**  
        Click project dropdown → "New Project" → name it → Create

        **3. Enable Required APIs**  
        - APIs & Services → Library
        - Search & enable "Google Docs API"
        - Search & enable "Google Drive API"

        **4. Create Service Account**  
        - IAM & Admin → Service Accounts
        - "Create Service Account"
        - Name it (e.g., `summarizely-sa`)

        **5. Grant Permissions**  
        - Role: Project → Editor
        - Continue → Done

        **6. Generate JSON Key**  
        - Click your service account
        - Keys tab → Add Key → Create New Key
        - Choose JSON → Create & download

        **7. Upload Here**  
        - Use the file uploader above ☝️
        
        🔐 **Security Note**: Keep your JSON file safe and never commit it to repositories.
        """,
        unsafe_allow_html=True,
    )

# Enhanced Gmail input
user_gmail = st.sidebar.text_input(
    "✉️ Your Gmail Address",
    placeholder="your.email@gmail.com",
    help="Gmail account that will receive edit access to the created document."
)

# Enhanced folder ID input
shared_folder_id = st.sidebar.text_input(
    "📂 Shared Folder ID (Optional)",
    placeholder="Google Drive folder ID",
    help="If you have a pre-shared Google Drive folder, enter its ID here. Documents created inside will inherit sharing permissions."
)

# Enhanced document title input
doc_title = st.sidebar.text_input(
    "📋 Document Title",
    value="AI Summary",
    help="Custom title for your generated Google Doc."
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    ### 📋 Checklist
    - 🔑 Valid Gemini API Key
    - 📄 Service Account JSON uploaded
    - ✉️ Gmail address (if no shared folder)
    - 📁 Optional: Shared folder ID
    """,
    unsafe_allow_html=True,
)

# ─── Enhanced Main Content Area ──────────────────────────────────────────
st.markdown(
    """
    <div class="glass-card">
        <h2 style="margin-top: 0;">✍️ Input Your Content</h2>
        <p style="color: var(--text-secondary); margin-bottom: 2rem;">
            Paste or type any text you'd like to summarize. Our AI will process it and create a polished Google Doc.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

raw_text = st.text_area(
    label="",
    placeholder="✨ Paste your content here... \n\nArticles, notes, research, meeting transcripts - anything you need summarized and documented!",
    height=250,
    key="raw_text_area",
)

# Enhanced processing button and logic
if st.button("🚀 Generate & Create Google Doc"):
    # Enhanced validation with better error styling
    missing = []
    if not gemini_key:
        missing.append("🔑 Gemini API Key")
    if sa_file is None:
        missing.append("📄 Service Account JSON")
    if not shared_folder_id and not user_gmail:
        missing.append("✉️ Gmail Address or 📂 Shared Folder ID")
    if not raw_text.strip():
        missing.append("✍️ Content to summarize")

    if missing:
        st.markdown(
            f"""
            <div class="stAlert" style="border-left-color: #ff4757 !important;">
                <h4 style="color: #ff4757; margin-top: 0;">⚠️ Missing Required Information</h4>
                <p>Please provide the following:</p>
                <ul style="margin: 0.5rem 0;">
                    {''.join([f'<li>{item}</li>' for item in missing])}
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Configure Gemini
        genai.configure(api_key=gemini_key.strip())

        # Save service account JSON to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
            tmp.write(sa_file.getbuffer())
            tmp_path = tmp.name

        # Build Google API clients
        SCOPES = [
            "https://www.googleapis.com/auth/documents",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
        ]

        try:
            creds = service_account.Credentials.from_service_account_file(tmp_path, scopes=SCOPES)
            docs_service = build("docs", "v1", credentials=creds)
            drive_service = build("drive", "v3", credentials=creds)
        except Exception as e:
            st.markdown(
                f"""
                <div class="stAlert" style="border-left-color: #ff4757 !important;">
                    <h4 style="color: #ff4757; margin-top: 0;">❌ Authentication Failed</h4>
                    <p>Failed to load Service Account credentials: {e}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.stop()

        # AI Summarization with enhanced loading
        with st.spinner("🤖 AI is analyzing and summarizing your content..."):
            try:
                model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
                response = model.generate_content(f"Summarize this:\n{raw_text}")
                summary = response.text.strip()
            except Exception as e:
                st.markdown(
                    f"""
                    <div class="stAlert" style="border-left-color: #ff4757 !important;">
                        <h4 style="color: #ff4757; margin-top: 0;">❌ Summarization Failed</h4>
                        <p>Gemini AI encountered an error: {e}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.stop()

        st.markdown(
            """
            <div class="success-message">
                <h4 style="color: var(--secondary-neon); margin-top: 0;">✅ Summarization Complete!</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="summary-display">
                <h3>📝 Gemini Summary</h3>
                {summary}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Create Google Doc & write summary
        with st.spinner("📝 Creating Google Doc and writing summary..."):
            try:
                if shared_folder_id.strip():
                    # Create doc inside shared folder via Drive API
                    file_metadata = {
                        "name": doc_title or "AI Summary",
                        "mimeType": "application/vnd.google-apps.document",
                        "parents": [shared_folder_id.strip()],
                    }
                    created = drive_service.files().create(body=file_metadata, fields="id").execute()
                    doc_id = created["id"]

                    # Insert summary via Docs API
                    docs_service.documents().batchUpdate(
                        documentId=doc_id,
                        body={
                            "requests": [
                                {"insertText": {"location": {"index": 1}, "text": summary}}
                            ]
                        },
                    ).execute()

                else:
                    # Create a standalone doc via Docs API
                    doc_body = {"title": doc_title or "AI Summary"}
                    doc = docs_service.documents().create(body=doc_body).execute()
                    doc_id = doc["documentId"]

                    # Insert summary at the top
                    docs_service.documents().batchUpdate(
                        documentId=doc_id,
                        body={
                            "requests": [
                                {"insertText": {"location": {"index": 1}, "text": summary}}
                            ]
                        },
                    ).execute()

                    # Attempt to share via Drive API
                    try:
                        drive_service.permissions().create(
                            fileId=doc_id,
                            body={
                                "type": "user",
                                "role": "writer",
                                "emailAddress": user_gmail.strip(),
                            },
                            fields="id",
                        ).execute()
                    except HttpError as share_err:
                        if share_err.status_code == 403 and "sharingRateLimitExceeded" in str(share_err):
                            st.markdown(
                                f"""
                                <div class="stAlert" style="border-left-color: #feca57 !important;">
                                    <h4 style="color: #feca57; margin-top: 0;">⚠️ Sharing Rate Limit Reached</h4>
                                    <p>Doc was created, but auto-sharing failed. Please manually share it:</p>
                                    <p><a href="https://docs.google.com/document/d/{doc_id}" target="_blank">Open your new Doc →</a></p>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        else:
                            raise

            except HttpError as err:
                st.markdown(
                    f"""
                    <div class="stAlert" style="border-left-color: #ff4757 !important;">
                        <h4 style="color: #ff4757; margin-top: 0;">❌ Google API Error</h4>
                        <p>Error while creating/sharing Doc: {err}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.stop()
            except Exception as e:
                st.markdown(
                    f"""
                    <div class="stAlert" style="border-left-color: #ff4757 !important;">
                        <h4 style="color: #ff4757; margin-top: 0;">❌ Unexpected Error</h4>
                        <p>Error while creating/sharing Doc: {e}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.stop()

        doc_url = f"https://docs.google.com/document/d/{doc_id}"
        st.markdown(
            f"""
            <div class="success-message">
                <h4 style="color: var(--secondary-neon); margin-top: 0;">✅ Google Doc Created!</h4>
                <p><a href="{doc_url}" target="_blank">🔗 Open your new Doc →</a></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Cleanup temporary JSON file
        try:
            os.remove(tmp_path)
        except OSError:
            pass