# AI-Powered-Anti-Short-Video-Addiction-Assistant
It's an AI-powered behavioral assistant built to detect and mitigate unconscious short-video addiction. It leverages machine learning and multi-agent systems, developed within the Trae IDE, to classify user behavior, recognize digital overconsumption patterns, and trigger personalized, empathetic interventions.

# Steps To Run This Project
### Step 1:
Download or Clone this Git Repo
### Step 2:
Open the Repo in Terminal or Editor
### Step 3:
cd AI_Final_API <br>
pip install -r requirements.txt <br>
uvicorn main:app --host 0.0.0.0 --port 8001
### Step 4:
cd .. <br>
cd web <br>
cd backend <br>
pip install -r requirements.txt <br>
uvicorn main:app --host 0.0.0.0
### Step 5:
cd .. <br>
cd frontend <br>
pip install -r requirements.txt <br>
node server.js

# Backend 
< FastAPI Python3.8>
### start command:
uvicorn main:app --reload

# Frontend 
< Node.js >
### start command:
node server.js

# AI API 
< FastAPI Python3.12>
### start command:
pip install -r requirements.txt
uvicorn main:app --reload --port 8001

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
