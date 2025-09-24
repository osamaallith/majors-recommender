import streamlit as st
import pandas as pd
from recommend_module import recommend

# إعدادات الصفحة
st.set_page_config(
    page_title="نظام توصية التخصصات الجامعية",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تحميل بيانات التخصصات
@st.cache_data
def load_data():
    try:
        return pd.read_csv("majors.csv")
    except FileNotFoundError:
        st.error("⚠️ ملف majors.csv غير موجود. يرجى التأكد من وجود الملف في المسار الصحيح.")
        return pd.DataFrame()

df = load_data()

# استخراج القيم الفريدة من الأعمدة النصية لعمل اقتراحات
@st.cache_data
def extract_unique_list(cols):
    values = []
    for col in cols:
        if col in df.columns and not df.empty:
            values.extend(df[col].dropna().astype(str).str.split(",").sum())
    return sorted(list(set([v.strip() for v in values if v.strip()])))

# الحصول على الخيارات فقط إذا كان DataFrame غير فارغ
if not df.empty:
    skills_options = extract_unique_list(["skills","acquired_skills"])
    interests_options = extract_unique_list(["interests_keywords","core_subjects"])
    preferred_fields_options = extract_unique_list(["domain","name"])
else:
    skills_options = []
    interests_options = []
    preferred_fields_options = []

# تخصيص التصميم باستخدام CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2E86AB;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-right: 5px solid #2E86AB;
        padding-right: 10px;
    }
    .form-container {
        background-color: #F8F9FA;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #2E86AB;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-size: 1.1rem;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1B5E7A;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .result-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-right: 4px solid #2E86AB;
    }
    .metric-card {
        background-color: #E9F7FE;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
    }
    .sidebar .sidebar-content {
        background-color: #F8F9FA;
    }
    .error-message {
        background-color: #FFE6E6;
        border: 1px solid #FF0000;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# الشريط الجانبي
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3710/3710274.png", width=100)
    st.markdown("<h2 style='text-align: center; color: #2E86AB;'>نظام التوصية الذكي</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    **كيف يعمل النظام؟**
    
    1. أدخل معلوماتك الأكاديمية
    2. حدد مهاراتك واهتماماتك
    3. اختر المجالات التي تفضلها
    4. احصل على توصيات مخصصة
    
    النظام يحلل ملفك الشخصي ويقارنه مع مئات التخصصات لإيجاد الأنسب لك.
    """)
    
    st.markdown("---")
    st.markdown("""
    **نصائح للحصول على أفضل النتائج:**
    - كن دقيقًا في إدخال درجاتك
    - اختر جميع المهارات والاهتمامات المناسبة
    - اكتب هدفك المهني بوضوح
    """)

# المحتوى الرئيسي
st.markdown("<h1 class='main-header'>🎓 نظام توصية التخصصات الجامعية</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; font-size: 1.2rem; margin-bottom: 2rem;'>الرجاء تعبئة البيانات أدناه للحصول على توصيات مخصصة بناءً على ملفك الشخصي</div>", unsafe_allow_html=True)

# تحقق من وجود البيانات
if df.empty:
    st.error("""
    ⚠️ **لا توجد بيانات للتخصصات متاحة حالياً**
    
    يرجى التأكد من:
    1. وجود ملف majors.csv في المجلد الصحيح
    2. أن الملف يحتوي على البيانات المطلوبة
    3. أن الملف بصيغة CSV صحيحة
    """)
    st.stop()

# نموذج إدخال البيانات
with st.container():
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    
    with st.form("profile_form"):
        # الأقسام الرئيسية للنموذج
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='sub-header'>📊 المعلومات الأكاديمية</div>", unsafe_allow_html=True)
            
            # استخدام أعمدة داخلية لتحسين التخطيط
            gpa_col, empty_col = st.columns([3, 1])
            with gpa_col:
                gpa = st.slider("معدل الثانوية (GPA)", min_value=0.0, max_value=100.0, value=75.0, step=0.5, help="أدخل معدلك في الثانوية العامة")
            
            # درجات المواد
            st.markdown("#### درجات المواد الأساسية")
            physics = st.slider("الفيزياء", min_value=0, max_value=100, value=75)
            chemistry = st.slider("الكيمياء", min_value=0, max_value=100, value=75)
            mathematics = st.slider("الرياضيات", min_value=0, max_value=100, value=75)
            
            # عرض ملخص للدرجات
            avg_grade = (physics + chemistry + mathematics) / 3
            st.markdown(f"<div class='metric-card'><h3>متوسط درجات المواد</h3><h2>{avg_grade:.1f}/100</h2></div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='sub-header'>👤 الملف الشخصي</div>", unsafe_allow_html=True)
            
            # المهارات والاهتمامات
            skills = st.multiselect("المهارات التي تمتلكها", skills_options, default=[], help="اختر المهارات التي تشعر أنك تمتلكها")
            interests = st.multiselect("مجالات اهتمامك", interests_options, default=[], help="اختر المجالات التي تثير اهتمامك")
            
            # المجالات المفضلة
            preferred_fields = st.multiselect("المجالات التي تفضل الدراسة فيها", preferred_fields_options, default=[], help="اختر المجالات التي تود الدراسة فيها")
            
            # الهدف المهني
            career_goal = st.text_area("هدفك المهني المستقبلي", placeholder="مثال: أريد العمل في مجال تطوير البرمجيات أو الذكاء الاصطناعي...", help="صف ما تطمح للوصول إليه في مستقبلك المهني")
            
            # المجالات غير المرغوبة
            dislikes = st.text_input("المجالات التي لا تفضل دراستها (افصل بينها بفاصلة)", placeholder="مثال: المحاسبة, الأدب", help="اذكر المجالات التي لا ترغب في دراستها")
        
        # زر الإرسال
        submit_col, empty_col = st.columns([1, 3])
        with submit_col:
            submit = st.form_submit_button("🚀 احصل على التوصيات", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# معالجة النتائج وعرضها
if submit:
    try:
        with st.spinner("جاري تحليل بياناتك وتوليد التوصيات المناسبة..."):
            profile = {
                "about": " ".join(skills + interests + [career_goal] + preferred_fields),
                "skills": skills,
                "interests": interests,
                "career_goal": career_goal,
                "preferred_fields": preferred_fields,
                "dislikes": [d.strip() for d in dislikes.split(",") if d.strip()],
                "gpa": gpa,
                "grades": {"physics": physics, "chemistry": chemistry, "mathematics": mathematics}
            }
            
            results = recommend(profile)
        
        # عرض النتائج
        st.markdown("---")
        
        # التحقق من نوع results وعرضها بشكل مناسب
        if results is None:
            st.markdown("""
            <div class='error-message'>
                <h3>⚠️ لم يتم العثور على نتائج</h3>
                <p>الوظيفة recommend() أعادت None. يرجى التحقق من:</p>
                <ul>
                    <li>أن الوظيفة تعيد DataFrame أو قائمة</li>
                    <li>أن البيانات المدخلة صحيحة</li>
                    <li>أن ملف التخصصات يحتوي على بيانات مناسبة</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        elif hasattr(results, 'empty') and results.empty:
            st.warning("""
            **لم نتمكن من العثور على تخصصات مناسبة**
            
            يرجى محاولة:
            - تعديل معايير البحث
            - إضافة المزيد من المهارات والاهتمامات
            - توسيع نطاق المجالات المفضلة
            """)
        
        elif isinstance(results, pd.DataFrame) and not results.empty:
            st.markdown(f"<h2 style='text-align: center; color: #2E86AB;'>🎯 أفضل {len(results)} تخصص يناسب ملفك الشخصي</h2>", unsafe_allow_html=True)
            
            # عرض النتائج في بطاقات
            for idx, row in results.head(10).iterrows():
                # استخدام get() للتعامل مع الأعمدة التي قد لا تكون موجودة
                name = row.get('name', 'التخصص')
                domain = row.get('domain', 'غير محدد')
                description = row.get('description', 'لا يوجد وصف متاح')[:200] + '...' if pd.notna(row.get('description')) else 'لا يوجد وصف متاح'
                job_opportunities = row.get('job_opportunities', 'غير محدد')
                
                with st.container():
                    st.markdown(f"""
                    <div class='result-card'>
                        <h3>{idx+1}. {name}</h3>
                        <p><strong>المجال:</strong> {domain}</p>
                        <p><strong>الوصف:</strong> {description}</p>
                        <p><strong>مجالات العمل:</strong> {job_opportunities}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # خيارات إضافية للنتائج
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📥 حفظ النتائج", use_container_width=True):
                    st.success("تم حفظ النتائج بنجاح!")
            
            with col2:
                if st.button("🖨️ طباعة النتائج", use_container_width=True):
                    st.info("يمكنك استخدام زر الطباعة في المتصفح لطباعة النتائج")
            
            with col3:
                if st.button("🔄 إعادة تعبئة النموذج", use_container_width=True):
                    st.experimental_rerun()
        
        else:
            st.markdown(f"<h2 style='text-align: center; color: #2E86AB;'>🎯 نتائج التوصية</h2>", unsafe_allow_html=True)
            st.write("تم العثور على التوصيات التالية:")
            st.write(results)
            
    except Exception as e:
        st.markdown(f"""
        <div class='error-message'>
            <h3>❌ حدث خطأ أثناء معالجة طلبك</h3>
            <p><strong>تفاصيل الخطأ:</strong> {str(e)}</p>
            <p>يرجى المحاولة مرة أخرى أو التواصل مع الدعم الفني.</p>
        </div>
        """, unsafe_allow_html=True)

# قسم المعلومات الإضافية
st.markdown("---")
st.markdown("<h2 style='text-align: center; color: #2E86AB;'>ℹ️ معلومات إضافية</h2>", unsafe_allow_html=True)

info_col1, info_col2, info_col3 = st.columns(3)

with info_col1:
    st.markdown("""
    <div style='text-align: right;'>
        <h4>📈 كيف يتم حساب التوصيات؟</h4>
        <p>يعتمد النظام على خوارزميات ذكية تقارن بين ملفك الشخصي وخصائص مئات التخصصات الجامعية، مع الأخذ بعين الاعتبار:</p>
        <ul>
            <li>المعدل الدراسي ودرجات المواد</li>
            <li>المهارات والاهتمامات الشخصية</li>
            <li>الأهداف المهنية المستقبلية</li>
            <li>مجالات العمل المتاحة</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with info_col2:
    st.markdown("""
    <div style='text-align: right;'>
        <h4>🎯 نصائح لاختيار التخصص</h4>
        <ul>
            <li>اختر تخصصًا يتوافق مع مهاراتك واهتماماتك</li>
            <li>ابحث عن فرص العمل المتاحة للتخصص</li>
            <li>تأكد من توفر التخصص في الجامعات التي تفضلها</li>
            <li>استشر أصحاب الخبرة في المجال</li>
            <li>فكر في مستقبل المجال واحتياجات سوق العمل</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with info_col3:
    st.markdown("""
    <div style='text-align: right;'>
        <h4>📞 هل تحتاج مساعدة؟</h4>
        <p>إذا كنت بحاجة إلى مساعدة إضافية في اختيار التخصص المناسب، يمكنك:</p>
        <ul>
            <li>التحدث مع مستشار أكاديمي</li>
            <li>زيارة معارض التعليم والجامعات</li>
            <li>التواصل مع خريجي التخصصات التي تهتم بها</li>
            <li>الاطلاع على خطط الدراسة للتبرع المختلفة</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# تذييل الصفحة
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'><p>© 2023 نظام توصية التخصصات الجامعية. جميع الحقوق محفوظة.</p></div>", unsafe_allow_html=True)
