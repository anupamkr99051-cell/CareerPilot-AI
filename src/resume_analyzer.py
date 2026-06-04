import pandas as pd

def analyze_resume(user_skills, career_file):

    careers = pd.read_csv(career_file)

    best_career = None
    best_score = 0
    missing_skills = []

    for _, row in careers.iterrows():

        career = row["career"]

        career_skills = row["skills"].split(",")

        matched_skills = list(
            set(user_skills).intersection(
                set(career_skills)
            )
        )

        score = round(
            (len(matched_skills) / len(career_skills)) * 100,
            2
        )

        if score > best_score:

            best_score = score

            best_career = career

            missing_skills = list(
                set(career_skills) - set(user_skills)
            )

    return best_career, best_score, missing_skills