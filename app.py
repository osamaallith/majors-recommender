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
        font-family: 'Segoe UI', Arial, sans-serif;
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
    
    .metric-card {
        background: linear-gradient(135deg, #E9F7FE 0%, #D1F0FF 100%);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
        border: 1px solid #BDE0FE;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #F8F9FA 0%, #E9ECEF 100%);
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
        font-family: 'Segoe UI', Arial, sans-serif;
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

# الشريط الجانبي
with st.sidebar:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3710/3710274.png", width=100)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #2E86AB;'>نظام التوصية الذكي</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    **🎯 كيف يعمل النظام؟**
    
    1. أدخل معلوماتك الأكاديمية بدقة
    2. حدد مهاراتك واهتماماتك
    3. اختر المجالات التي تفضلها
    4. احصل على توصيات مخصصة
    
    النظام يحلل ملفك الشخصي ويقارنه مع مئات التخصصات لإيجاد الأنسب لك.
    """)
    
    st.markdown("---")
    st.markdown("""
    **💡 نصائح للحصول على أفضل النتائج:**
    - كن دقيقًا في إدخال درجاتك
    - اختر جميع المهارات والاهتمامات المناسبة
    - اكتب هدفك المهني بوضوح
    - حدد المجالات التي تفضل العمل فيها
    """)

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
            **🔍 لم نتمكن من العثور على تخصصات مناسبة**
            
            يرجى محاولة:
            - تعديل معايير البحث
            - إضافة المزيد من المهارات والاهتمامات
            - توسيع نطاق المجالات المفضلة
            - تقليل عدد المجالات غير المرغوبة
            """)
        
        elif isinstance(results, pd.DataFrame) and not results.empty:
            st.markdown(f"<h2 style='text-align: center; color: #2E86AB;'>🎯 أفضل {min(len(results), 10)} تخصص يناسب ملفك الشخصي</h2>", unsafe_allow_html=True)
            
            # عرض النتائج في بطاقات
            for idx, row in results.head(10).iterrows():
                # استخدام get() للتعامل مع الأعمدة التي قد لا تكون موجودة
                name = row.get('name', 'التخصص')
                domain = row.get('domain', 'غير محدد')
                description = row.get('description', 'لا يوجد وصف متاح')
                if pd.notna(description) and len(description) > 200:
                    description = description[:200] + '...'
                
                job_opportunities = row.get('job_opportunities', 'غير محدد')
                if pd.notna(job_opportunities) and len(job_opportunities) > 150:
                    job_opportunities = job_opportunities[:150] + '...'
                
                with st.container():
                    st.markdown(f"""
                    <div class='result-card'>
                        <h3>#{idx+1} {name}</h3>
                        <p><strong>🏷️ المجال:</strong> {domain}</p>
                        <p><strong>📝 الوصف:</strong> {description}</p>
                        <p><strong>💼 مجالات العمل:</strong> {job_opportunities}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # خيارات إضافية للنتائج
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("💾 حفظ النتائج", use_container_width=True):
                    st.success("✅ تم حفظ النتائج بنجاح!")
            
            with col2:
                if st.button("🖨️ طباعة النتائج", use_container_width=True):
                    st.info("📄 يمكنك استخدام زر الطباعة في المتصفح لطباعة النتائج")
            
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
    <div style='text-align: right; padding: 1rem;'>
        <h4>📈 كيف يتم حساب التوصيات؟</h4>
        <p>يعتمد النظام على خوارزميات ذكية تقارن بين ملفك الشخصي وخصائص مئات التخصصات الجامعية، مع الأخذ بعين الاعتبار:</p>
        <ul>
            <li>المعدل الدراسي ودرجات المواد العلمية</li>
            <li>المهارات الشخصية والقدرات</li>
            <li>مجالات الاهتمام والهوايات</li>
            <li>الأهداف المهنية المستقبلية</li>
            <li>مجالات العمل المتاحة واحتياجات سوق العمل</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with info_col2:
    st.markdown("""
    <div style='text-align: right; padding: 1rem;'>
        <h4>🎯 نصائح لاختيار التخصص</h4>
        <ul>
            <li>اختر تخصصًا يتوافق مع مهاراتك واهتماماتك</li>
            <li>ابحث عن فرص العمل المتاحة للتخصص</li>
            <li>تأكد من توفر التخصص في الجامعات التي تفضلها</li>
            <li>استشر أصحاب الخبرة في المجال</li>
            <li>فكر في مستقبل المجال واحتياجات سوق العمل</li>
            <li>اختر تخصصًا يمكنك التميز فيه</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with info_col3:
    st.markdown("""
    <div style='text-align: right; padding: 1rem;'>
        <h4>📞 هل تحتاج مساعدة؟</h4>
        <p>إذا كنت بحاجة إلى مساعدة إضافية في اختيار التخصص المناسب، يمكنك:</p>
        <ul>
            <li>التحدث مع مستشار أكاديمي متخصص</li>
            <li>زيارة معارض التعليم والجامعات</li>
            <li>التواصل مع خريجي التخصصات التي تهتم بها</li>
            <li>الاطلاع على خطط الدراسة للتبرع المختلفة</li>
            <li>إجراء اختبارات الميول المهنية</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# تذييل الصفحة
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>© 2024 نظام توصية التخصصات الجامعية الذكي. تم التطوير بدعم من تقنيات الذكاء الاصطناعي.</p>
    <p style='font-size: 0.9rem;'>جميع الحقوق محفوظة | تم تصميم النظام لدعم الطلاب في اختيار التخصص المناسب</p>
</div>
""", unsafe_allow_html=True)
