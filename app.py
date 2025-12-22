import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
import base64

# --- 1. وظيفة تحويل الصورة ---
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    except Exception:
        return None

# 2. إعدادات الصفحة
st.set_page_config(page_title="Strategic AI Manager", layout="wide", page_icon="👨‍💼")

# 3. تهيئة البيانات واللغة
if 'db_init' not in st.session_state:
    st.session_state.lang = "ar"  # اللغة الافتراضية
    prods = ['Cola 330ml', 'Cola 1.5L', 'Water 500ml', 'Flour 5kg', 'Pasta']
    whs = ['Dubai Central', 'Abu Dhabi Main', 'Sharjah Hub']
    inv = []
    for p in prods:
        for w in whs:
            inv.append({'Warehouse': w, 'Product': p, 'Stock': np.random.randint(50, 4000)})
    
    drivers = ['Saeed', 'Ahmed', 'Jasim', 'Khaled', 'Mohamed']
    cities = ['Dubai', 'Abu Dhabi', 'Sharjah', 'Al Ain', 'Fujairah']
    orders = []
    for i in range(1, 41):
        orders.append({
            'Customer': f'Client {i}',
            'Status': np.random.choice(['Delivered ✅', 'Delayed 🔴', 'In Transit 🚚']),
            'Driver': np.random.choice(drivers),
            'City': np.random.choice(cities),
            'Priority': np.random.choice(['VIP (AAA)', 'High (AA)', 'Normal (A)']),
            'Truck': f'TRK-{100+i}'
        })
    st.session_state.df_inv = pd.DataFrame(inv)
    st.session_state.df_orders = pd.DataFrame(orders)
    st.session_state.chat_history = [] 
    st.session_state.db_init = True

# --- قاموس الترجمة ---
texts = {
    "ar": {
        "title": "🏛️ مركز الإدارة والتحليل الاستراتيجي",
        "sidebar_title": "المستشار طارق",
        "sidebar_sub": "مدير العمليات الذكي",
        "eff": "كفاءة النظام",
        "active_trucks": "شاحنات نشطة",
        "delays": "تأخيرات 🔴",
        "total_inv": "إجمالي المخزون",
        "tab1": "🚛 الرقابة الجغرافية",
        "tab2": "📦 حالة المستودعات",
        "tab3": "📊 الرؤية البيانية",
        "chat_placeholder": "تحدث معي.. كيف نحسن العمل؟",
        "response_intro": "أهلاً أستاذ طارق. بناءً على التحليل اللحظي: ",
    },
    "en": {
        "title": "🏛️ Strategic Management & Analytics Center",
        "sidebar_title": "Consultant Tariq",
        "sidebar_sub": "AI Operations Manager",
        "eff": "System Efficiency",
        "active_trucks": "Active Trucks",
        "delays": "Delays 🔴",
        "total_inv": "Total Inventory",
        "tab1": "🚛 Geographic Control",
        "tab2": "📦 Warehouse Status",
        "tab3": "📊 Analytics Vision",
        "chat_placeholder": "Chat with me.. How can we improve?",
        "response_intro": "Hello Mr. Tariq. Based on real-time analysis: ",
    }
}

L = texts[st.session_state.lang]

# تعريف المتغيرات
df_ord = st.session_state.df_orders
df_inv = st.session_state.df_inv
delayed_count = len(df_ord[df_ord['Status'].str.contains('Delayed|متأخر')])
efficiency = 100 - (delayed_count/len(df_ord)*100) if len(df_ord) > 0 else 100
user_avatar = get_image_base64("me.jpg")

# --- 4. القائمة الجانبية ---
with st.sidebar:
    # اختيار اللغة
    st.session_state.lang = st.selectbox("🌐 Language / اللغة", ["ar", "en"], index=0 if st.session_state.lang == "ar" else 1)
    st.markdown("---")
    
    if user_avatar:
        st.markdown(f'<div style="display: flex; justify-content: center;"><img src="{user_avatar}" style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 3px solid #1E3A8A;"></div>', unsafe_allow_html=True)
    
    st.markdown(f"<h3 style='text-align: center;'>{L['sidebar_title']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #1E3A8A;'>{L['sidebar_sub']}</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar=user_avatar if msg["role"] == "assistant" else None):
            st.markdown(msg["content"])

    if prompt := st.chat_input(L["chat_placeholder"]):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=user_avatar):
            if st.session_state.lang == "ar":
                res = f"أهلاً أستاذ طارق، كفاءة النظام حالياً {efficiency:.1f}%. رصدت {delayed_count} تأخيرات. بصفتي مستشارك، أنصح بالتدخل الفوري."
            else:
                res = f"Hello Mr. Tariq, current efficiency is {efficiency:.1f}%. I detected {delayed_count} delays. As your advisor, I recommend immediate intervention."
            st.markdown(res)
            st.session_state.chat_history.append({"role": "assistant", "content": res})

# --- 5. الواجهة الرئيسية ---
st.markdown(f"<h1 style='text-align: center; color: #1E3A8A;'>{L['title']}</h1>", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
k1.metric(L["eff"], f"{efficiency:.1f}%")
k2.metric(L["active_trucks"], len(df_ord))
k3.metric(L["delays"], delayed_count, delta_color="inverse")
k4.metric(L["total_inv"], f"{df_inv['Stock'].sum():,}")

t1, t2, t3 = st.tabs([L["tab1"], L["tab2"], L["tab3"]])

with t1:
    st.dataframe(df_ord, use_container_width=True)
with t2:
    st.dataframe(df_inv, use_container_width=True)
with t3:
    c1, c2 = st.columns(2)
    with c1: st.plotly_chart(px.pie(df_ord, names='Status', hole=0.4, title=L["tab1"]), use_container_width=True)
    with c2: st.plotly_chart(px.bar(df_inv, x='Product', y='Stock', color='Warehouse', barmode='group', title=L["tab2"]), use_container_width=True)