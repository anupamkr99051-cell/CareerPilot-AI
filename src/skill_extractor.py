from src.skill_loader import load_skills

def extract_skills(text, skills_file):
    skills_db = load_skills(skills_file)

    found_skills = []

    for skill in skills_db:
        if skill.lower() in text:
            found_skills.append(skill)

    return sorted(list(set(found_skills)))