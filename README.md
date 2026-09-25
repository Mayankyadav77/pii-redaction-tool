# PII Redaction Tool

## Overview
This solution redacts the requested PII categories from the supplied 127-page Red Herring Prospectus DOCX and writes a new DOCX. The assignment asks for company names to be treated as sensitive, so company/organization names are also replaced.

## Approach
The implementation is hybrid:

1. **Regex detectors** for email addresses, Indian phone numbers, SSNs, credit-card numbers, DOBs, and IPv4 addresses.
2. **Document-specific entity dictionaries** for people, organizations, and high-confidence physical addresses found in the supplied prospectus. This improves precision for a document whose person/company names are highly structured, but it is not a general-purpose NER system.
3. **Deterministic replacement mapping** so repeated occurrences of the same original value receive the same synthetic replacement.
4. **Overlap handling** gives structured PII (email/phone/etc.) priority over address/company/name matches.
5. DOCX paragraphs, tables, headers and footers are processed. Table cells are de-duplicated to avoid processing merged cells twice.

## Replacement examples
- Person -> `John Carter`
- Email -> `person001@example.com`
- Phone -> `+91 90000 10001`
- Company -> `Example Company 01 Private Limited`
- Address -> `101, Example Road, Pune – 411 101, Maharashtra, India`
- SSN -> `999-99-1001`
- Credit card -> `4111 1111 1111 1001`
- DOB -> `15 August 1988`
- IPv4 -> `192.0.2.11`

## Deliberate choices
- The assignment explicitly requests company-name redaction, so organizations are redacted even though not every company name is personal data in a legal/privacy sense.
- Generic order/ticket/reference numbers are not automatically treated as PII. This avoids false positives.
- Ordinary dates are not redacted; a date is treated as DOB only when it is explicitly introduced as DOB/date of birth.

## Tradeoffs
The supplied prospectus is a highly structured financial document rather than a typical ticket log. The person/company/address dictionaries therefore improve precision on this document but create a document-specific dependency. A production system for arbitrary documents should add a general NER/PII engine such as spaCy/Presidio and a separately annotated benchmark.

Address detection is intentionally conservative. Some unusual address layouts or text embedded in Word drawing/text-box structures may require XML-level handling. Character-level formatting inside paragraphs can also be simplified because the implementation rewrites paragraph text through the first run.

## Run
```bash
python pii_redaction.py "Red Herring Prospectus.docx" "redacted_output.docx"
```

## Validation
The evaluation report contains both a small manually labelled detector test fixture and a full-document residual-value audit. The detector fixture is used for precision/recall/accuracy; the document audit is reported separately so that document-specific dictionary coverage is not presented as a general benchmark.
