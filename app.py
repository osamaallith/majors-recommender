import streamlit as st
from recommend_module import recommend

st.set_page_config(page_title="توصية التخصصات", layout="wide")
st.title("نظام توصية التخصصات الجامعية")

with st.form("profile_form"):
    about = st.text_area("اكتب عن نفسك:")
    skills = st.text_input("المهارات (افصل بين المهارات بفاصلة)").split(",")
    interests = st.text_input("الاهتمامات (افصل بين الاهتمامات بفاصلة)").split(",")
    career_goal = st.text_input("هدفك المهني")
    preferred_fields = st.text_input("المجالات المفضلة").split(",")
    dislikes = st.text_input("ما لا تحبه").split(",")
    gpa = st.number_input("معدل الثانوية (GPA)", min_value=0.0, max_value=100.0, value=50.0)
    physics = st.number_input("درجة الفيزياء", min_value=0, max_value=100, value=50)
    chemistry = st.number_input("درجة الكيمياء", min_value=0, max_value=100, value=50)
    mathematics = st.number_input("درجة الرياضيات", min_value=0, max_value=100, value=50)
    submit = st.form_submit_button("احصل على التوصيات")

if submit:
    profile = {
        "about": about,
        "skills": [s.strip() for s in skills if s.strip()],
        "interests": [i.strip() for i in interests if i.strip()],
        "career_goal": career_goal,
        "preferred_fields": [p.strip() for p in preferred_fields if p.strip()],
        "dislikes": [d.strip() for d in dislikes if d.strip()],
        "gpa": gpa,
        "grades": {"physics": physics, "chemistry": chemistry, "mathematics": mathematics}
    }
    results = recommend(profile)
    st.subheader("أفضل التخصصات لك")
    st.dataframe(results)
