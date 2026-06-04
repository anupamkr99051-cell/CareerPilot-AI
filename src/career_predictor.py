import joblib

model = joblib.load("models/career_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

def predict_career(user_skills):

    skill_text = " ".join(user_skills)

    skill_vector = vectorizer.transform([skill_text])

    prediction = model.predict(skill_vector)

    return prediction[0]