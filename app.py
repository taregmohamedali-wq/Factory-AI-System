import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. إعدادات الصفحة
st.set_page_config(page_title="Strategic AI Manager", layout="wide")

# 2. تهيئة البيانات والذاكرة بشكل عام
if 'db_initialized' not in st.session_state:
    # إنشاء البيانات الافتراضية
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

# تعريف المتغيرات لتكون مرئية لكل أجزاء الكود
df_ord = st.session_state.df_orders
df_inv = st.session_state.df_inv

# --- القائمة الجانبية: محرك الدردشة الذكي (ChatGPT Style) ---
with st.sidebar:
    st.header("👨‍💼 خبير العمليات الذكي")
    st.markdown("---")
    
    # عرض سجل المحادثة
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # مدخل الدردشة
    if prompt := st.chat_input("سيد طارق، كيف يمكنني مساعدتك اليوم؟"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            q = prompt.lower()
            delayed_data = df_ord[df_ord['الحالة'] == 'متأخر 🔴']
            low_stock_data = df_inv[df_inv['الرصيد'] < 400]
            
            # منطق الرد الاستشاري المفتوح
            if any(word in q for word in ["أهلا", "مرحبا", "هلا", "كيف حالك"]):
                response = "أهلاً بك! أنا بخير وأراقب العمليات بدقة. بشكل عام، الوضع مستقر ولكن رصدت بعض التأخيرات في الأسطول ونقصاً بسيطاً في المخازن. هل نغوص في التفاصيل؟"
            
            elif any(word in q for word in ["مدن", "مدينة", "وين", "فين", "تأخير"]):
                if not delayed_data.empty:
                    c_names = delayed_data['المدينة'].unique()
                    response = f"بناءً على تحليلي، التأخير يتركز حالياً في: **{', '.join(c_names)}**. لدينا {len(delayed_data)} شحنات متوقفة. أنصح بالتواصل مع السائقين في هذه المناطق فوراً."
                else:
                    response = "أبشرك، لا توجد أي مدينة تعاني من تأخير حالياً، الأسطول يتحرك بانسيابية."

            elif any(word in q for word in ["مخزن", "بضاعة", "نقص", "نواقص"]):
                if not low_stock_data.empty:
                    item = low_stock_data.iloc[0]
                    response = f"هناك تنبيه بخصوص **{item['المنتج']}** في **{item['المستودع']}**، الرصيد منخفض ({item['الرصيد']}). هل أقوم بجدولة أمر تحويل عاجل؟"
                else:
                    response = "المخازن ممتلئة ولا يوجد نقص في أي من المنتجات الأساسية اليوم."

            else:
                response = "فهمت قصدك تماماً. كوني شريكك الاستشاري، أقترح علينا التركيز على تحسين مسارات المدن المتأخرة أو مراجعة مخزون الطوارئ. ما هو قرارك؟"

            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- الواجهة الرئيسية (لوحة التحكم الاستراتيجية) ---
st.markdown("<h1 style='text-align: center;'>🏭 مركز الإدارة والتحليل اللحظي</h1>", unsafe_allow_html=True)

# المؤشرات (KPIs)
k1, k2, k3, k4 = st.columns(4)
k1.metric("كفاءة النظام", "94%", "2%+")
k2.metric("شاحنات نشطة", len(df_ord[df_ord['الحالة'] != 'تم التسليم ✅']))
k3.metric("تأخيرات 🔴", len(df_ord[df_ord['الحالة'] == 'متأخر 🔴']))
k4.metric("إجمالي المخزون", f"{df_inv['الرصيد'].sum():,}")

st.markdown("---")
# الأقسام التفاعلية
tab1, tab2, tab3 = st.tabs(["🚛 تحليل الأسطول والمدن", "📦 تقرير المستودعات", "📊 الرؤية البيانية"])

with tab1:
    st.dataframe(df_ord.sort_values(by='المدينة'), use_container_width=True)

with tab2:
    st.dataframe(df_inv, use_container_width=True)

with tab3:
    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(px.pie(df_ord, names='الحالة', hole=0.4, title="حالة الأسطول"), use_container_width=True)
    with col_b:
        st.plotly_chart(px.bar(df_inv, x='المنتج', y='الرصيد', color='المستودع', barmode='group', title="توزيع المخزون"), use_container_width=True)