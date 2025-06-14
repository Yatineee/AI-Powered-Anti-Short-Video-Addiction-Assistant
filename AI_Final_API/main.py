from fastapi import FastAPI
from schemas.user_input import UserInput
from utils.preprocessing import preprocess_data
from models import model_loader

app = FastAPI(title="Psychological State Predictor")

@app.post("/predict")
def predict_state(user: UserInput):
    data = preprocess_data(user.dict(by_alias=True))
    # data = preprocess_data(user.dict())
    prediction = model_loader.model.predict(data)
    label = model_loader.label_encoder.inverse_transform(prediction)[0]
    return {"predicted_state": label}
