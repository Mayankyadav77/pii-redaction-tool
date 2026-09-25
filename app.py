import streamlit as st
from pathlib import Path
import tempfile
from pii_redaction import redact_docx

st.set_page_config(
    page_title="PII Redaction Tool",
    page_icon="🔒"
)

st.title("PII Redaction Tool")
st.write(
    "Upload a DOCX file to detect and replace supported PII "
    "with synthetic alternatives."
)

uploaded = st.file_uploader(
    "Upload DOCX document",
    type=["docx"]
)

if uploaded is not None and st.button("Redact PII", type="primary"):

    with tempfile.TemporaryDirectory() as tmp:

        input_path = Path(tmp) / "input.docx"
        output_path = Path(tmp) / "redacted_output.docx"

        # Save uploaded document
        input_path.write_bytes(uploaded.getvalue())

        try:
            # redact_docx returns a Redactor object
            redactor = redact_docx(
                str(input_path),
                str(output_path)
            )

            # Get statistics from the Redactor object
            stats = redactor.stats

            st.success("Redaction completed successfully!")

            st.subheader("Redaction Summary")
            st.json(stats)

            # Make sure output file was actually created
            if output_path.exists():

                st.download_button(
                    label="Download redacted DOCX",
                    data=output_path.read_bytes(),
                    file_name="redacted_output.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            else:
                st.error("Redacted output file was not created.")

        except Exception as exc:
            st.error(f"Could not process the document: {exc}")
