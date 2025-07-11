from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import joblib
from model_utils import predict
from recommender import recommend_content
from daily_emotion_report import generate_daily_emotion_report

# إنشاء تطبيق FastAPI
app = FastAPI()

# إعداد CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # يمكنك تخصيصها حسب الحاجة
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تحميل النموذج والأدوات
model = joblib.load("./models/random_forest_model.pkl")
tfidf = joblib.load("./models/tfidf_vectorizer.pkl")
le = joblib.load("./models/label_encoder.pkl")

# ====== Data Models ======
class TextInput(BaseModel):
    text: str

class DailyPostsInput(BaseModel):
    posts: List[str]

# ====== Endpoints ======

@app.post("/predict")
def predict_emotion_endpoint(data: TextInput):
    emotion = predict(data.text)
    return {"emotion": emotion}

@app.post("/recommend")
def recommend_endpoint(data: TextInput):
    emotion = predict(data.text)
    recommendations = recommend_content(emotion)
    return {
        "emotion": emotion,
        "recommendations": recommendations
    }

@app.post("/daily-report")
def daily_report_api(data: DailyPostsInput):
    report = generate_daily_emotion_report(
        posts=data.posts,
        model=model,
        vectorizer=tfidf,
        label_encoder=le
    )
    return report
