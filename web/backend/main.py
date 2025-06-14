from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from openai import OpenAI
from config.middleware import setup_middlewares
from sqlmodel import Session, SQLModel, create_engine
from databases.session import SessionLog
from datetime import datetime

app = FastAPI()
setup_middlewares(app)  # 👉 注册中间件

# === Session Data Schema ===
class SessionData(BaseModel):
    user_id: str
    session_start_time: str
    session_duration_min: float
    active_period_label: str
    avg_video_duration_sec: float
    switch_frequency: float
    content_emotion_score: float
    content_type_keywords: List[str]
    repeated_viewing_ratio: float
    skipped_intro_ratio: float
    saved_to_favorites: bool
    _3_day_total_watch_time: float
    short_video_ratio: float
    self_reported_goal: str
    ai_tone_description: str  # 用户手写的语气偏好描述


# === SQLite Setup ===
engine = create_engine("sqlite:///./sessions.db")
SQLModel.metadata.create_all(engine)

# === Should Intervene Logic ===
def should_intervene(session: SessionData) -> bool:
    # print("🔍 should_intervene result:", should_intervene(session))
    # print("Incoming session:", session.dict())
    # print("should_intervene:", should_intervene(session))

    return (
        session.session_duration_min > 45 and
        session.switch_frequency > 2.0 and
        session.content_emotion_score < -0.3
    )

# === Deepseek Client Setup ===
novita_client = OpenAI(
    base_url="https://api.novita.ai/v3/openai",
    api_key="sk_AAuPB1pBdcAHu85cbXj3w7-dE3KJAEqmuLmYlQMesDM"
)

def call_novita_gpt(goal: str, label: str, tone_desc: str) -> str:
    prompt = (
        f"The user currently feels '{label}' and their self-set goal is: '{goal}'.\n"
        f"They hope you respond in the following style: \"{tone_desc}\".\n"
        "Please provide a one-paragraph piece of advice in this tone that is supportive and emotionally appropriate."
    )

    chat_completion_res = novita_client.chat.completions.create(
        model="deepseek/deepseek-v3-0324",
        messages=[
            {"role": "system", "content": "You are a wellness AI that adapts fully to the user's preferred tone."},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )

    return chat_completion_res.choices[0].message.content


# def call_novita_gpt(goal: str, label: str) -> str:
#     prompt = (
#         f"The user currently feels '{label}' and has the goal: '{goal}'. "
#         "Please generate a warm, comforting message to guide them positively."
#     )
#     chat_completion_res = novita_client.chat.completions.create(
#         model="deepseek/deepseek-v3-0324",
#         messages=[
#             {"role": "system", "content": "You are an empathetic, friendly assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         stream=False
#     )
#     return chat_completion_res.choices[0].message.content

# === Main API Endpoint ===
@app.post("/api/intervene")
async def intervene(session: SessionData):
    print("✅ Received session:", session.dict())

    intervene_flag = should_intervene(session)
    print("🔍 should_intervene result:", intervene_flag)

    predicted_label = "anxious" if intervene_flag else "normal"

    # ✅ 使用自定义语气调用 GPT
    advice = (
        call_novita_gpt(session.self_reported_goal, predicted_label, session.ai_tone_description)
        if intervene_flag
        else "You're doing fine!"
    )

    session_dict = session.dict()
    session_dict["content_type_keywords"] = ",".join(session.content_type_keywords)

    log = SessionLog(
        **session_dict,
        predicted_label=predicted_label,
        intervention_level="medium" if intervene_flag else "normal",
        gpt_response=advice
    )

    with Session(engine) as db:
        db.add(log)
        db.commit()
        print("✅ DB commit complete")

    return {
        "level": "medium" if intervene_flag else "normal",
        "advice_text": advice
    }



