from pydantic import BaseModel, Field

class UserInput(BaseModel):
    session_duration_min: float
    active_period_label: str
    avg_video_duration_sec: float
    switch_frequency: float
    content_emotion_score: float
    content_type_keywords: list
    repeated_viewing_ratio: float
    skipped_intro_ratio: float
    saved_to_favorites: bool
    three_day_total_watch_time: float = Field(..., alias="3_day_total_watch_time")
    short_video_ratio: float
