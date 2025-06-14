import pandas as pd
from models import model_loader

def preprocess_data(user_input):
    data = pd.DataFrame([user_input])

    data['content_type_keywords'] = data['content_type_keywords'].apply(lambda x: ' '.join(x))

    tfidf_features = pd.DataFrame(
        model_loader.tfidf.transform(data['content_type_keywords']).toarray(),
        columns=model_loader.tfidf.get_feature_names_out()
    )
    numeric_cols = [
        'session_duration_min', 'avg_video_duration_sec', 'switch_frequency',
        'content_emotion_score', 'repeated_viewing_ratio', 'skipped_intro_ratio',
        '3_day_total_watch_time',  # ✅ Pay attention to this field name
        'short_video_ratio'
    ]
    # numeric_cols = [
    #     'session_duration_min', 'avg_video_duration_sec', 'switch_frequency',
    #     'content_emotion_score', 'repeated_viewing_ratio', 'skipped_intro_ratio',
    #     'three_day_total_watch_time', 'short_video_ratio'
    # ]
    scaled_num = pd.DataFrame(model_loader.scaler.transform(data[numeric_cols]), columns=numeric_cols)

    cat_data = pd.get_dummies(data[['active_period_label', 'saved_to_favorites']], drop_first=True)

    final_input = pd.concat(
        [scaled_num.reset_index(drop=True), cat_data.reset_index(drop=True), tfidf_features.reset_index(drop=True)],
        axis=1
    )

    expected_cols = model_loader.model.get_booster().feature_names
    final_input = final_input.reindex(columns=expected_cols, fill_value=0)

    return final_input
