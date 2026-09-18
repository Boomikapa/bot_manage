import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Load data and train model
data = pd.read_csv("mlalgo/dataset/intents.csv")
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data["text"])
model = LogisticRegression()
model.fit(X, data["intent"])

def classify_intent(text):
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]

def get_image_url(intent):
    images = {
        "greeting": "https://cdn-icons-png.flaticon.com/512/21/21104.png",
        "weather": "https://cdn-icons-png.flaticon.com/512/869/869869.png",
        "sports": "https://cdn-icons-png.flaticon.com/512/616/616554.png",
        "technology": "https://cdn-icons-png.flaticon.com/512/1055/1055687.png"
    }
    return images.get(intent, None)
