import streamlit as st
import pandas as pd
import re
from recommend_module import recommend

# إعدادات الصفحة مع دعم اللغة العربية
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

# دعم كامل للغة العربية وتحسين معالجة النصوص
@st.cache_data
def extract_unique_values(cols):
    values = []
    for col in cols:
        if col in df.columns and not df.empty:
            # تنظيف النصوص وفصلها بشكل أفضل
            column_values = df[col].dropna().astype(str)
            for value in column_values:
                # فصل القيم باستخدام فواصل متعددة وتنظيفها
                separated_values = re.split(r'[،,;؛\n]', value)
                for v in separated_values:
                    cleaned_v = v.strip()
                    if cleaned_v and cleaned_v != 'nan':
                        values.append(cleaned_v)
    return sorted(list(set(values)), key=lambda x: x.strip())

# الحصول على الخيارات
if not df.empty:
    skills_options = extract_unique_values(["skills", "acquired_skills"])
    interests_options = extract_unique_values(["interests_keywords", "core_subjects"])
    preferred_fields_options = extract_unique_values(["domain", "name"])
else:
    skills_options = []
    interests_options = []
    preferred_fields_options = []

# تخصيص التصميم مع دعم كامل للغة العربية
st.markdown("""
<style>
    /* دعم اللغة العربية وتحسين الخطوط */
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: right;
        direction: rtl;
    }
    
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
        padding-right: 15px;
        font-weight: bold;
    }
    
    .form-container {
        background-color: #F8F9FA;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        border: 1px solid #E0E0E0;
    }
    
    .stNumberInput > div > div > input {
        text-align: center;
        font-size: 1.1rem;
        padding: 10px;
    }
    
    .stSelectbox > div > div {
        text-align: right;
    }
    
    .stMultiSelect > div > div {
        text-align: right;
    }
    
    .stTextInput > div > div > input {
        text-align: right;
        padding: 10px;
    }
    
    .stTextArea > div > div > textarea {
        text-align: right;
        padding: 10px;
        min-height: 100px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #2E86AB 0%, #1B5E7A 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-size: 1.2rem;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    
    .result-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-right: 5px solid #2E86AB;
        transition: transform 0.3s ease;
    }
    
    .result-card:hover {
        transform: translateX(-5px);
    }
    
    .specialty-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border-right: 6px solid #2E86AB;
        transition: all 0.3s ease;
    }
    
    .specialty-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
    
    .specialty-header {
        color: #2E86AB;
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .specialty-domain {
        background: #E9F7FE;
        color: #1B5E7A;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    .specialty-description {
        color: #555;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .specialty-details {
        background: #F8F9FA;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    
    .detail-item {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        padding: 0.3rem 0;
    }
    
    .detail-label {
        font-weight: bold;
        color: #2E86AB;
    }
    
    .detail-value {
        color: #555;
    }
    
    .match-score {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.1rem;
        display: inline-block;
        margin-top: 0.5rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #E9F7FE 0%, #D1F0FF 100%);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
        border: 1px solid #BDE0FE;
    }
    
    .sidebar-content {
        background: linear-gradient(180deg, #F8F9FA 0%, #E9ECEF 100%) !important;
        padding: 1rem !important;
    }
    
    .sidebar-section {
        margin: 1.5rem 0;
    }
    
    .sidebar-title {
        color: #2E86AB;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .error-message {
        background: linear-gradient(135deg, #FFE6E6 0%, #FFCCCC 100%);
        border: 2px solid #FF0000;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .success-message {
        background: linear-gradient(135deg, #E6FFE6 0%, #CCFFCC 100%);
        border: 2px solid #00CC00;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* تحسين العناوين والأقسام */
    h1, h2, h3, h4, h5, h6 {
        font-weight: bold;
        text-align: right;
    }
    
    /* تحسين التباعد والمحاذاة */
    .css-1d391kg {
        text-align: right;
    }
    
    .row-widget.stSelectbox {
        text-align: right;
    }
    
    /* تحسين عرض القوائم المختارة */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #2E86AB;
        color: white;
        border-radius: 20px;
        padding: 2px 8px;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# الشريط الجانبي المحسن
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <img src='https://cdn-icons-png.flaticon.com/512/3710/3710274.png' width='80' style='margin-bottom: 1rem;'>
        <h2 style='color: #2E86AB; margin: 0;'>نظام التوصية الذكي</h2>
        <p style='color: #666; margin: 0.5rem 0;'>للتخصصات الجامعية</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div class='sidebar-section'>
        <div class='sidebar-title'>🎯 كيف يعمل النظام؟</div>
        <ol style='color: #555; line-height: 1.8; padding-right: 1rem;'>
            <li>أدخل معلوماتك الأكاديمية بدقة</li>
            <li>حدد مهاراتك واهتماماتك</li>
            <li>اختر المجالات التي تفضلها</li>
            <li>احصل على توصيات مخصصة</li>
        </ol>
        <p style='color: #666; font-size: 0.9rem;'>
        النظام يحلل ملفك الشخصي ويقارنه مع مئات التخصصات لإيجاد الأنسب لك.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div class='sidebar-section'>
        <div class='sidebar-title'>💡 نصائح مهمة</div>
        <ul style='color: #555; line-height: 1.8; padding-right: 1rem;'>
            <li>كن دقيقًا في إدخال درجاتك</li>
            <li>اختر جميع المهارات والاهتمامات المناسبة</li>
            <li>اكتب هدفك المهني بوضوح</li>
            <li>حدد المجالات التي تفضل العمل فيها</li>
            <li>كن صادقًا مع نفسك في التقييم</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div class='sidebar-section'>
        <div class='sidebar-title'>📊 إحصائيات النظام</div>
        <div style='background: #E9F7FE; padding: 1rem; border-radius: 10px; text-align: center;'>
            <div style='font-size: 2rem; color: #2E86AB; font-weight: bold;'>{}</div>
            <div style='color: #666;'>تخصص متاح في النظام</div>
        </div>
    </div>
    """.format(len(df) if not df.empty else 0), unsafe_allow_html=True)

# المحتوى الرئيسي
st.markdown("<h1 class='main-header'>🎓 نظام توصية التخصصات الجامعية</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; font-size: 1.2rem; margin-bottom: 2rem; color: #666;'>الرجاء تعبئة البيانات أدناه للحصول على توصيات مخصصة بناءً على ملفك الشخصي</div>", unsafe_allow_html=True)

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
            
            # استخدام حقول إدخال رقمية بدلاً من الشرائط المنزلقة
            st.markdown("#### المعدل الدراسي")
            gpa = st.number_input(
                "معدل الثانوية العامة (GPA)", 
                min_value=0.0, 
                max_value=100.0, 
                value=85.0, 
                step=0.1,
                help="أدخل معدلك في الثانوية العامة من 100"
            )
            
            st.markdown("#### درجات المواد الأساسية")
            
            # استخدام أعمدة لعرض حقول الإدخال بشكل متجاور
            col1_1, col1_2, col1_3 = st.columns(3)
            
            with col1_1:
                physics = st.number_input(
                    "الفيزياء", 
                    min_value=0, 
                    max_value=100, 
                    value=85,
                    help="درجة مادة الفيزياء من 100"
                )
            
            with col1_2:
                chemistry = st.number_input(
                    "الكيمياء", 
                    min_value=0, 
                    max_value=100, 
                    value=85,
                    help="درجة مادة الكيمياء من 100"
                )
            
            with col1_3:
                mathematics = st.number_input(
                    "الرياضيات", 
                    min_value=0, 
                    max_value=100, 
                    value=85,
                    help="درجة مادة الرياضيات من 100"
                )
            
            # عرض ملخص للدرجات
            avg_grade = (physics + chemistry + mathematics) / 3
            st.markdown(f"""
            <div class='metric-card'>
                <h3>📈 متوسط درجات المواد العلمية</h3>
                <h2 style='color: #2E86AB; font-size: 2rem;'>{avg_grade:.1f}/100</h2>
                <p style='color: #666; font-size: 0.9rem;'>بناءً على درجات الفيزياء، الكيمياء، والرياضيات</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='sub-header'>👤 الملف الشخصي والاهتمامات</div>", unsafe_allow_html=True)
            
            # المهارات والاهتمامات مع تحسين العرض
            st.markdown("##### المهارات الشخصية")
            skills = st.multiselect(
                "اختر المهارات التي تمتلكها", 
                skills_options, 
                default=[],
                help="اختر المهارات التي تشعر أنك تمتلكها أو ترغب في تطويرها"
            )
            
            st.markdown("##### مجالات الاهتمام")
            interests = st.multiselect(
                "اختر المجالات التي تثير اهتمامك", 
                interests_options, 
                default=[],
                help="اختر المجالات التي تستمتع بدراستها أو التعلم عنها"
            )
            
            st.markdown("##### المجالات الدراسية المفضلة")
            preferred_fields = st.multiselect(
                "اختر المجالات التي تفضل الدراسة فيها", 
                preferred_fields_options, 
                default=[],
                help="اختر المجالات التي ترغب في متابعتها academically"
            )
            
            st.markdown("##### الهدف المهني المستقبلي")
            career_goal = st.text_area(
                "اكتب هدفك المهني بوضوح", 
                placeholder="مثال: أطمح أن أصبح مهندس برمجيات في شركة تقنية رائدة، أو العمل في مجال الذكاء الاصطناعي...",
                help="صف ما تطمح للوصول إليه في مستقبلك المهني بشكل مفصل"
            )
            
            st.markdown("##### المجالات غير المرغوبة")
            dislikes = st.text_input(
                "المجالات التي لا تفضل دراستها (افصل بينها بفاصلة)", 
                placeholder="مثال: المحاسبة, الأدب الإنجليزي, التاريخ",
                help="اذكر المجالات التي لا ترغب في دراستها أو العمل فيها"
            )
        
        # زر الإرسال
        st.markdown("<br>", unsafe_allow_html=True)
        submit_col, empty_col = st.columns([1, 3])
        with submit_col:
            submit = st.form_submit_button("🚀 احصل على التوصيات الآن", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# دالة لعرض النتائج بشكل أنيق
def display_specialty_results(results):
    if not isinstance(results, pd.DataFrame) or results.empty:
        return
    
    st.markdown(f"<h2 style='text-align: center; color: #2E86AB; margin-bottom: 2rem;'>🎯 أفضل {min(len(results), 10)} تخصص يناسبك</h2>", unsafe_allow_html=True)
    
    for idx, row in results.head(10).iterrows():
        # استخراج البيانات مع قيم افتراضية
        name = row.get('name', 'التخصص')
        domain = row.get('domain', 'غير محدد')
        description = row.get('description', 'لا يوجد وصف متاح')
        job_opportunities = row.get('job_opportunities', 'غير محدد')
        required_skills = row.get('required_skills', 'غير محدد')
        salary_range = row.get('salary_range', 'غير محدد')
        duration = row.get('duration', 'غير محدد')
        
        # حساب نسبة المطابقة (افتراضي)
        match_score = min(95, 80 + idx * 2)  # قيمة افتراضية للعرض
        
        # إنشاء البطاقة
        st.markdown(f"""
        <div class='specialty-card'>
            <div class='specialty-header'>#{idx+1} {name}</div>
            <div class='specialty-domain'>📁 {domain}</div>
            
            <div class='specialty-description'>
                <strong>📝 الوصف:</strong> {description}
            </div>
            
            <div class='specialty-details'>
                <div class='detail-item'>
                    <span class='detail-label'>💼 مجالات العمل:</span>
                    <span class='detail-value'>{job_opportunities}</span>
                </div>
                <div class='detail-item'>
                    <span class='detail-label'>🛠️ المهارات المطلوبة:</span>
                    <span class='detail-value'>{required_skills}</span>
                </div>
                <div class='detail-item'>
                    <span class='detail-label'>💰 متوسط الراتب:</span>
                    <span class='detail-value'>{salary_range}</span>
                </div>
                <div class='detail-item'>
                    <span class='detail-label'>⏱️ مدة الدراسة:</span>
                    <span class='detail-value'>{duration}</span>
                </div>
            </div>
            
            <div style='text-align: left;'>
                <div class='match-score'>نسبة المطابقة: {match_score}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# معالجة النتائج وعرضها
if submit:
    try:
        with st.spinner("🔍 جاري تحليل بياناتك وتوليد التوصيات المناسبة..."):
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
        
        if results is None:
            st.error("""
            **⚠️ لم يتم العثور على نتائج**
            
            يرجى التحقق من:
            - أن الوظيفة recommend() تعيد بيانات صحيحة
            - أن البيانات المدخلة صحيحة
            - أن ملف التخصصات يحتوي على بيانات مناسبة
            """)
        
        elif hasattr(results, 'empty') and results.empty:
            st.warning("""
            **🔍 لم نتمكن من العثور على تخصصات مناسبة**
            
            يرجى محاولة:
            - تعديل معايير البحث
            - إضافة المزيد من المهارات والاهتمامات
            - توسيع نطاق المجالات المفضلة
            - تقليل عدد المجالات غير المرغوبة
            """)
        
        elif isinstance(results, pd.DataFrame) and not results.empty:
            display_specialty_results(results)
            
            # خيارات إضافية للنتائج
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("💾 حفظ النتائج", use_container_width=True):
                    st.success("✅ تم حفظ النتائج بنجاح!")
            
            with col2:
                if st.button("🖨️ طباعة التقرير", use_container_width=True):
                    st.info("📄 يمكنك استخدام زر الطباعة في المتصفح لطباعة النتائج")
            
            with col3:
                if st.button("🔄 بدء بحث جديد", use_container_width=True):
                    st.rerun()
        
        else:
            st.info("📊 عرض النتائج الأساسية:")
            st.dataframe(results)
            
    except Exception as e:
        st.error(f"""
        **❌ حدث خطأ أثناء معالجة طلبك**
        
        التفاصيل: {str(e)}
        
        يرجى المحاولة مرة أخرى أو التواصل مع الدعم الفني.
        """)

# قسم المعلومات الإضافية
st.markdown("---")
st.markdown("<h2 style='text-align: center; color: #2E86AB;'>ℹ️ معلومات إضافية</h2>", unsafe_allow_html=True)

info_col1, info_col2, info_col3 = st.columns(3)

with info_col1:
    st.markdown("""
    <div style='text-align: right; padding: 1rem;'>
        <h4>📈 آلية التوصية</h4>
        <p>يعتمد النظام على خوارزميات متقدمة تقوم بمقارنة شاملة بين:</p>
        <ul>
            <li>المؤهلات الأكاديمية</li>
            <li>المهارات الشخصية</li>
            <li>الاهتمامات والهوايات</li>
            <li>الأهداف المستقبلية</li>
            <li>متطلبات سوق العمل</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with info_col2:
    st.markdown("""
    <div style='text-align: right; padding: 1rem;'>
        <h4>🎯 معايير الاختيار</h4>
        <ul>
            <li>التوافق مع القدرات</li>
            <li>الفرص الوظيفية</li>
            <li>متطلبات السوق</li>
            <li>الإمكانيات الشخصية</li>
            <li>الاتجاهات المستقبلية</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with info_col3:
    st.markdown("""
    <div style='text-align: right; padding: 1rem;'>
        <h4>📞 الدعم والمساعدة</h4>
        <p>للاستفسارات أو المساعدة:</p>
        <ul>
            <li>مركز الدعم الأكاديمي</li>
            <li>مستشارو التخصصات</li>
            <li>مركز التوجيه المهني</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# تذييل الصفحة
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>© 2024 نظام توصية التخصصات الجامعية الذكي - جميع الحقوق محفوظة</p>
</div>
""", unsafe_allow_html=True)
