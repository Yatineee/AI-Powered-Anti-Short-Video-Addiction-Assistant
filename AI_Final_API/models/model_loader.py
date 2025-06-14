import joblib

model = joblib.load('saved_models/xgboost_best_model.pkl')
scaler = joblib.load('saved_models/scaler.pkl')
tfidf = joblib.load('saved_models/tfidf_vectorizer.pkl')
label_encoder = joblib.load('saved_models/label_encoder.pkl')
