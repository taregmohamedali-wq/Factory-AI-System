import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
import os

# --- 1. إعدادات الصفحة والأفاتار ---
st.set_page_config(page_title="Strategic AI Manager", layout="wide", page_icon="👨‍💼")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    return None

user_avatar = get_image_base64("me.jpg")

# --- 2. تهيئة البيانات في الـ Session State ---
if 'db_init' not in st.session_state:
    prods = ['Cola 330ml', 'Cola 1.5L', 'Water 500ml', 'Flour 5kg', 'Pasta']
    whs = ['Dubai Central', 'Abu Dhabi Main', 'Sharjah Hub']
    inv = []
    for p in prods:
        for w in whs:
            inv.append({'Warehouse': w, 'Product': p, 'Stock': np.random.randint(50, 4000)})
    
    orders = []
    drivers = ['Saeed', 'Ahmed', 'Jasim', 'Khaled', 'Mohamed']
    cities = ['Dubai', 'Abu Dhabi', 'Sharjah', 'Al Ain', 'Fujairah']
    for i in range(1, 61):
        orders.append({
            'Order_ID': f'ORD-{1000+i}',
            'Status': np.random.choice(['Delivered ✅', 'Delayed 🔴', 'In Transit 🚚']),
            'Driver': np.random.choice(drivers),
            'City': np.random.choice(cities),
            'Quantity': np.random.randint(10, 100)
        })
    
    st.session_state.df_inv = pd.DataFrame(inv)
    st.session_state.df_ord = pd.DataFrame(orders)
    st.session_state.chat_history = []
    st.session_state.db_init = True

# --- 3. محرك التحليل الذكي (الاستجابة حسب السؤال) ---
def smart_response(prompt):
    q = prompt.lower()
    df_inv = st.session_state.df_inv
    df_ord = st.session_state.df_ord
    
    # أ- سؤال عن النقص (اين النقص؟ / بضاعة قليلة)
    if any(word in q for word in ['نقص', 'قليل', 'ناقص', 'shortage', 'low']):
        low_stock = df_inv[df_inv['Stock'] < 600]
        if not low_stock.empty:
            res = f"سيدي، رصدت نقصاً في **{len(low_stock)}** أصناف. أكثرها حرجاً هو **{low_stock.sort_values('Stock').iloc[0]['Product']}**."
            return res, low_stock, "table"
        return "المخزون ممتاز حالياً، لا يوجد صنف تحت حد الخطر.", None, None

    # ب- سؤال عن وضع المخزون العام (رسم بياني)
    if any(word in q for word in ['مخزون', 'وضع', 'كل', 'inventory', 'stock']):
        res = f"إجمالي المخزون الحالي في جميع الفروع هو **{df_inv['Stock'].sum():,}** وحدة."
        return res, df_inv, "chart"

    # ج- سؤال عن السائقين أو الأداء
    if any(word in q for word in ['سائق', 'أداء', 'سواق', 'driver']):
        top_driver = df_ord[df_ord['Status'] == 'Delivered ✅']['Driver'].value_counts()
        res = f"أفضل سائق من حيث الإنجاز هو **{top_driver.index[0]}** بـ {top_driver.values[0]} شحنة مكتملة."
        return res, top_driver.to_frame(), "table"

    # د- سؤال عن التأخير
    if any(word in q for word in ['تأخير', 'مشكلة', 'delayed']):
        delayed_df = df_ord[df_ord['Status'] == 'Delayed 🔴']
        res = f"هناك **{len(delayed_df)}** شحنة متأخرة حالياً. المشكلة تتركز في **{delayed_df['City'].value_counts().index[0]}**."
        return res, delayed_df, "table"

    return "مرحباً أستاذ طارق. أنا جاهز لتحليل العمليات. يمكنك سؤالي عن (النقص، المخزون العام، أداء السائقين، أو التأخير).", None, None

# --- 4. تصميم الواجهة (Sidebar & Chat) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="width:100px;border-radius:50%;border:3px solid #1E3A8A;"></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center'>المستشار طارق</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # عرض الدردشة
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar=user_avatar if msg["role"] == "assistant" else None):
            st.markdown(msg["content"])
            if "data" in msg:
                if msg["type"] == "table": st.dataframe(msg["data"], use_container_width=True)
                if msg["type"] == "chart": 
                    fig = px.bar(msg["data"], x='Product', y='Stock', color='Warehouse', barmode='group')
                    st.plotly_chart(fig, use_container_width=True)

    if prompt := st.chat_input("اسألني أي شيء عن العمليات..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        text_res, data_res, type_res = smart_response(prompt)
        
        msg_obj = {"role": "assistant", "content": text_res}
        if data_res is not None:
            msg_obj["data"] = data_res
            msg_obj["type"] = type_res
            
        st.session_state.chat_history.append(msg_obj)
        st.rerun()

# --- 5. الواجهة الرئيسية (The Professional Dashboard) ---
st.markdown("<h1 style='text-align: center;'>📊 Strategic Operations Center</h1>", unsafe_allow_html=True)

# صف المؤشرات العلوية (KPIs)
m1, m2, m3, m4 = st.columns(4)
total_inv = st.session_state.df_inv['Stock'].sum()
delayed_count = len(st.session_state.df_ord[st.session_state.df_ord['Status'] == 'Delayed 🔴'])
delivered_rate = (len(st.session_state.df_ord[st.session_state.df_ord['Status'] == 'Delivered ✅']) / len(st.session_state.df_ord)) * 100

m1.metric("إجمالي المخزون", f"{total_inv:,}")
m2.metric("شحنات متأخرة", delayed_count, delta="-2" if delayed_count > 5 else "0", delta_color="inverse")
m3.metric("نسبة النجاح", f"{delivered_rate:.1f}%")
m4.metric("عدد السائقين", "5")

st.markdown("---")

# الرسوم البيانية الرئيسية
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📦 توزيع المخزون حسب الصنف")
    fig1 = px.bar(st.session_state.df_inv.groupby('Product')['Stock'].sum().reset_index(), x='Product', y='Stock', color_discrete_sequence=['#00CC96'])
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader("🚚 حالة الأسطول الحالي")
    fig2 = px.pie(st.session_state.df_ord, names='Status', hole=0.4, color_discrete_map={'Delivered ✅':'green', 'Delayed 🔴':'red', 'In Transit 🚚':'orange'})
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("📋 تفاصيل البيانات التشغيلية")
st.dataframe(st.session_state.df_inv, use_container_width=True)