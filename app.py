import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
import base64

# --- 1. وظيفة الأفاتار لضمان ظهور صورتك me.jpg ---
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    except: return None

# 2. إعدادات الصفحة
st.set_page_config(page_title="Strategic AI Manager", layout="wide", page_icon="👨‍💼")

# 3. تهيئة البيانات (محاكاة دال فود - Dal Food Context)
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

# تعريف المتغيرات
df_ord = st.session_state.df_orders
df_inv = st.session_state.df_inv
user_avatar = get_image_base64("me.jpg")

# --- 4. القائمة الجانبية: المستشار طارق (المحلل الذكي) ---
with st.sidebar:
    st.session_state.lang = st.selectbox("🌐 Language", ["ar", "en"], index=0 if st.session_state.lang == "ar" else 1)
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="width:100px;border-radius:50%;border:3px solid #1E3A8A;"></div>', unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center'>{'المستشار طارق' if st.session_state.lang == 'ar' else 'Consultant Tariq'}</h3>", unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar=user_avatar if msg["role"] == "assistant" else None):
            st.markdown(msg["content"])

    if prompt := st.chat_input("اسألني عن المخزون أو التأخير..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant", avatar=user_avatar):
            query = prompt.lower()
            
            # --- منطق تحليل المستودعات الذكي ---
            if any(word in query for word in ["مستودع", "دبي", "warehouse", "dubai"]):
                # تحليل بيانات دبي تحديداً
                dubai_inv = df_inv[df_inv['Warehouse'].str.contains('Dubai', case=False)]
                total_stock = dubai_inv['Stock'].sum()
                low_stock_items = dubai_inv[dubai_inv['Stock'] < 1000]['Product'].tolist()
                
                if st.session_state.lang == "ar":
                    response = f"### 📦 تحليل مستودع دبي المركز\n\n"
                    response += f"سيدي، إجمالي المخزون الحالي في دبي هو **{total_stock:,} وحدة**. \n\n"
                    response += f"**⚠️ ملاحظة ذكاء اصطناعي:** رصدت نقصاً في الأصناف التالية: {', '.join(low_stock_items)}. \n"
                    response += "**💡 مقترح القرار:** أنصح بتحويل جزء من مخزون مستودع أبوظبي لدعم دبي، أو جدولة أمر توريد عاجل لتغطية الطلبات القادمة."
                else:
                    response = f"### 📦 Dubai Warehouse Analysis\n\n"
                    response += f"Total stock in Dubai is **{total_stock:,} units**. \n\n"
                    response += f"**⚠️ AI Alert:** Stock is low for: {', '.join(low_stock_items)}. \n"
                    response += "**💡 Decision Support:** I recommend a stock transfer from Abu Dhabi or an immediate procurement order."

            elif any(word in query for word in ["تأخير", "delay", "شاحن"]):
                delayed = df_ord[df_ord['Status'].str.contains('Delayed|متأخر')]
                if st.session_state.lang == "ar":
                    response = f"رصدت {len(delayed)} شحنات متأخرة في مدن {', '.join(delayed['City'].unique())}. أنصح بإعادة توجيه الأسطول."
                else:
                    response = f"Detected {len(delayed)} delays in {', '.join(delayed['City'].unique())}. Recommend re-routing."
            
            else:
                response = "أهلاً أستاذ طارق. أنا جاهز لتحليل بيانات مستودعات دبي وأبوظبي، أو تقديم مقترحات لتحسين مسارات الشاحنات. بماذا نبدأ؟"

            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- 5. الواجهة الرئيسية (Dashboard) ---
st.markdown(f"<h1 style='text-align: center;'>🏭 Strategic Operations Center</h1>", unsafe_allow_html=True)
# (باقي الكود الخاص بـ KPIs والجداول والرسوم البيانية يبقى كما هو)
st.dataframe(df_inv, use_container_width=True)