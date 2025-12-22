import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. إعدادات الصفحة
st.set_config = st.set_page_config(page_title="Strategic AI Manager", layout="wide")

# 2. تهيئة البيانات والذاكرة بشكل "عام" (Global) لضمان عدم حدوث NameError
if 'db_initialized' not in st.session_state:
    # إنشاء البيانات
    prods = ['Cola 330ml', 'Cola 1.5L', 'Water 500ml', 'Flour 5kg', 'Pasta']
    whs = ['مستودع دبي المركزي', 'مستودع أبوظبي الرئيسي', 'مستودع الشارقة']
    inv = []
    for p in prods:
        for w in whs:
            inv.append({'المستودع': w, 'المنتج': p, 'الرصيد': np.random.randint(50, 4000)})
    
    drivers = ['سعيد محمد', 'أحمد علي', 'جاسم عبدالله', 'خالد إبراهيم', 'محمد حسن']
    cities = ['دبي', 'أبوظبي', 'الشارقة', 'العين', 'الفجيرة']
    orders = []
    for i in range(1, 41):
        orders.append({
            'العميل': f'عميل {i}',
            'الحالة': np.random.choice(['تم التسليم ✅', 'متأخر 🔴', 'في الطريق 🚚']),
            'السائق': np.random.choice(drivers),
            'المدينة': np.random.choice(cities),
            'الأهمية': np.random.choice(['VIP (AAA)', 'High (AA)', 'Normal (A)']),
            'الشاحنة': f'TRK-{100+i}'
        })
    
    st.session_state.df_inv = pd.DataFrame(inv)
    st.session_state.df_orders = pd.DataFrame(orders)
    st.session_state.chat_history = [] 
    st.session_state.db_initialized = True

# تعريف المتغيرات للاستخدام في كل مكان بالكود
df_ord = st.session_state.df_orders
df_inv = st.session_state.df_inv

# --- القائمة الجانبية: محادثة ChatGPT المفتوحة ---
with st.sidebar:
    st.header("👨‍💼 خبير العمليات الذكي")
    st.markdown("---")
    
    # عرض سجل المحادثة
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("تحدث معي بحرية عن أي شيء في المصنع..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            q = prompt.lower()
            
            # منطق تحليل البيانات للرد الذكي
            delayed_list = df_ord[df_ord['الحالة'] == 'متأخر 🔴']
            low_stock_list = df_inv[df_inv['الرصيد'] < 400]

            # 1. تحليل المدن والتأخير (استجابة مفتوحة)
            if any(word in q for word in ["مدن", "مدينة", "تأخير", "وين", "فين"]):
                if not delayed_list.empty:
                    cities_names = delayed_list['المدينة'].unique()
                    response = f"أستاذ طارق، رصدت تأخيرات في المدن التالية: **{', '.join(cities_names)}**. \n\n"
                    response += f"لدينا حالياً {len(delayed_list)} شحنات لم تصل في موعدها. "
                    response += "من وجهة نظري، هذا يتطلب مراجعة فورية مع السائقين في هذه المناطق لتجنب غرامات التأخير."
                else:
                    response = "جميع المدن مغطاة بكفاءة اليوم ولا توجد أي بلاغات تأخير جغرافي."

            # 2. تحليل المخزون
            elif any(word in q for word in ["مخزن", "بضاعة", "نقص", "نواقص"]):
                if not low_stock_list.empty:
                    top_low = low_stock_list.iloc[0]
                    response = f"هناك نقطة قلق في المخازن؛ صنف **{top_low['المنتج']}** في **{top_low['المستودع']}** وصل لمستوى {top_low['الرصيد']} وحدة فقط. \n\n"
                    response += "💡 **اقتراح:** هل نخطط لطلبية توريد عاجلة أم نقوم بمناقلة داخلية من فرع آخر؟"
                else:
                    response = "مستويات المخزون ممتازة ومستقرة تماماً في كافة الفروع."

            # 3. التحية والدردشة العامة
            elif any(word in q for word in ["أهلا", "مرحبا", "هلا", "كيف حالك"]):
                response = "أهلاً بك! أنا أتابع البيانات لحظة بلحظة. بشكل عام، كفاءة الأسطول اليوم جيدة ولكن نحتاج للتركيز على الشحنات المتأخرة. بماذا نفكر الآن؟"

            else:
                response = "أنا معك، أستطيع تحليل (حالة المدن، أداء السائقين، أو توازن المخازن). ناقشني في أي نقطة تراها أولوية الآن."

            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- الواجهة الرئيسية (لوحة القيادة الاستراتيجية) ---
st.markdown("<h1 style='text-align: center;'>🏭 مركز الإدارة والتحليل اللحظي</h1>", unsafe_allow_html=True)

# صف الـ KPIs - (الآن تم تعريف df_ord بالخارج فلن يظهر خطأ)
k1, k2, k3, k4 = st.columns(4)
k1.metric("كفاءة العمليات", "93%")
k2.metric("شاحنات في الطريق 🚚", len(df_ord[df_ord['الحالة'] == 'في الطريق 🚚']))
k3.metric("تأخيرات 🔴", len(df_ord[df_ord['الحالة'] == 'متأخر 🔴']))
k4.metric("رصيد المخازن", f"{df_inv['الرصيد'].sum():,}")

st.markdown("---")
tab1, tab2, tab3 = st.tabs(["🚛 الرقابة على الأسطول", "📦 حالة المستودعات", "📊 الرؤية البيانية"])

with tab1:
    st.subheader("تفاصيل حركة السائقين حسب المدينة")
    st.dataframe(df_ord.sort_values(by='الأهمية'), use_container_width=True)

with tab2:
    st.subheader("مستويات المخزون الحالية")
    st.dataframe(df_inv, use_container_width=True)

with tab3:
    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(px.pie(df_ord, names='الحالة', hole=0.4, title="تحليل حالة الأسطول"), use