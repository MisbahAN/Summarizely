import os
import streamlit as st
import google.generativeai as genai
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ─── 1) Page Configuration (MUST be first) ─────────────────────────────────────
st.set_page_config(
    page_title="Summarizely",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ─── 2) Inject Custom CSS (style.css must live alongside this script) ─────────────
if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# ─── 3) Enhanced Hero Section ────────────────────────────────────────────────
st.markdown(
    """
    <h1 data-text="SUMMARIZELY">SUMMARIZELY</h1>
    <div class="hero-subtitle">
        Your Python‐based AI sidekick: Gemini does the heavy lifting,<br>
        then pushes polished summaries into Google Docs with futuristic style.
    </div>
    """,
    unsafe_allow_html=True,
)

# ─── 4) Feature Highlights ──────────────────────────────────────────────────
st.markdown(
    """
    <div class="feature-grid">
        <div class="feature-item">
            <h4>🤖 AI‐Powered</h4>
            <p>Advanced Gemini AI for intelligent text summarization</p>
        </div>
        <div class="feature-item">
            <h4>📄 Auto‐Documentation</h4>
            <p>Seamless Google Docs integration with sharing</p>
        </div>
        <div class="feature-item">
            <h4>⚡ Lightning Fast</h4>
            <p>Process and summarize content in seconds</p>
        </div>
        <div class="feature-item">
            <h4>🔒 Secure</h4>
            <p>Your data stays protected with enterprise‐grade security</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─── 5) Enhanced Sidebar Configuration ──────────────────────────────────────
st.sidebar.markdown("### ⚙️ Configuration Panel")

# 5.1) Gemini API key input
gemini_key = st.sidebar.text_input(
    "🔑 Gemini API Key",
    type="password",
    help="Enter your Google Gemini API key here for AI summarization.",
    placeholder="Enter your Gemini API key..."
)

# 5.2) Note: We use a *single* service account (summarizely_sa.json) for everyone.
st.sidebar.markdown(
    """
    ### 📁 Service Account Authentication  
    (Using the developer’s shared service account - no upload needed)
    
    This app uses a pre‐configured service account (`summarizely_sa.json`) stored on the server.  
    All generated Docs will be created under that account.  
    """
)

# 5.3) User’s Gmail address for sharing (if not using a pre‐shared folder)
user_gmail = st.sidebar.text_input(
    "✉️ Your Gmail Address",
    placeholder="your.email@gmail.com",
    help="Enter your Gmail if you want this document shared directly to you."
)

# 5.4) Optional: Shared Folder ID (folder-based auto‐share)
shared_folder_id = st.sidebar.text_input(
    "📂 Shared Folder ID (Optional)",
    placeholder="Enter a pre‐shared Google Drive folder ID",
    help="If you already have a folder shared to your Gmail, enter its ID here. New Docs inside it inherit sharing."
)

# 5.5) Custom document title
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
    - ✉️ Gmail address (if no shared folder)  
    - 📁 Optional: Shared folder ID  
    """
, unsafe_allow_html=True)

# ─── 6) Enhanced Main Content Area ──────────────────────────────────────────
st.markdown(
    """
    <div class="glass-card">
        <h2 style="margin-top: 0;">✍️ Input Your Content</h2>
        <p style="color: var(--text-secondary); margin-bottom: 2rem;">
            Paste or type any text you'd like to summarize. Our AI will process it  
            and create a polished Google Doc.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

raw_text = st.text_area(
    label="",
    placeholder="✨ Paste your content here...  \n\nArticles, notes, research, meeting transcripts—anything you need summarized and documented!",
    height=250,
    key="raw_text_area",
)

# ─── 7) Processing Button & Logic ─────────────────────────────────────────
if st.button("🚀 Generate & Create Google Doc"):
    # 7.1) Validate inputs
    missing = []
    if not gemini_key:
        missing.append("🔑 Gemini API Key")
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
        # ─── 7.2) Configure Gemini ─────────────────────────────────────────
        genai.configure(api_key=gemini_key.strip())

        # ─── 7.3) Load developer’s Service Account JSON ────────────────
        SERVICE_ACCOUNT_FILE = "summarizely_sa.json"
        if not os.path.exists(SERVICE_ACCOUNT_FILE):
            st.markdown(
                f"""
                <div class="stAlert" style="border-left-color: #ff4757 !important;">
                    <h4 style="color: #ff4757; margin-top: 0;">❌ Service Account Missing</h4>
                    <p>The required service account JSON (`{SERVICE_ACCOUNT_FILE}`) was not found on the server.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.stop()

        # ─── 7.4) Build Google Docs & Drive clients ────────────────────
        SCOPES = [
            "https://www.googleapis.com/auth/documents",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
        ]
        try:
            creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES
            )
            docs_service = build("docs", "v1", credentials=creds)
            drive_service = build("drive", "v3", credentials=creds)
        except Exception as e:
            st.markdown(
                f"""
                <div class="stAlert" style="border-left-color: #ff4757 !important;">
                    <h4 style="color: #ff4757; margin-top: 0;">❌ Authentication Failed</h4>
                    <p>Failed to load service account credentials: {e}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.stop()

        # ─── 7.5) AI Summarization ────────────────────────────────────
        with st.spinner("🤖 AI is analyzing and summarizing your content..."):
            try:
                model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
                
                # Instead of a plain “Summarize this,” ask Gemini to create detailed, tutor-style notes:
                prompt = f"""
                    Please convert the following text into comprehensive, tutor‐style study notes. 
                    - Organize the information under clear headings or sections.
                    - Use bullet points for key concepts and definitions.
                    - Include brief explanations or examples where helpful.
                    - Highlight any important terms in bold or italics.

                    Text to be transformed:
                    \"\"\"
                    {raw_text}
                    \"\"\"
                """

                response = model.generate_content(prompt)
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

        # ─── 7.6) Create Google Doc & write summary ────────────────────
        with st.spinner("📝 Creating Google Doc and writing summary..."):
            try:
                if shared_folder_id.strip():
                    # 7.6.1) Create doc inside shared folder (Drive API)
                    file_metadata = {
                        "name": doc_title or "AI Summary",
                        "mimeType": "application/vnd.google-apps.document",
                        "parents": [shared_folder_id.strip()],
                    }
                    created = drive_service.files().create(
                        body=file_metadata, fields="id"
                    ).execute()
                    doc_id = created["id"]

                    # Insert summary via Docs API
                    docs_service.documents().batchUpdate(
                        documentId=doc_id,
                        body={
                            "requests": [
                                {
                                    "insertText": {
                                        "location": {"index": 1},
                                        "text": summary
                                    }
                                }
                            ]
                        },
                    ).execute()
                else:
                    # 7.6.2) Create standalone doc (Docs API)
                    doc_body = {"title": doc_title or "AI Summary"}
                    doc = docs_service.documents().create(body=doc_body).execute()
                    doc_id = doc["documentId"]

                    # Insert summary at index=1
                    docs_service.documents().batchUpdate(
                        documentId=doc_id,
                        body={
                            "requests": [
                                {
                                    "insertText": {
                                        "location": {"index": 1},
                                        "text": summary
                                    }
                                }
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
                                    <p>Document was created, but auto‐sharing failed. Please manually share it:</p>
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

# ─── End of Script ───────────────────────────────────────────────────────────
