import streamlit as st
from pathlib import Path
import tempfile
from pii_redaction import redact_docx

st.set_page_config(
    page_title="PII Redaction Tool",
    page_icon="🔒"
)

st.title("PII Redaction Tool")
st.write("Upload a DOCX file to redact supported PII.")

uploaded = st.file_uploader(
    "Upload DOCX document",
    type=["docx"]
)

if uploaded is not None:

    st.success(f"File uploaded: {uploaded.name}")

    if st.button("Redact PII", type="primary"):

        st.write("### Processing started...")

        with tempfile.TemporaryDirectory() as tmp:

            input_path = Path(tmp) / "input.docx"
            output_path = Path(tmp) / "redacted_output.docx"

            st.write("Step 1: Saving uploaded file...")

            input_path.write_bytes(uploaded.getvalue())

            st.write(
                f"Step 2: Input file size: "
                f"{input_path.stat().st_size / (1024 * 1024):.2f} MB"
            )

            try:

                st.write("Step 3: Starting redaction...")

                redactor = redact_docx(
                    str(input_path),
                    str(output_path)
                )

                st.write("Step 4: Redaction function finished.")

                stats = redactor.stats

                st.write("Step 5: Redaction statistics:")
                st.json(stats)

                if output_path.exists():

                    output_size = output_path.stat().st_size

                    st.success(
                        f"Redaction completed! "
                        f"Output size: {output_size / (1024 * 1024):.2f} MB"
                    )

                    with open(output_path, "rb") as f:
                        output_data = f.read()

                    st.download_button(
                        label="Download redacted DOCX",
                        data=output_data,
                        file_name="redacted_output.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

                else:

                    st.error(
                        "Redaction function finished, "
                        "but the output DOCX was not created."
                    )

            except Exception as exc:

                st.error(
                    f"Could not process the document: {type(exc).__name__}: {exc}"
                )

                st.exception(exc)
