import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.pdf_reader import extract_text_from_pdf
from src.text_cleaner import clean_text
from src.skill_extractor import extract_skills
from src.recommender import recommend_careers
from src.resume_analyzer import analyze_resume
from src.career_predictor import predict_career
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AI Career Recommendation System",
    page_icon="🚀",
    layout="wide"
)
st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

[data-testid="stMetric"] {
    background-color:#1e293b;
    padding:20px;
    border-radius:15px;
    border:1px solid #334155;
}

div[data-testid="stMetric"]:hover {
    border:1px solid #3b82f6;
}

div[data-testid="column"] > div {
    transition: 0.3s;
}

div[data-testid="column"] > div:hover {
    transform: translateY(-5px);
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

div[data-testid="column"] > div {
    transition: all 0.3s ease;
}

div[data-testid="column"] > div:hover {
    transform: translateY(-8px);
}

.dashboard-card {
    background: linear-gradient(135deg,#1e293b,#0f172a);
    padding:25px;
    border-radius:18px;
    text-align:center;
    border:1px solid #334155;
    box-shadow:0 4px 20px rgba(0,0,0,0.3);
}

.dashboard-card h3{
    color:#94a3b8;
    margin-bottom:10px;
}

.dashboard-card h1{
    color:white;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.title("🚀 CareerPilot AI")

    st.markdown("---")

    st.success("📄 Resume Analysis")

    st.success("🎯 Career Prediction")

    st.success("📊 ATS Analysis")

    st.success("📚 Learning Roadmap")

    st.success("💼 Internship Guidance")

    st.markdown("---")

    st.caption("Version 3.0")

# =====================================
# MAIN TITLE
# =====================================

st.markdown("""
<div style="
padding:40px;
border-radius:20px;
background: linear-gradient(
135deg,
#2563eb,
#7c3aed
);
color:white;
text-align:center;
margin-bottom:30px;
">

<h1>🚀 CareerPilot AI</h1>

<h3>
Discover Careers, Improve Your Resume,
Find Internships & Build Your Future
</h3>

<p>
Upload your resume and get AI-powered
career guidance instantly.
</p>

</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

# =====================================
# PROCESS RESUME
# =====================================

if uploaded_file is not None:

    temp_path = "temp_resume.pdf"

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract Text
    text = extract_text_from_pdf(temp_path)

    cleaned_text = clean_text(text)

    # Resume Preview
    with st.expander("📄 Resume Preview"):
        st.write(text[:2000])

    # Extract Skills
    skills = extract_skills(
        cleaned_text,
        "data/skills/skills.csv"
    )

    # =====================================
# DETECTED SKILLS
# =====================================

    st.subheader("🛠 Detected Skills")

    skill_cols = st.columns(4)

    for i, skill in enumerate(skills):
        with skill_cols[i % 4]:
          
          st.success(skill.title())

        # =====================================
    # CAREER RECOMMENDATIONS
    # =====================================

    recommendations = recommend_careers(
    skills,
    "data/jobs/careers.csv"
)

    st.subheader("🎯 Career Recommendations")

    for career, score in recommendations:
        
        st.markdown(f"""
<div style="
    background:#1e293b;
    padding:15px;
    border-radius:12px;
    border:1px solid #334155;
    margin-bottom:10px;
">
    <h4 style="margin:0;color:white;">
        🎯 {career}
    </h4>
</div>
""", unsafe_allow_html=True)
        
        st.progress(score / 100)
        
        st.caption(f"{score}% Match")

    # =====================================
    # CHART
    # =====================================

    careers = [c[0] for c in recommendations]
    scores = [c[1] for c in recommendations]

    chart_df = pd.DataFrame({
        "Career": careers,
        "Score": scores
    })

    st.subheader("📊 Career Match Chart")

    fig = px.bar(
    chart_df,
    x="Career",
    y="Score",
    color="Score",
    text="Score",
    title="Career Match Percentage"
)

    fig.update_layout(
    template="plotly_dark",
    height=500
)

    st.plotly_chart(
    fig,
    use_container_width=True
)

    # =====================================
    # RESUME ANALYSIS
    # =====================================

    best_career, resume_score, missing_skills = analyze_resume(
        skills,
        "data/jobs/careers.csv"
    )

    # =====================================
    # DASHBOARD
    # =====================================

    st.subheader("📊 Career Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="dashboard-card">
            <h3>🛠 Skills</h3>
            <h1>{len(skills)}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="dashboard-card">
            <h3>📄 ATS Score</h3>
            <h1>{resume_score}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="dashboard-card">
            <h3>🎯 Career</h3>
            <h4>{best_career}</h4>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="dashboard-card">
            <h3>⚠ Missing</h3>
            <h1>{len(missing_skills)}</h1>
        </div>
        """, unsafe_allow_html=True)

    # =====================================
    # BEST CAREER + SCORE
    # =====================================

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏆 Best Career Match")
        st.success(best_career)

    with col2:
        st.subheader("📈 Resume Score")
        st.metric(
            "Resume Score",
            f"{resume_score}/100"
        )

        st.progress(resume_score / 100)

    # =====================================
    # MISSING SKILLS
    # =====================================

    st.subheader("⚠ Missing Skills")

    if len(missing_skills) == 0:
        st.success("No Missing Skills")

    else:
        
        for skill in missing_skills:
            
            st.warning(skill)


    # =====================================
    # SKILL GAP ANALYSIS
    # =====================================

    st.subheader("📉 Skill Gap Analysis")

    required_skills = len(skills) + len(missing_skills)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Current Skills", len(skills))

    with col2:
        st.metric("Required Skills", required_skills)

    with col3:
        st.metric("Skill Gap", len(missing_skills))

    if len(missing_skills) > 0:
        
        st.warning(
            f"You need {len(missing_skills)} more skills "
            f"to become a stronger {best_career} candidate." 
            )

    else:
        st.success(
            "Your skill profile is highly aligned with this career."
            )
    
    
    
    # =====================================
    # ATS ANALYSIS
    # =====================================

    st.subheader("📄 ATS Analysis")

    ats_score = resume_score

    if ats_score >= 90:
        ats_status = "Excellent"
    elif ats_score >= 75:
        ats_status = "Good"
    elif ats_score >= 60:
        ats_status = "Average"
    else:
        ats_status = "Needs Improvement"

    import plotly.graph_objects as go

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=ats_score,
        title={"text": "ATS Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "green"},
            "steps": [
                {"range": [0, 50], "color": "red"},
                {"range": [50, 75], "color": "orange"},
                {"range": [75, 100], "color": "lightgreen"}
                ]
                }
                ))

    st.plotly_chart(
        gauge,
        use_container_width=True
        )

    st.info(f"ATS Rating: {ats_status}")

    st.subheader("✅ Resume Strengths")

    if len(skills) >= 5:
        st.success("Strong technical skill set detected")

    if resume_score >= 80:
        st.success("Resume matches career requirements well")

    if len(missing_skills) <= 2:
        st.success("Very few missing skills")

    st.subheader("⚠ Improvement Suggestions")

    if len(missing_skills) > 0:
        for skill in missing_skills:
            st.warning(f"Learn {skill}")

    st.warning("Add GitHub profile if not present")
    st.warning("Add measurable project achievements")
    st.warning("Use action verbs in resume descriptions")
    
    # =====================================
    # ML PREDICTION
    # =====================================

    predicted_career = predict_career(skills)
    st.subheader("🧠 AI Resume Summary")

    st.info(
        f"""
    Skills Found: {len(skills)}

    Predicted Career: {predicted_career}

    Resume Score: {resume_score}/100

    Career Match: {best_career}
    """
)

    st.subheader("🤖 ML Predicted Career")

    st.success(predicted_career)

    # =====================================
# CAREER INSIGHTS
# =====================================

    st.subheader("💼 Career Insights")

    career_info = {

    "Software Engineer": {
        "salary": "₹8 - ₹25 LPA",
        "growth": "High Demand",
        "skills": "Java, Spring Boot, Docker, System Design",
        "companies": "Google, Amazon, Microsoft, Flipkart"
    },

    "Data Scientist": {
        "salary": "₹10 - ₹30 LPA",
        "growth": "Very High Demand",
        "skills": "Python, ML, Deep Learning, Statistics",
        "companies": "Google, NVIDIA, Amazon, IBM"
    },

    "Data Analyst": {
        "salary": "₹6 - ₹15 LPA",
        "growth": "High Demand",
        "skills": "SQL, Excel, Power BI, Tableau",
        "companies": "Deloitte, EY, Accenture, KPMG"
    }
}

    if predicted_career in career_info:
        info = career_info[predicted_career]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"💰 Average Salary\n\n{info['salary']}")
            st.info(f"📈 Growth Outlook\n\n{info['growth']}")
            
            with col2:
                st.info(f"🛠 Key Skills\n\n{info['skills']}")
                st.info(f"🏢 Top Recruiters\n\n{info['companies']}")

    st.subheader("📚 Learning Roadmap")

    roadmaps = {
        "Software Engineer": [
            "Advanced Java",
            "Spring Boot",
            "System Design",
            "Docker",
            "Kubernetes"
        ],

        "Data Scientist": [
            "Python",
            "Statistics",
            "Machine Learning",
            "Deep Learning",
            "MLOps"
        ],

        "Data Analyst": [
            "Excel",
            "SQL",
            "Power BI",
            "Tableau",
            "Data Visualization"
        ]
    }

    if predicted_career in roadmaps:

        for item in roadmaps[predicted_career]:
            st.success(f"✅ {item}")

    # =====================================
# RECOMMENDED COURSES
# =====================================

    st.subheader("🎓 Recommended Courses")

    courses = {
        "Software Engineer": [
            ("Java Programming Masterclass",
             "https://www.udemy.com/topic/java/"),
            ("Spring Boot Fundamentals",
              "https://www.udemy.com/topic/spring/"),
            ("Docker & Kubernetes",
               "https://www.udemy.com/topic/docker/")
        ],

        "Data Scientist": [
            ("Python for Data Science",
             "https://www.coursera.org/learn/python"),
            ("Machine Learning",
             "https://www.coursera.org/learn/machine-learning"),
            ("Deep Learning Specialization",
             "https://www.coursera.org/specializations/deep-learning")
        ],

        "Data Analyst": [
            ("Excel for Business",
             "https://www.coursera.org/learn/excel"),
            ("SQL for Data Analysis",
             "https://www.coursera.org/learn/sql-for-data-science"),
            ("Power BI Training",
             "https://learn.microsoft.com/en-us/training/powerplatform/power-bi/")
        ]
    }

    if predicted_career in courses:
        
        for title, link in courses[predicted_career]:
            
            st.link_button(
                f"📖 {title}",
                link
                )

                # =====================================
    # INTERNSHIP RECOMMENDATIONS
    # =====================================

    st.subheader("💼 Recommended Internships")

    internships = {
        "Software Engineer": [
            "Backend Developer Intern",
            "Full Stack Developer Intern",
            "Java Developer Intern",
            "Web Developer Intern",
            "DevOps Intern"
        ],

        "Data Scientist": [
            "Data Science Intern",
            "Machine Learning Intern",
            "AI Research Intern",
            "NLP Intern",
            "Analytics Intern"
        ],

        "Data Analyst": [
            "Data Analyst Intern",
            "Business Analyst Intern",
            "BI Analyst Intern",
            "SQL Analyst Intern",
            "Reporting Analyst Intern"
        ]
    }

    if predicted_career in internships:

        for internship in internships[predicted_career]:

            st.info(f"🚀 {internship}")

    # =====================================
    # PDF REPORT
    # =====================================

    pdf_file = "CareerPilot_Report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "CareerPilot AI - Career Analysis Report",
            styles["Title"]
            )
        )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "<b>Career Prediction</b>",
            styles["Heading2"]
            )
        )

    content.append(
        Paragraph(
            predicted_career,
            styles["Normal"]
            )
        )

    content.append(Spacer(1, 10))

    content.append(
        Paragraph(
            "<b>Best Career Match</b>",
            styles["Heading2"]
            )
        )

    content.append(
        Paragraph(
            best_career,
            styles["Normal"]
            )
        )   

    content.append(Spacer(1, 10))

    content.append(
        Paragraph(
            "<b>ATS Score</b>",
            styles["Heading2"]
            )
        )

    content.append(
        Paragraph(
            f"{resume_score}/100",
            styles["Normal"]
            )
        )

    content.append(Spacer(1, 10))

    content.append(
        Paragraph(
            "<b>Detected Skills</b>",
            styles["Heading2"]
            )
        )

    content.append(
        Paragraph(
            ", ".join(skills),
            styles["Normal"]
            )
        )

    content.append(Spacer(1, 10))

    content.append(
        Paragraph(
            "<b>Missing Skills</b>",
            styles["Heading2"]
            )
        )

    content.append(
        Paragraph(
            ", ".join(missing_skills)
            if missing_skills
            else "No Missing Skills",
            styles["Normal"]
            )
        )
    

    content.append(Spacer(1, 15))

    content.append(
        Paragraph(
            "<b>Recommended Internships</b>",
            styles["Heading2"]
            )
        )

    if predicted_career in internships:

        for internship in internships[predicted_career]:

            content.append(
                Paragraph(
                    f"• {internship}",
                    styles["Normal"]
                    )
                )
    
    doc.build(content)

    with open(pdf_file, "rb") as pdf:

        PDFbyte = pdf.read()

    st.download_button(
        label="📄 Download PDF Report",
        data=PDFbyte,
        file_name="CareerPilot_Report.pdf",
        mime="application/pdf"
    )
# =====================================
# FOOTER
# =====================================

st.markdown("---")

st.caption(
    "Built with Python • Machine Learning • Streamlit"
)