import pandas as pd

def recommend_careers(user_skills, career_file):

    careers = pd.read_csv(career_file)

    recommendations = []

    for _, row in careers.iterrows():

        career_name = row["career"]

        career_skills = row["skills"].split(",")

        matched = len(
            set(user_skills).intersection(set(career_skills))
        )

        score = round(
            (matched / len(career_skills)) * 100,
            2
        )

        recommendations.append(
            (career_name, score)
        )

    recommendations.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return recommendations