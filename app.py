import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
import base64

# --- 1. وظائف تقنية ---
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    except: return None

# 2. إعدادات الصفحة
st.set_page_config(page_title="Strategic AI Manager", layout="wide", page_icon="👨‍💼")

# 3. تهيئة البيانات المركزية
if 'db_init' not in st.session_state:
    st.session_state.lang = "ar"
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

# تعريف المتغيرات للتحليل
df_ord = st.session_state.df_orders
delayed_df = df_ord[df_ord['Status'].str.contains('Delayed|متأخر')]
efficiency = 100 - (len(delayed_df)/len(df_ord)*100) if len(df_ord) > 0 else 100
user_avatar = get_image_base64("me.jpg")

# --- 4. القائمة الجانبية (AI Dialogue Engine) ---
with st.sidebar:
    st.session_state.lang = st.selectbox("🌐 Language", ["ar", "en"], index=0 if st.session_state.lang == "ar" else 1)
    st.markdown("---")
    
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="width:100px;border-radius:50%;border:3px solid #1E3A8A;"></div>', unsafe_allow_html=True)
    
    st.markdown(f"<h3 style='text-align:center'>{'المستشار طارق' if st.session_state.lang == 'ar' else 'Consultant Tariq'}</h3>", unsafe_allow_html=True)
    
    # عرض المحادثة
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar=user_avatar if msg["role"] == "assistant" else None):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Type your question..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant", avatar=user_avatar):
            # --- محرك التحليل الذكي ---
            query = prompt.lower()
            if "delay" in query or "تأخير" in query or "تاخير" in query:
                # الرد بناءً على تحليل حقيقي للبيانات
                cities = delayed_df['City'].unique()
                drivers_list = delayed_df['Driver'].unique()
                if st.session_state.lang == "ar":
                    response = f"### 🔴 تحليل التأخيرات اللحظي\n\nأهلاً أستاذ طارق. لقد قمت بتحليل الأسطول الآن؛ لدينا **{len(delayed_df)}** شحنة متأخرة. \n\n"
                    response += f"**المناطق المتأثرة:** {', '.join(cities)}.\n"
                    response += f"**السائقين المعنيين:** {', '.join(drivers_list)}.\n\n"
                    response += "بناءً على هذا، المشكلة تبدو متعلقة بضغط العمل في تلك المسارات. أنصح بالتواصل مع السائقين أو إعادة جدولة طلبات الـ VIP أولاً."
                else:
                    response = f"### 🔴 Real-time Delay Analysis\n\nI have analyzed the fleet data. We currently have **{len(delayed_df)}** delayed shipments.\n\n"
                    response += f"**Affected Areas:** {', '.join(cities)}.\n"
                    response += f"**Drivers Involved:** {', '.join(drivers_list)}.\n\n"
                    response += "Recommendation: The bottleneck seems to be route-specific. I suggest prioritizing VIP orders and re-routing available trucks."
            
            elif "hello" in query or "مرحبا" in query or "اهلا" in query:
                if st.session_state.lang == "ar":
                    response = f"أهلاً بك يا أستاذ طارق. كفاءة النظام الحالية هي {efficiency:.1f}%. كيف يمكنني مساعدتك في تحسين الأداء اليوم؟"
                else:
                    response = f"Hello Mr. Tariq. Current efficiency is {efficiency:.1f}%. How can I assist you in optimizing operations today?"
            
            else:
                if st.session_state.lang == "ar":
                    response = "لقد استلمت استفسارك. هل تود مني تحليل بيانات المستودعات أم تعمق أكثر في أداء السائقين والرحلات المتأخرة؟"
                else:
                    response = "I've received your query. Would you like me to analyze warehouse data or dive deeper into driver performance and delayed trips?"

            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- 5. الواجهة الرئيسية (تبقى كما هي لضمان الـ KPIs) ---
st.markdown("<h1 style='text-align: center;'>🏭 Strategic Operations Center</h1>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)
k1.metric("Efficiency", f"{efficiency:.1f}%")
k2.metric("Active Jobs", len(df_ord))
k3.metric("Delays", len(delayed_df), delta_color="inverse")
k4.metric("Inventory", f"{st.session_state.df_inv['Stock'].sum():,}")

tab1, tab2, tab3 = st.tabs(["Fleet", "Warehouse", "Analytics"])
with tab1: st.dataframe(df_ord, use_container_width=True)
with tab2: st.dataframe(st.session_state.df_inv, use_container_width=True)
with tab3:
    c1, c2 = st.columns(2)
    with c1: st.plotly_chart(px.pie(df_ord, names='Status', hole=0.4), use_container_width=True)
    with c2: st.plotly_chart(px.bar(st.session_state.df_inv, x='Product', y='Stock', color='Warehouse'), use_container_width=True)