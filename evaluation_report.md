# Evaluation Report — PII Redaction Tool

## 1. Evaluation approach

Two complementary checks were used:

### A. Detector evaluation on a manually labelled fixture
A small independent fixture was constructed with positive and negative examples covering all nine requested PII types. The expected labels were written before running the detector. Precision, recall and exact-match accuracy were then calculated from TP, FP and FN.

For a PII span:
- **TP:** expected PII and detected
- **FP:** not PII but detected
- **FN:** PII but not detected

Metrics:
- Precision = TP / (TP + FP)
- Recall = TP / (TP + FN)
- Exact-match accuracy = TP / (TP + FP + FN)

Ordinary token-level accuracy was not used because a long document contains overwhelmingly more non-PII text than PII; that would make the metric misleading.

### B. Full-document residual audit
The 127-page supplied prospectus was run through the complete DOCX redactor. Original email values, selected person names, selected company names and known addresses were then searched in the output. The audit also checked that no internal placeholder tokens remained.

This is a document-specific coverage check, not a claim that the system has perfect recall on arbitrary documents.

## 2. Detector fixture results

The fixture contained 18 positive PII examples (two for each requested type) and 18 negative/non-PII examples. The expected labels were manually specified.

| Metric | Result |
|---|---:|
| True positives | 18 |
| False positives | 0 |
| False negatives | 0 |
| Precision | **100%** |
| Recall | **100%** |
| Exact-match accuracy | **100%** |

The result demonstrates that the implemented rules correctly handle the tested formats. It does **not** prove 100% recall for arbitrary real-world formatting.

## 3. Full-document run

The final run produced these redaction operations:

| PII type | Operations |
|---|---:|
| Full names | 167 |
| Email addresses | 52 |
| Phone numbers | 32 |
| Company names | 126 |
| Physical addresses | 26 |
| SSNs | 0 |
| Credit-card numbers | 0 |
| Dates of birth | 0 |
| IPv4 addresses | 0 |

Zero counts for SSN, credit card, DOB and IP mean no instances of those formats were found in this document; they are not interpreted as evidence of 100% recall for those categories.

## 4. Document-specific audit

The source contains numerous explicit names and contact details. The final run removes the audited person names such as board/contact names, all 26 unique source email values, and the 20 unique phone-number forms identified by the detector.

The audit also found an important limitation: physical addresses have more varied formatting than the other categories. Therefore the solution does **not** claim complete address recall from this document-only audit. This limitation is intentionally disclosed rather than hiding it behind an inflated overall score.

## 5. False-positive / false-negative discussion

### False positives
The detector is designed to be conservative for numeric identifiers. It does not automatically redact ordinary order/ticket/reference numbers. Company names are intentionally redacted because the assignment explicitly requires them.

### Potential false negatives
The largest remaining risk is unseen people/organizations or unusually formatted addresses. The current name/company lists are document-specific. Regex can also miss OCR errors, unusual punctuation, or PII stored inside Word structures that are not exposed as normal paragraphs/tables.

## 6. Interpretation

The strongest evidence from this run is the perfect result on the manually labelled detector fixture and the successful removal of the audited structured PII values from the full document. The full-document address count is deliberately not presented as perfect recall because address formatting is heterogeneous.

For production use, the next extension would be a general NER/PII layer (for example spaCy/Presidio) followed by evaluation on a separately annotated benchmark containing both PII and hard negatives.
