from src.pdf_reader import extract_text_from_pdf
from src.text_cleaner import clean_text
from src.skill_extractor import extract_skills
from src.recommender import recommend_careers
from src.resume_analyzer import analyze_resume
from src.career_predictor import predict_career

resume_path = "data/resumes/Resume-Sample-1-Software-Engineer.pdf"

text = extract_text_from_pdf(resume_path)

cleaned_text = clean_text(text)

skills = extract_skills(
    cleaned_text,
    "data/skills/skills.csv"
)

print("\nDetected Skills:\n")

for skill in skills:
    print("-", skill)

print("\nCareer Recommendations:\n")

recommendations = recommend_careers(
    skills,
    "data/jobs/careers.csv"
)

for career, score in recommendations:
    print(f"{career}: {score}%")

best_career, score, missing_skills = analyze_resume(
    skills,
    "data/jobs/careers.csv"
)

print("\nBest Career Match:")
print(best_career)

print("\nResume Score:")
print(f"{score}/100")

print("\nMissing Skills:")

if len(missing_skills) == 0:
    print("None")
else:
    for skill in missing_skills:
        print("-", skill)

predicted_career = predict_career(skills)

print("\nML Predicted Career:")
print(predicted_career)