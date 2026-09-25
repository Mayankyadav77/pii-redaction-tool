import streamlit as st
from pathlib import Path
import tempfile
from pii_redaction import redact_docx

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="PII Redaction Tool",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# Custom styling
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    /* Main page */
    .stApp {
        background: #f7f9fc;
    }

    .block-container {
        max-width: 1050px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Hide Streamlit chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Hero */
    .hero {
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        border-radius: 18px;
        padding: 32px 36px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(17, 24, 39, 0.12);
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.16);
        border-radius: 999px;
        padding: 6px 12px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: .3px;
        margin-bottom: 14px;
    }

    .hero h1 {
        margin: 0;
        font-size: 34px;
        line-height: 1.15;
        font-weight: 750;
        letter-spacing: -0.8px;
    }

    .hero p {
        margin: 10px 0 0;
        color: #d1d5db;
        font-size: 15px;
        line-height: 1.6;
        max-width: 720px;
    }

    /* Cards */
    .card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);
    }

    .card-title {
        font-size: 15px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 6px;
    }

    .card-text {
        font-size: 13px;
        color: #6b7280;
        line-height: 1.5;
    }

    /* Upload area */
    [data-testid="stFileUploader"] {
        background: white;
        border: 1px dashed #cbd5e1;
        border-radius: 14px;
        padding: 8px;
    }

    /* Primary button */
    .stButton > button[kind="primary"] {
        width: 100%;
        border-radius: 10px;
        height: 46px;
        font-weight: 700;
        border: 0;
        background: #111827;
    }

    .stButton > button[kind="primary"]:hover {
        background: #374151;
    }

    /* Download button */
    .stDownloadButton > button {
        width: 100%;
        border-radius: 10px;
        height: 46px;
        font-weight: 700;
    }

    /* Metric cards */
    .metric-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        min-height: 95px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.04);
    }

    .metric-value {
        font-size: 25px;
        font-weight: 750;
        color: #111827;
        line-height: 1.1;
    }

    .metric-label {
        font-size: 12px;
        color: #6b7280;
        margin-top: 7px;
    }

    .section-title {
        font-size: 20px;
        font-weight: 750;
        color: #111827;
        margin: 22px 0 12px;
    }

    .success-box {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 12px;
        padding: 15px 17px;
        color: #166534;
        margin: 14px 0;
    }

    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 12px;
        margin-top: 35px;
        padding-top: 20px;
        border-top: 1px solid #e5e7eb;
    }

    /* Remove excess spacing around markdown */
    .small-gap {
        height: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Hero section
# ---------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">🔐 DOCUMENT PRIVACY</div>
        <h1>PII Redaction Tool</h1>
        <p>
            Securely process DOCX documents by detecting supported personally
            identifiable information and replacing it with synthetic alternatives.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Feature cards
# ---------------------------------------------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="card">
            <div class="card-title">📄 DOCX Support</div>
            <div class="card-text">Upload a Word document and generate a redacted copy.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="card">
            <div class="card-title">🛡️ PII Detection</div>
            <div class="card-text">Detect names, emails, phones, addresses and other supported PII.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="card">
            <div class="card-title">✨ Synthetic Replacement</div>
            <div class="card-text">Replace detected values with consistent fake alternatives.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# Upload section
# ---------------------------------------------------------
st.markdown('<div class="section-title">Upload document</div>', unsafe_allow_html=True)

uploaded = st.file_uploader(
    "Choose a DOCX file",
    type=["docx"],
    help="Only .docx files are supported.",
)

if uploaded is not None:
    st.caption(f"Selected file: **{uploaded.name}** · {uploaded.size / 1024 / 1024:.2f} MB")

    if st.button("🔒 Redact PII", type="primary", use_container_width=True):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "input.docx"
            output_path = Path(tmp) / "redacted_output.docx"

            input_path.write_bytes(uploaded.getvalue())

            try:
                with st.spinner("Scanning document and applying redactions..."):
                    redactor = redact_docx(str(input_path), str(output_path))

                # Current redactor returns a Redactor object.
                # Keep a small fallback in case the implementation returns a dict.
                stats = getattr(redactor, "stats", redactor)

                st.markdown(
                    """
                    <div class="success-box">
                        <strong>✓ Redaction completed successfully.</strong><br>
                        Your processed DOCX is ready.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # -------------------------------------------------
                # Results
                # -------------------------------------------------
                st.markdown('<div class="section-title">Redaction summary</div>', unsafe_allow_html=True)

                stat_items = [
                    ("Full names", stats.get("name", 0)),
                    ("Email addresses", stats.get("email", 0)),
                    ("Phone numbers", stats.get("phone", 0)),
                    ("Company names", stats.get("company", 0)),
                    ("Addresses", stats.get("address", 0)),
                    ("SSNs", stats.get("ssn", 0)),
                    ("Credit cards", stats.get("credit_card", 0)),
                    ("Dates of birth", stats.get("dob", 0)),
                    ("IP addresses", stats.get("ip", 0)),
                ]

                # Three rows of three metrics
                for row_start in range(0, len(stat_items), 3):
                    cols = st.columns(3)
                    for col, (label, value) in zip(cols, stat_items[row_start:row_start + 3]):
                        with col:
                            st.markdown(
                                f"""
                                <div class="metric-card">
                                    <div class="metric-value">{value}</div>
                                    <div class="metric-label">{label}</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                    st.markdown('<div class="small-gap"></div>', unsafe_allow_html=True)

                # -------------------------------------------------
                # Download
                # -------------------------------------------------
                st.markdown('<div class="section-title">Download result</div>', unsafe_allow_html=True)

                output_bytes = output_path.read_bytes()

                st.download_button(
                    "⬇️ Download Redacted DOCX",
                    data=output_bytes,
                    file_name="redacted_output.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )

            except Exception as exc:
                st.error(f"Could not process the document: {exc}")

else:
    st.info("Upload a DOCX file above to get started.")

# ---------------------------------------------------------
# Supported PII
# ---------------------------------------------------------
st.markdown('<div class="section-title">Supported PII categories</div>', unsafe_allow_html=True)

supported = [
    "Full names",
    "Email addresses",
    "Phone numbers",
    "Company names",
    "Physical / mailing addresses",
    "SSNs",
    "Credit card numbers",
    "Dates of birth",
    "IPv4 addresses",
]

st.markdown(
    "  ".join([f"`{item}`" for item in supported])
)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown(
    """
    <div class="footer">
        PII Redaction Tool · Built for document privacy processing
    </div>
    """,
    unsafe_allow_html=True,
)
