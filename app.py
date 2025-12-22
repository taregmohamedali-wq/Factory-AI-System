import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. إعدادات الصفحة
st.set_page_config(page_title="Strategic AI Manager", layout="wide")

# 2. حل مشكلة AttributeError - تهيئة الذاكرة والبيانات فوراً
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'db_initialized' not in st.session_state:
    # بناء قاعدة البيانات
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
    st.session_state.db_initialized = True

# --- القائمة الجانبية: محادثة ChatGPT المفتوحة ---
with st.sidebar:
    st.header("👨‍💼 خبير العمليات الذكي")
    st.write("أستاذ طارق، أنا الآن جاهز للنقاش المفتوح وتحليل أي مشكلة.")
    st.markdown("---")
    
    # عرض سجل المحادثة بأمان
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("تحدث معي.. كيف ترى وضع المصنع اليوم؟"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            q = prompt.lower()
            df_ord = st.session_state.df_orders
            df_inv = st.session_state.df_inv
            
            # استخراج أرقام للتحليل اللحظي
            delayed_orders = df_ord[df_ord['الحالة'] == 'متأخر 🔴']
            low_stock = df_inv[df_inv['الرصيد'] < 400]

            # ردود ذكية ومفتوحة بناءً على السياق
            if any(word in q for word in ["أهلا", "مرحبا", "هلا", "كيف حالك", "شلونك"]):
                response = f"أهلاً بك أستاذ طارق! أنا في قمة الجاهزية. قمت بتحليل سريع للوضع: لدينا {len(delayed_orders)} شحنات متأخرة، و {len(low_stock)} أصناف تحتاج إعادة تعبئة فورية. بماذا نبدأ نقاشنا الاستراتيجي اليوم؟"
            
            elif any(word in q for word in ["مدن", "مدينة", "وين", "فين", "تأخير"]):
                if not delayed_orders.empty:
                    cities = delayed_orders['المدينة'].unique()
                    response = f"بناءً على تتبع الأسطول، المدن التي تعاني من مشاكل تسليم الآن هي: **{', '.join(cities)}**. \n\n"
                    response += "💡 **رأيي الاستشاري:** يتركز التأخير في هذه المناطق مما قد يشير إلى ضغط مروري أو سوء توزيع للمسارات. هل تريد مني اقتراح إعادة توزيع للشاحنات؟"
                else:
                    response = "جميع المدن مغطاة بالكامل والوضع تحت السيطرة سيدي."

            elif any(word in q for word in ["مخزن", "نقص", "بضاعة", "نواقص", "حل"]):
                if not low_stock.empty:
                    p_name = low_stock.iloc[0]['المنتج']
                    w_name = low_stock.iloc[0]['المستودع']
                    response = f"رصدت نقصاً حاداً في **{p_name}** بـ **{w_name}**. \n\n"
                    response += "💼 **نصيحة للمدير:** تأخير توريد هذه المادة قد يعطل خطوط الإنتاج أو يسخط كبار العملاء. أنصح بعمل مناقلة فورية من مخزن أبوظبي لتغطية العجز."
                else:
                    response = "المخزون مستقر جداً اليوم، ولا توجد أي نواقص تعيق العمل."

            else:
                response = "فهمت وجهة نظرك. كخبير عمليات، أرى أن التركيز على 'زمن الاستجابة' هو مفتاحنا اليوم. هل تريد تحليل أداء السائقين بشكل أعمق أم ننتقل لمراجعة توازن المخازن؟"

            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- الواجهة الرئيسية (لوحة القيادة الاستراتيجية) ---
st.markdown("<h1 style='text-align: center;'>🏭 مركز الإدارة والتحليل الاستراتيجي</h1>", unsafe_allow_html=True)

# صف الـ KPIs
k1, k2, k3, k4 = st.columns(4)
k1.metric("كفاءة التشغيل", "94%", "2%+")
k2.metric("شاحنات في الطريق 🚚", len(df_ord[df_ord['الحالة'] == 'في الطريق 🚚']))
k3.metric("تأخيرات حرجة 🔴", len(delayed_orders), delta_color="inverse")
k4.metric("تغطية الأصناف", f"{len(df_inv) - len(low_stock)}/{len(df_inv)}")

st.markdown("---")
tab1, tab2, tab3 = st.tabs(["🚛 رقابة الأسطول والمدن", "📦 حالة المستودعات", "📊 تحليل الأداء"])

with tab1:
    st.subheader("تحليل جرافي وحركي للأسطول")
    st.dataframe(st.session_state.df_orders.sort_values(by='الأهمية'), use_container_width=True)

with tab2:
    st.subheader("تقرير توازن المخزون")
    st.dataframe(st.session_state.df_inv, use_container_width=True)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.pie(df_ord, names='الحالة', hole=0.4, title="تحليل حالة الشحنات"), use_container_width=True)
    with c2:
        st.plotly_chart(px.bar(df_inv, x='المنتج', y='الرصيد', color='المستودع', barmode='group', title="مستويات المخزون"), use_container_width=True)