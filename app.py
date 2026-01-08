import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
import os

# --- 1. إعدادات الهوية والتصميم الداكن ---
st.set_page_config(page_title="Strategic Operations Center", layout="wide", page_icon="👨‍💼")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    return None

user_avatar = get_image_base64("me.jpg")

# --- 2. تهيئة البيانات وذاكرة المحادثة ---
if 'db_init' not in st.session_state:
    st.session_state.df_inv = pd.DataFrame([
        {'Warehouse': w, 'Product': p, 'Stock': np.random.randint(50, 4000)}
        for w in ['Dubai Central', 'Abu Dhabi Main', 'Sharjah Hub']
        for p in ['Cola 330ml', 'Cola 1.5L', 'Water 500ml', 'Flour 5kg', 'Pasta']
    ])
    st.session_state.df_ord = pd.DataFrame([
        {'Order_ID': f'ORD-{100+i}', 'Status': np.random.choice(['Delivered ✅', 'Delayed 🔴', 'In Transit 🚚']),
         'City': np.random.choice(['Dubai', 'Abu Dhabi', 'Sharjah', 'Al Ain']),
         'Driver': np.random.choice(['Saeed', 'Ahmed', 'Jasim', 'Khaled', 'Mohamed']),
         'Delivery_Time': np.random.randint(40, 600)} for i in range(50)
    ])
    st.session_state.chat_history = []
    st.session_state.last_topic = None  # ذاكرة الموضوع الحالي
    st.session_state.db_init = True

# --- 3. محرك الاستشارة الذكي (فهم السياق) ---
def smart_advisor_logic(prompt):
    q = prompt.lower()
    df_i = st.session_state.df_inv
    df_o = st.session_state.df_ord
    
    # تحليلات سريعة
    low_stock = df_i[df_i['Stock'] < 600]
    
    # أ- التعامل مع الردود المكملة (مثل: نعم، كمل، أعطني تفاصيل)
    if any(word in q for word in ['نعم', 'تمام', 'كمل', 'تفاصيل', 'اكثر', 'details', 'more']):
        if st.session_state.last_topic == "sharjah":
            data = df_i[df_i['Warehouse'].str.contains("Sharjah")]
            return f"بالتأكيد أستاذ طارق، في الشارقة لدينا عجز في {len(data[data['Stock'] < 600])} أصناف. المخزون الإجمالي هناك هو {data['Stock'].sum():,} وحدة. هل نطلب توريد الآن؟"
        elif st.session_state.last_topic == "delays":
            return "بخصوص التأخيرات، تتركز المشكلة في 'العين' بسبب نقص الشاحنات الخفيفة. أقترح إعادة توجيه شاحنة من دبي."
        else:
            return "بالطبع، أنا معك. ما هي الجزئية التي تود الغوص في تفاصيلها أكثر (المخازن أم المسارات)؟"

    # ب- تحليل المواقع (الشارقة، دبي، إلخ)
    if any(word in q for word in ['شارقه', 'sharjah']):
        st.session_state.last_topic = "sharjah"
        val = df_i[df_i['Warehouse'].str.contains("Sharjah")]['Stock'].sum()
        return f"مستودع الشارقة حالياً يحتوي على **{val:,}** وحدة. لاحظت وجود بطء في حركة 'Water 500ml' هناك. هل تريد تفاصيل النواقص؟"

    # ج- تحليل المسارات والطرق
    if any(word in q for word in ['طريق', 'شارع', 'زحمة', 'اسرع', 'route']):
        st.session_state.last_topic = "routes"
        return "المسار الأسرع حالياً هو **E311**. تجنب وسط المدينة لوجود أعمال صيانة. وجهت 'Saeed' لاتخاذ المخرج الخلفي لتوفير الوقت."

    # د- تحليل عام
    if any(word in q for word in ['وضع', 'تحليل', 'كامل', 'status']):
        st.session_state.last_topic = "general"
        return f"سيدي، الوضع العام مستقر بنسبة 85%. لدينا {len(low_stock)} أصناف حرجة و {len(df_o[df_o['Status'] == 'Delayed 🔴'])} شحنات متأخرة."

    return "مرحباً أستاذ طارق. أنا جاهز؛ اسألني عن أي مدينة أو اطلب تحليلاً للمخازن والمسارات وسأجيبك فوراً."

# --- 4. تصميم الواجهة الجانبية (الشات المطور) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="width:100px;border-radius:50%;border:3px solid #00FFCC;object-fit:cover;"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center'>المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar=user_avatar if msg["role"] == "assistant" else None):
            st.markdown(msg["content"])

    if prompt := st.chat_input("تحدث معي.. اسألني عن أي شيء"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        response = smart_advisor_logic(prompt)
        with st.chat_message("assistant", avatar=user_avatar):
            st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- 5. الواجهة الرئيسية (التصميم الاحترافي المطلوب) ---
st.markdown("<h1 style='text-align: center;'>📊 Strategic Operations Hub</h1>", unsafe_allow_html=True)

# صف المؤشرات (KPIs)
m1, m2, m3, m4 = st.columns(4)
m1.metric("إجمالي المخزون", f"{st.session_state.df_inv['Stock'].sum():,}")
m2.metric("شحنات متأخرة", len(st.session_state.df_ord[st.session_state.df_ord['Status'] == 'Delayed 🔴']), delta="-3", delta_color="inverse")
m3.metric("نسبة الإنجاز", f"{(len(st.session_state.df_ord[st.session_state.df_ord['Status'] == 'Delivered ✅'])/len(st.session_state.df_ord))*100:.1f}%")
m4.metric("السائق المثالي", "Saeed")

st.markdown("---")
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📈 تحليل تدفق المنتجات وزمن التسليم")
    fig1 = px.area(st.session_state.df_ord.sort_values('City'), x='City', y='Delivery_Time', color='Driver', template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("💡 نصيحة استشارية اليوم")
    st.info("يتوقع زيادة طلب 15% في العين نهاية الأسبوع. تأكد من جاهزية أسطول النقل الخفيف.")
    
    st.subheader("🌍 مراقبة المواقع (Live Map)")
    map_data = pd.DataFrame({'lat': [25.2, 24.4, 25.3, 24.1], 'lon': [55.3, 54.4, 55.4, 55.7]})
    st.map(map_data, zoom=7)

st.subheader("📋 تفاصيل البيانات التشغيلية")
st.dataframe(st.session_state.df_inv, use_container_width=True)