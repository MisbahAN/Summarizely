import os
import base64
import streamlit as st
import google.generativeai as genai
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ─── 0) Write service account JSON from Base64‐encoded env var ─────────────
SERVICE_ACCOUNT_FILE = "summarizely_sa.json"
if not os.path.exists(SERVICE_ACCOUNT_FILE):
    # Try to read the base64‐encoded string from env
    sa_b64 = os.getenv("SERVICE_ACCOUNT_JSON_B64")
    if sa_b64:
        try:
            decoded = base64.b64decode(sa_b64)
            with open(SERVICE_ACCOUNT_FILE, "wb") as f:
                f.write(decoded)
        except Exception as e:
            st.error(f"❌ Failed to decode/write service account JSON: {e}")
    # If SERVICE_ACCOUNT_JSON_B64 is not set, we’ll catch that below

# ─── 1) Page Configuration (MUST be first) ─────────────────────────────────────
st.set_page_config(
    page_title="Summarizely",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ─── 2) Inject Custom CSS ─────────────────────────────────────────────────────
if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ─── 3) Enhanced Hero Section ───────────────────────────────────────────────
st.markdown(
    """
    <h1 data-text="SUMMARIZELY">SUMMARIZELY</h1>
    <div class="hero-subtitle">
        Your Python-based AI sidekick: Gemini does the heavy lifting,<br>
        then pushes polished summaries into Google Docs with futuristic style.
    </div>
    """,
    unsafe_allow_html=True
)

# ─── 4) Feature Highlights ───────────────────────────────────────────────────
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
    unsafe_allow_html=True
)

# ─── 5) Sidebar Configuration ────────────────────────────────────────────────
st.sidebar.markdown("### ⚙️ Configuration Panel")

# 5.1) Gemini API key input
gemini_key = st.sidebar.text_input(
    "🔑 Gemini API Key",
    type="password",
    help="Enter your Google Gemini API key here for AI summarization.",
    placeholder="Enter your Gemini API key..."
)

# 5.2) Behind-the-scenes authentication note
st.sidebar.markdown(
    """
    **Authentication is managed by our service account—no upload required on your end.**
    """
)

# 5.3) User’s Gmail address (if no shared folder)
user_gmail = st.sidebar.text_input(
    "✉️ Your Gmail Address",
    placeholder="your.email@gmail.com",
    help="Enter your Gmail if you want this document shared directly to you."
)

# 5.4) Optional: Shared Folder ID
shared_folder_id = st.sidebar.text_input(
    "📂 Shared Folder ID (Optional)",
    placeholder="Enter a pre-shared Google Drive folder ID",
    help="If you already have a folder shared to your Gmail, enter its ID here. Docs inside inherit sharing."
)

# 5.5) Document title
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
    """,
    unsafe_allow_html=True
)

# ─── 6) Main Content Area ────────────────────────────────────────────────────
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
    unsafe_allow_html=True
)

raw_text = st.text_area(
    label="",
    placeholder="✨ Paste your content here...\n\nArticles, notes, research, etc.",
    height=250,
    key="raw_text_area"
)

# ─── 7) “Generate & Create” Logic ─────────────────────────────────────────────
if st.button("🚀 Generate & Create Google Doc"):
    # 7.1) Validate required fields
    missing = []
    if not gemini_key:
        missing.append("🔑 Gemini API Key")
    if not shared_folder_id and not user_gmail:
        missing.append("✉️ Gmail Address or 📂 Shared Folder ID")
    if not raw_text.strip():
        missing.append("✍️ Content to summarize")

    if missing:
        st.markdown(
            "<div class='stAlert' style='border-left-color:#ff4757;'>"
            "<h4 style='color:#ff4757; margin-top:0;'>⚠️ Missing Required Information</h4>"
            "<p>Please provide the following:</p>"
            "<ul style='margin:0.5rem 0;'>"
            + "".join(f"<li>{item}</li>" for item in missing) +
            "</ul></div>",
            unsafe_allow_html=True
        )
        st.stop()

    # ─── 7.2) Configure Gemini ─────────────────────────────────────────
    genai.configure(api_key=gemini_key.strip())

    # ─── 7.3) Ensure service account JSON is on disk ────────────────
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        st.markdown(
            "<div class='stAlert' style='border-left-color:#ff4757;'>"
            "<h4 style='color:#ff4757; margin-top:0;'>❌ Service Account Missing</h4>"
            "<p>The file <code>summarizely_sa.json</code> was not found. "
            "Ensure you added the Base64‐encoded secret <code>SERVICE_ACCOUNT_JSON_B64</code> "
            "in Streamlit Cloud Settings → Secrets.</p>"
            "</div>",
            unsafe_allow_html=True
        )
        st.stop()

    # ─── 7.4) Build Google Docs & Drive clients ────────────────────
    SCOPES = [
        "https://www.googleapis.com/auth/documents",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file"
    ]
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        docs_service = build("docs", "v1", credentials=creds)
        drive_service = build("drive", "v3", credentials=creds)
    except Exception as e:
        st.markdown(
            "<div class='stAlert' style='border-left-color:#ff4757;'>"
            "<h4 style='color:#ff4757; margin-top:0;'>❌ Authentication Failed</h4>"
            f"<p>Could not load service account credentials: {e}</p>"
            "</div>",
            unsafe_allow_html=True
        )
        st.stop()

    # ─── 7.5) Generate Tutor-Style Notes via Gemini ────────────
    with st.spinner("🤖 AI is analyzing and summarizing your content..."):
        try:
            prompt = (
                "Please convert the following text into comprehensive, tutor‐style study notes:\n"
                "- Organize under clear headings/sections.\n"
                "- Use bullet points for key concepts and definitions.\n"
                "- Include brief explanations or examples.\n"
                "- Highlight important terms in bold or italics.\n\n"
                "Text:\n\"\"\"\n"
                f"{raw_text}\n"
                "\"\"\"\n"
            )
            model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
            response = model.generate_content(prompt)
            notes = response.text.strip()
        except Exception as e:
            st.markdown(
                "<div class='stAlert' style='border-left-color:#ff4757;'>"
                "<h4 style='color:#ff4757; margin-top:0;'>❌ Summarization Failed</h4>"
                f"<p>Gemini AI encountered an error: {e}</p>"
                "</div>",
                unsafe_allow_html=True
            )
            st.stop()

    st.markdown(
        "<div class='success-message'>"
        "<h4 style='color:var(--secondary-neon); margin-top:0;'>✅ Tutor-Style Notes Ready!</h4>"
        "</div>",
        unsafe_allow_html=True
    )

    # Strip out markdown bold markers (**) so they don't appear literally
    clean_notes = notes.replace("**", "")
    replaced_notes = clean_notes.replace("\n", "<br>")

    st.markdown(
        "<div class='summary-display'>"
        "<h3>📝 Gemini Study Notes</h3>"
        f"{replaced_notes}"
        "</div>",
        unsafe_allow_html=True
    )

    # ─── 7.6) Create Google Doc & insert notes ────────────────────
    with st.spinner("📝 Creating Google Doc and writing notes..."):
        try:
            if shared_folder_id.strip():
                file_metadata = {
                    "name": doc_title or "AI Summary",
                    "mimeType": "application/vnd.google-apps.document",
                    "parents": [shared_folder_id.strip()]
                }
                created = drive_service.files().create(
                    body=file_metadata, fields="id"
                ).execute()
                doc_id = created["id"]

                docs_service.documents().batchUpdate(
                    documentId=doc_id,
                    body={
                        "requests": [
                            {
                                "insertText": {
                                    "location": {"index": 1},
                                    "text": clean_notes
                                }
                            }
                        ]
                    }
                ).execute()
            else:
                doc_body = {"title": doc_title or "AI Summary"}
                doc = docs_service.documents().create(body=doc_body).execute()
                doc_id = doc["documentId"]

                docs_service.documents().batchUpdate(
                    documentId=doc_id,
                    body={
                        "requests": [
                            {
                                "insertText": {
                                    "location": {"index": 1},
                                    "text": clean_notes
                                }
                            }
                        ]
                    }
                ).execute()

                try:
                    drive_service.permissions().create(
                        fileId=doc_id,
                        body={
                            "type": "user",
                            "role": "writer",
                            "emailAddress": user_gmail.strip()
                        },
                        fields="id"
                    ).execute()
                except HttpError as share_err:
                    if share_err.status_code == 403 and "sharingRateLimitExceeded" in str(share_err):
                        st.markdown(
                            "<div class='stAlert' style='border-left-color:#feca57;'>"
                            "<h4 style='color:#feca57; margin-top:0;'>⚠️ Sharing Rate Limit Reached</h4>"
                            "<p>Document was created, but auto‐sharing failed. Please manually share it:</p>"
                            f"<p><a href='https://docs.google.com/document/d/{doc_id}' "
                            "target='_blank'>Open your new Doc →</a></p>"
                            "</div>",
                            unsafe_allow_html=True
                        )
                    else:
                        raise
        except HttpError as err:
            st.markdown(
                "<div class='stAlert' style='border-left-color:#ff4757;'>"
                "<h4 style='color:#ff4757; margin-top:0;'>❌ Google API Error</h4>"
                f"<p>Failed to create/share Doc: {err}</p>"
                "</div>",
                unsafe_allow_html=True
            )
            st.stop()
        except Exception as e:
            st.markdown(
                "<div class='stAlert' style='border-left-color:#ff4757;'>"
                "<h4 style='color:#ff4757; margin-top:0;'>❌ Unexpected Error</h4>"
                f"<p>Failed to create/share Doc: {e}</p>"
                "</div>",
                unsafe_allow_html=True
            )
            st.stop()

    doc_url = f"https://docs.google.com/document/d/{doc_id}"
    st.markdown(
        "<div class='success-message'>"
        "<h4 style='color:var(--secondary-neon); margin-top:0;'>✅ Google Doc Created!</h4>"
        f"<p><a href='{doc_url}' target='_blank'>🔗 Open your new Doc →</a></p>"
        "</div>",
        unsafe_allow_html=True
    )
