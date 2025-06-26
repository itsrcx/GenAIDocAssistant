```mermaid
graph TD
  subgraph Frontend
    A1[Angular 19+ Chat UI] -->|SSE / REST| B1[FastAPI API]
    A2[Flutter Mobile Forms] -->|REST API| B1
  end

  subgraph FastAPI Backend
    B1 --> B2[Cognito Auth]
    B1 --> B3[OpenAI / Bedrock]
    B1 --> B4[Textract OCR]
    B1 --> B5[DynamoDB Form Data]
    B1 --> B6[Polly / Transcribe]
    B1 --> B7[Guardrails + Comprehend Medical]
  end

  subgraph Admin
    A3[Admin Panel]
    A3 -->|Usage Logs| B1
    A3 -->|Moderation Events| B7
  end
