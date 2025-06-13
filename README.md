# AI-Powered-Anti-Short-Video-Addiction-Assistant
It's an AI-powered behavioral assistant built to detect and mitigate unconscious short-video addiction. It leverages machine learning and multi-agent systems, developed within the Trae IDE, to classify user behavior, recognize digital overconsumption patterns, and trigger personalized, empathetic interventions.

# Backend 
< FastAPI Python >
### start command:
uvicorn main:app --reload

# Frontend 
< Node.js >
### start command:
node server.js

## 🧠 Real-Time Intervention Flow

```mermaid
graph TD
    A[User watches short videos]
    A --> B[Frontend sends behavior data]
    B --> C[Backend receives session data]
    C --> D{Should intervene?}
    D -- No --> X[Return 0]
    D -- Yes --> E[Call AI model to identify state]
    E --> F[Evaluate intervention level]
    F --> G[Return level and message]
    G --> H[Frontend shows reminder card]
```
