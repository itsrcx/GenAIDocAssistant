```mermaid
sequenceDiagram
    participant User
    participant Frontend (Browser)
    participant Cognito
    participant Backend (/callback route)

    User->>Frontend: Clicks "Login"
    Frontend->>Cognito: Redirect to login URL (Hosted UI)
    Cognito->>User: Shows login page (Google / Username / Password)
    User->>Cognito: Submits credentials
    Cognito->>Frontend/Backend: Redirects to /callback?code=XYZ
    Frontend->>Backend: (optional) passes code to backend
    Backend->>Cognito: Exchanges code for tokens
    Cognito->>Backend: Returns id_token, access_token, etc.
