# System Audit Status

## Overall Verdict
FAIL

## UI / UX Audit
- Status: FAIL
- Findings:
  - **No Results Display**: The dashboard shows high-level stats but provides no way to view the results of a specific analysis batch. This is a critical failure.
  - **Misleading UX**: The "Export PDF/CSV" buttons on the main dashboard are non-functional placeholders, which is misleading.
  - **Lack of Transparency**: The AI detection page displays a score but fails to explain what the score means, the model used, or the significant risk of false positives.
  - **No Error State Details**: When an upload or analysis fails, the user is given a generic "failed" message with no actionable information.
- Required Fixes:
  - Implement a results page for each batch, showing a document-by-document breakdown of plagiarism and AI scores.
  - Make export buttons functional and context-specific (i.e., on a batch results page).
  - Add clear, concise explanations to the AI detection interface regarding the model, confidence scores, and limitations.

## Backend & API Audit
- Status: FAIL
- Findings:
  - **No Input Validation**: The `/documents/upload` endpoint does not validate file size, MIME types, or the number of files. This exposes the system to trivial payload flooding attacks.
  - **Insecure Temporary File Handling**: The system writes uploaded files and extracted archive contents to a shared `/tmp` directory without proper sandboxing or resource limits.
  - **Exposed Internal State**: The `/batch/{batch_id}/results` endpoint dumps raw database query results, exposing internal table structures.
  - **No Rate Limiting**: There is no protection against abuse from a single user rapidly submitting analysis requests.
- Required Fixes:
  - Implement strict input validation on the upload endpoint for file size, types (e.g., `application/pdf`), and quantity.
  - Use a secure, isolated directory for temporary file processing and ensure cleanup.
  - Refactor API endpoints to return data through structured, well-defined Pydantic schemas, not raw database objects.
  - Implement rate limiting on all resource-intensive endpoints.

## Plagiarism Detection Audit
- Status: FAIL
- Missing or Weak Features:
  - **Simplistic Similarity Metric**: Plagiarism detection is based *only* on a single cosine similarity score for an entire document's embedding. This is insufficient for academic or enterprise use.
  - **No Highlighted Passages**: The system does not identify *which* parts of a document are similar, making the results unactionable.
  - **No Source Comparison**: The system only compares documents within the same batch. It does not compare against a broader corpus or external sources, severely limiting its utility.
  - **No Score Explanation**: The UI never explains how the "similarity" score is calculated.
- Required Fixes:
  - Implement a chunk-based comparison algorithm. The backend should compare embeddings of smaller text chunks (e.g., paragraphs) to identify specific similar passages.
  - The API response must include the actual text of the matching passages and their location within the source documents.
  - The system must clearly state that plagiarism checks are limited to the uploaded batch of documents.

## AI Detection Audit
- Status: FAIL
- Risks & False Positives:
  - **No Model Disclosure**: The UI does not name the model being used (e.g., `roberta-base-openai-detector`).
  - **No Calibration or Thresholding Explanation**: The system uses a default 0.5 threshold on the model's output without any evidence of calibration. This is known to be unreliable.
  - **High Risk of False Positives**: There are no warnings about the high rate of false positives, especially for text written by non-native English speakers. A binary "AI" or "Human" label is dangerously misleading.
  - **No Mixed-Content Handling**: The system averages AI scores across chunks, which will fail to detect documents that are a mix of human and AI-generated text.
- Required Fixes:
  - Clearly state the name of the AI detection model in the UI.
  - Replace the binary label with a nuanced confidence score (e.g., "Likely AI-Generated," "Possibly AI-Generated") and provide a detailed explanation of what the score means.
  - Add a prominent, non-dismissible warning about the limitations of AI detection and the risk of false positives.
  - The detection logic should be updated to identify and flag individual passages with high AI probability, rather than averaging the score over the entire document.

## Critical Risks (If Deployed)
- **High Potential for False Accusations**: The current AI detection implementation is highly likely to falsely flag human-written text as AI-generated, which could have severe consequences in an academic setting.
- **System Instability**: The lack of input validation and rate limiting makes the backend vulnerable to denial-of-service attacks.
- **Misleading Plagiarism Results**: The plagiarism detection is too simplistic to be reliable, giving a false sense of security.

## Final Recommendation
- **Block deployment**. The system is not fit for purpose in its current state. It requires a significant architectural redesign of its core ML features and security hardening before it can be considered for even limited use.
