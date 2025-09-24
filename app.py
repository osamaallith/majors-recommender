import streamlit as st
import pandas as pd
from recommend_module import recommend

st.set_page_config(page_title="نظام توصية التخصصات", layout="wide")
st.title("نظام توصية التخصصات الجامعية")
st.markdown("<div style='text-align: right'>الرجاء تعبئة البيانات أدناه للحصول على التوصيات.</div>", unsafe_allow_html=True)

# --- تحميل بيانات التخصصات ---
df = pd.read_csv("majors.csv")

# استخراج القيم الفريدة من الأعمدة النصية لعمل اقتراحات
def extract_unique_list(cols):
    values = []
    for col in cols:
        if col in df.columns:
            values.extend(df[col].dropna().astype(str).str.split(",").sum())
    return sorted(list(set([v.strip() for v in values if v.strip()])))

skills_options = extract_unique_list(["skills","acquired_skills"])
interests_options = extract_unique_list(["interests_keywords","core_subjects"])
preferred_fields_options = extract_unique_list(["domain","name"])

with st.form("profile_form"):
    # --- الحقول الرقمية أولاً ---
    gpa = st.number_input("معدل الثانوية (GPA)", min_value=0.0, max_value=100.0, value=50.0)
    physics = st.number_input("درجة الفيزياء", min_value=0, max_value=100, value=50)
    chemistry = st.number_input("درجة الكيمياء", min_value=0, max_value=100, value=50)
    mathematics = st.number_input("درجة الرياضيات", min_value=0, max_value=100, value=50)

    # --- الحقول النصية مع اقتراحات من الملف ---
    skills = st.multiselect("المهارات", skills_options, default=[])
    interests = st.multiselect("الاهتمامات", interests_options, default=[])
    career_goal = st.text_input("هدفك المهني")
    preferred_fields = st.multiselect("المجالات المفضلة", preferred_fields_options, default=[])
    dislikes = st.text_input("ما لا تحبه").split(",")  # عادة هذه قليلة ويمكن كتابتها يدوياً

    submit = st.form_submit_button("احصل على التوصيات")

if submit:
    profile = {
        # about يُملأ تلقائياً من الحقول النصية الأخرى
        "about": " ".join(skills + interests + [career_goal] + preferred_fields),
        "skills": skills,
        "interests": interests,
        "career_goal": career_goal,
        "preferred_fields": preferred_fields,
        "dislikes": [d.strip() for d in dislikes if d.strip()],
        "gpa": gpa,
        "grades": {"physics": physics, "chemistry": chemistry, "mathematics": mathematics}
    }
    results = recommend(profile)
    st.subheader("أفضل التخصصات لك")
    st.dataframe(results)
