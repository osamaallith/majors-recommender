import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
from rank_bm25 import BM25Okapi

# ---------- تحميل البيانات ----------
df = pd.read_csv("majors.csv")

# الأعمدة النصية
text_cols = [
    "name","domain","description","core_subjects",
    "interests_keywords","skills","acquired_skills",
    "career_paths","job_sectors","track_requirement"
]
for col in text_cols:
    if col not in df.columns:
        df[col] = ""
df["full_text"] = df[text_cols].fillna("").agg(" ".join, axis=1)

# الأعمدة الرقمية
num_cols = [
    "min_highschool_gpa", "study_duration_years", "automation_risk_score",
    "holy_quran","islamic_education",
    "arabic_language","english_language","mathematics","physics","chemistry","biology"
]
for col in num_cols:
    if col not in df.columns:
        df[col] = 0
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce").fillna(0.0)

# إعداد Embeddings و BM25
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
embeddings = model.encode(df["full_text"].tolist(),
                          show_progress_bar=False,
                          convert_to_numpy=True,
                          normalize_embeddings=True)
tokenized_corpus = [doc.split() for doc in df["full_text"].tolist()]
bm25 = BM25Okapi(tokenized_corpus)

# ---------- دوال مساعدة ----------
def normalize_np(x):
    x = np.array(x, dtype=float)
    mn = x.min()
    mx = x.max()
    return np.zeros_like(x) if mx-mn < 1e-9 else (x-mn)/(mx-mn)*100

# ---------- دالة التوصية ----------
def recommend(profile, top_n=7, alpha=0.6, beta=0.35, gamma=0.1):
    weights = {"about":1.0,"skills":1.5,"interests":1.5,"career_goal":1.7,
               "preferred_fields":1.2,"dislikes":-0.9}

    # استعلامات نصية
    queries, q_weights = [], []
    if profile.get("about"): queries.append(profile["about"]); q_weights.append(weights["about"])
    for s in profile.get("skills", []): queries.append(s); q_weights.append(weights["skills"])
    for it in profile.get("interests", []): queries.append(it); q_weights.append(weights["interests"])
    if profile.get("career_goal"): queries.append(profile["career_goal"]); q_weights.append(weights["career_goal"])
    for pf in profile.get("preferred_fields", []): queries.append(pf); q_weights.append(weights["preferred_fields"])
    for d in profile.get("dislikes", []): queries.append(d); q_weights.append(weights["dislikes"])

    n = len(df)
    if not queries:
        semantic_scores = np.zeros(n)
    else:
        q_embeddings = model.encode(queries, convert_to_numpy=True, normalize_embeddings=True)
        scores_emb = np.zeros(n)
        for qv, w in zip(q_embeddings, q_weights):
            sims = util.cos_sim(qv, embeddings)[0].numpy()
            scores_emb += sims * w
        scores_bm25 = np.zeros(n)
        for q in queries:
            scores_bm25 += bm25.get_scores(q.split())
        semantic_scores = alpha * normalize_np(scores_emb) + (1-alpha)*normalize_np(scores_bm25)

    # حساب الدرجة النهائية
    results = []
    subjects = ["arabic_language","english_language","mathematics","physics","chemistry","biology"]
    default_grade = 50.0
    autom_min, autom_max = df["automation_risk_score"].min(), df["automation_risk_score"].max()
    study_max = df["study_duration_years"].replace(0,np.nan).max()
    study_max = study_max if not np.isnan(study_max) else 1.0

    for i, row in df.iterrows():
        if profile.get("gpa") is not None and profile.get("gpa") < row.get("min_highschool_gpa",0):
            continue
        major_weights = np.array([row.get(sub,0) for sub in subjects])
        user_grades_vec = np.array([profile.get("grades",{}).get(sub,default_grade)/100.0 for sub in subjects])
        grade_score = ((user_grades_vec * major_weights).sum()/major_weights.sum()) if major_weights.sum()>0 else user_grades_vec.mean()
        automation_component = (autom_max - row["automation_risk_score"])/(autom_max-autom_min)*100 if autom_max-autom_min>0 else 50
        duration_component = (1 - row["study_duration_years"]/study_max)*100 if study_max>0 else 50
        numeric_score = gamma*((automation_component+duration_component)/2)
        boost = 0
        for pf in profile.get("preferred_job_sectors", []):
            if pf.lower() in str(row.get("job_sectors","")).lower(): boost += 8
        for pd in profile.get("preferred_domains", []):
            if pd.lower() in str(row.get("domain","")).lower(): boost += 6
        sem_score = float(semantic_scores[i]) if len(semantic_scores)>i else 0
        final_score = (1-beta)*sem_score + beta*(grade_score*100) + numeric_score + boost
        results.append({
            "major_id": row.get("major_id"),
            "name": row.get("name"),
            "domain": row.get("domain"),
            "job_sectors": row.get("job_sectors"),
            "study_duration_years": row.get("study_duration_years"),
            "min_highschool_gpa": row.get("min_highschool_gpa"),
            "automation_risk_score": row.get("automation_risk_score"),
            "score": round(final_score,3),
            "description": row.get("description"),
            "skills_required": row.get("skills")
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]
