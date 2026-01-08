import streamlit as st
import pandas as pd
import numpy as np
import base64
import os

# --- 1. وظيفة الأفاتار المحسنة ---
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    else:
        # في حال لم يجد الصورة، سيعطيك لوناً افتراضياً بدلاً من كسر الكود
        return None

# 2. إعدادات الصفحة
st.set_page_config(page_title="Strategic AI Manager", layout="wide", page_icon="👨‍💼")

# 3. تهيئة البيانات (تبقى كما هي لضمان المنطق)
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
    for i in range(1, 51):
        orders.append({
            'Order_ID': f'ORD-{1000+i}',
            'Status': np.random.choice(['Delivered ✅', 'Delayed 🔴', 'In Transit 🚚']),
            'Driver': np.random.choice(drivers),
            'City': np.random.choice(cities),
            'Priority': np.random.choice(['VIP (AAA)', 'High (AA)', 'Normal (A)'])
        })
    st.session_state.df_inv = pd.DataFrame(inv)
    st.session_state.df_orders = pd.DataFrame(orders)
    st.session_state.chat_history = [] 
    st.session_state.db_init = True

# استدعاء الصورة (تأكد أن ملف me.jpg في نفس مجلد الكود)
user_avatar = get_image_base64("me.jpg")

# --- 4. محرك الإجابة المنطقية (المستشار طارق) ---
def advanced_analyser(query):
    q = query.lower()
    df_i = st.session_state.df_inv
    df_o = st.session_state.df_orders
    
    # منطق الكلمات المفتاحية الذكي
    if any(word in q for word in ['مخزون', 'بضاعة', 'stock']):
        total = df_i['Stock'].sum()
        return f"سيدي، إجمالي المخزون المتاح حالياً هو **{total:,}** وحدة موزعة على جميع المستودعات."
    
    if any(word in q for word in ['تأخير', 'مشكلة', 'delay']):
        delayed = len(df_o[df_o['Status'] == 'Delayed 🔴'])
        return f"رصدت وجود **{delayed}** شحنات متأخرة. أنصح بالتحقق من قسم التوزيع."

    if any(word in q for word in ['سائق', 'سواق', 'driver']):
        top_driver = df_o[df_o['Status'] == 'Delivered ✅']['Driver'].value_counts().index[0]
        return f"أفضل أداء حالياً هو للسائق **{top_driver}**."

    return "مرحباً أستاذ طارق، أنا المحلل الذكي الخاص بك. كيف يمكنني دعم اتخاذ القرار اليوم؟"

# --- 5. الواجهة الجانبية (الشات مع الصورة) ---
with st.sidebar:
    # عرض الصورة الشخصية في أعلى القائمة الجانبية كشعار
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="width:100px;height:100px;border-radius:50%;border:3px solid #FF4B4B;object-fit:cover;"></div>', unsafe_allow_html=True)
    
    st.markdown(f"<h2 style='text-align:center'>المستشار طارق</h2>", unsafe_allow_html=True)
    st.markdown("---")

    # عرض تاريخ المحادثة مع أيقونة الأفاتار
    for msg in st.session_state.chat_history:
        # إذا كان المساعد هو من يتحدث، نستخدم الصورة me.jpg
        avatar_to_show = user_avatar if msg["role"] == "assistant" else None
        with st.chat_message(msg["role"], avatar=avatar_to_show):
            st.markdown(msg["content"])

    if prompt := st.chat_input("اسألني عن العمليات..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): 
            st.markdown(prompt)
        
        response = advanced_analyser(prompt)
        
        # عرض رد الروبوت مع الصورة
        with st.chat_message("assistant", avatar=user_avatar):
            st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- 6. الواجهة الرئيسية (تبقى كما هي) ---
st.title("🏭 Strategic Operations Center")
# (بقية كود الـ Dashboard والرسوم البيانية)