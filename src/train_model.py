import pandas as pd
import joblib

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

data = pd.read_csv("data/jobs/training_data.csv")

X = data["skills"]
y = data["career"]

vectorizer = CountVectorizer()

X_vectorized = vectorizer.fit_transform(X)

model = LogisticRegression(max_iter=1000)

model.fit(X_vectorized, y)

joblib.dump(model, "models/career_model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("Model trained and saved successfully!")