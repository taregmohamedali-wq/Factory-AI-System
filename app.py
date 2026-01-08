import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
import os
from datetime import datetime

# --- 1. إعدادات الهوية البصرية ---
st.set_page_config(page_title="Strategic AI Consultant", layout="wide", page_icon="👨‍💼")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    return None

user_avatar = get_image_base64("me.jpg")

# --- 2. بناء قاعدة بيانات العمليات (محاكاة واقعية) ---
if 'db_init' not in st.session_state:
    # بيانات المخازن
    prods = ['Cola 330ml', 'Cola 1.5L', 'Water 500ml', 'Flour 5kg', 'Pasta']
    whs = ['Dubai Central', 'Abu Dhabi Main', 'Sharjah Hub']
    inv = []
    for p in prods:
        for w in whs:
            inv.append({'Warehouse': w, 'Product': p, 'Stock': np.random.randint(50, 5000), 'Min_Limit': 1000})
    
    # بيانات الأسطول والعملاء
    drivers = ['Saeed', 'Ahmed', 'Jasim', 'Khaled', 'Mohamed']
    cities = ['Dubai', 'Abu Dhabi', 'Sharjah', 'Al Ain', 'Fujairah']
    orders = []
    for i in range(1, 101):
        orders.append({
            'Order_ID': f'ORD-{2000+i}',
            'Customer': f'V-Client {np.random.randint(1,20)}',
            'Status': np.random.choice(['Delivered ✅', 'Delayed 🔴', 'In Transit 🚚']),
            'Driver': np.random.choice(drivers),
            'City': np.random.choice(cities),
            'Delivery_Time': np.random.randint(30, 180), # بالدقائق
            'Route_Efficiency': np.random.uniform(0.5, 1.0)
        })
    
    st.session_state.df_inv = pd.DataFrame(inv)
    st.session_state.df_ord = pd.DataFrame(orders)
    st.session_state.chat_history = []
    st.session_state.db_init = True

# --- 3. محرك الاستشارة والذكاء الاصطناعي (Logic & Advice Engine) ---
def get_strategic_advice(query):
    q = query.lower()
    df_i = st.session_state.df_inv
    df_o = st.session_state.df_ord
    
    # أ- التحليل العام الشامل (المخازن + السيارات + العملاء)
    if any(word in q for word in ['عام', 'تحليل كامل', 'الوضع', 'overall']):
        low_stock = len(df_i[df_i['Stock'] < df_i['Min_Limit']])
        delayed = len(df_o[df_o['Status'] == 'Delayed 🔴'])
        top_city = df_o['City'].value_counts().idxmax()
        
        advice = f"""
        ### 📊 التقرير الاستراتيجي الشامل:
        1. **المخازن:** يوجد لدينا **{low_stock}** منتجات تحت حد الطلب. أنصح بجدولة توريد فورية.
        2. **الأسطول:** هناك **{delayed}** شحنة متأخرة، مما يؤثر على سمعة الشركة لدى العملاء.
        3. **العملاء:** مدينة **{top_city}** هي الأكثر طلباً حالياً، يجب تكثيف السيارات هناك.
        
        💡 **نصيحة استشارية:** بناءً على معايير (Supply Chain Excellence)، أنصحك بتقليل الفاقد في مستودع الشارقة لتحسين التدفق النقدي.
        """
        return advice, "general"

    # ب- ذكاء الطرق والخرائط (محاكاة البحث في الخرائط)
    if any(word in q for word in ['طريق', 'شارع', 'أسرع', 'خريطة', 'route', 'map']):
        fastest_route = "شارع الشيخ محمد بن زايد (E311)"
        alternative = "شارع الإمارات (E611)"
        advice = f"""
        ### 🗺️ تحليل المسارات الذكي (Real-time Simulation):
        بناءً على تحديثات المرور الحالية في الإمارات:
        * **المسار الأسرع:** حالياً هو **{fastest_route}** نظراً لسيولة الحركة.
        * **تحذير:** تجنب وسط مدينة دبي (منطقة القوز) لوجود أعمال صيانة مؤقتة.
        * **توصية:** وجه السائقين (Saeed و Ahmed) لاتخاذ المخرج رقم 45 لتوفير 15 دقيقة من زمن التسليم.
        """
        return advice, "map"

    # ج- تحليل النواقص والطلبيات الحرج
    if any(word in q for word in ['نقص', 'نواقص', 'shortage']):
        critical = df_i[df_i['Stock'] < 500]
        advice = "### ⚠️ تقرير النواقص الحرجة:\n"
        for _, row in critical.iterrows():
            advice += f"* المنتج **{row['Product']}** في {row['Warehouse']} وصل لمستوى **{row['Stock']}** (حرج جداً!).\n"
        return advice, "table"

    return "مرحباً أستاذ طارق. أنا مستشارك الرقمي. اطلب مني (تحليل كامل للوضع، أسرع طريق للمدينة، أو تقرير النواقص) وسأقوم بالبحث والتحليل فوراً.", "text"

# --- 4. تصميم الواجهة الجانبية (الشات الاستشاري) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="width:100px;border-radius:50%;border:3px solid #00FFCC;"></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center'>المستشار طارق AI</h2>", unsafe_allow_html=True)
    st.markdown("---")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar=user_avatar if msg["role"] == "assistant" else None):
            st.markdown(msg["content"])

    if prompt := st.chat_input("اطلب استشارة: تحليل كامل، أسرع طريق..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        response_text, res_type = get_strategic_advice(prompt)
        
        with st.chat_message("assistant", avatar=user_avatar):
            st.markdown(response_text)
            # إظهار داشبورد مصغر داخل الشات لو كان التحليل عاماً
            if res_type == "general":
                st.line_chart(st.session_state.df_ord.groupby('City')['Delivery_Time'].mean())
        
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})

# --- 5. الواجهة الرئيسية (Strategic Dashboard) ---
st.markdown("<h1 style='text-align: center;'>🌐 Global Strategic Operations Hub</h1>", unsafe_allow_html=True)

# مؤشرات الأداء الكبرى
m1, m2, m3, m4 = st.columns(4)
m1.metric("إجمالي الأصول", f"{st.session_state.df_inv['Stock'].sum():,}", "Active")
m2.metric("كفاءة المسارات", "92%", "+3%")
m3.metric("رضا العملاء", "4.8/5", "⭐")
m4.metric("تنبؤات الذكاء", "مستقرة")

st.markdown("---")
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📊 تحليل تدفق المنتجات عبر المدن")
    fig = px.area(st.session_state.df_ord.sort_values('City'), x='City', y='Delivery_Time', color='Driver', title="زمن التسليم لكل مدينة حسب السائق")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("💡 نصيحة استشارية اليوم")
    st.info("بناءً على بيانات السوق، يرتفع الطلب على 'Flour 5kg' في عطلة نهاية الأسبوع. تأكد من شحن مستودع أبوظبي اليوم بنسبة 20% إضافية.")
    
    st.subheader("🌍 مراقبة المواقع")
    # محاكاة خريطة (Map)
    map_data = pd.DataFrame({
        'lat': [25.276987, 24.453884, 25.346255],
        'lon': [55.296249, 54.377343, 55.420932]
    })
    st.map(map_data)