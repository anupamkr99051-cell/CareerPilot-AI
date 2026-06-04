import pandas as pd

def load_skills(path):
    skills = pd.read_csv(path)

    return skills["skill"].tolist()