import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
import os

# --- 1. إعدادات الصفحة والهوية (Dark Theme) ---
st.set_page_config(page_title="Strategic Operations Center", layout="wide", page_icon="👨‍💼")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    return None

user_avatar = get_image_base64("me.jpg")

# --- 2. محرك البيانات (Data Engine) ---
if 'db_init' not in st.session_state:
    # بيانات المخزون
    st.session_state.df_inv = pd.DataFrame([
        {'Warehouse': w, 'Product': p, 'Stock': np.random.randint(50, 4000)}
        for w in ['Dubai Central', 'Abu Dhabi Main', 'Sharjah Hub']
        for p in ['Cola 330ml', 'Cola 1.5L', 'Water 500ml', 'Flour 5kg', 'Pasta']
    ])
    # بيانات الأسطول
    st.session_state.df_ord = pd.DataFrame([
        {
            'Order_ID': f'ORD-{100+i}',
            'Status': np.random.choice(['Delivered ✅', 'Delayed 🔴', 'In Transit 🚚']),
            'City': np.random.choice(['Dubai', 'Abu Dhabi', 'Sharjah', 'Al Ain']),
            'Driver': np.random.choice(['Saeed', 'Ahmed', 'Jasim', 'Khaled', 'Mohamed']),
            'Delivery_Time': np.random.randint(40, 600)
        } for i in range(50)
    ])
    st.session_state.chat_history = []
    st.session_state.db_init = True

# --- 3. محرك الاستشارة المرن (Human-Like Advisor) ---
def get_expert_advice(prompt):
    q = prompt.lower()
    df_i = st.session_state.df_inv
    df_o = st.session_state.df_ord
    
    # تحليلات سريعة للرد
    low_stock = df_i[df_i['Stock'] < 600]
    delays = df_o[df_o['Status'] == 'Delayed 🔴']
    
    # أ- تحليل المسارات والخرائط (محاكاة ذكاء الإنترنت)
    if any(word in q for word in ['طريق', 'شارع', 'زحمة', 'اسرع', 'route', 'map']):
        return (f"### 🗺️ تحليل المسارات الذكي:\n"
                f"بناءً على تحديثات المرور الحالية، أنصح باتخاذ **شارع محمد بن زايد (E311)** كبديل لشارع الشيخ زايد المتوقف حالياً.\n\n"
                f"💡 **نصيحة:** وجه السائقين (Saeed و Ahmed) للتحرك الآن لتفادي ذروة الازدحام المسائية، هذا سيوفر 20% من استهلاك الوقود.")

    # ب- تحليل الوضع العام (استشارة شاملة)
    if any(word in q for word in ['وضع', 'كامل', 'تحليل', 'ايه الاخبار', 'status']):
        return (f"### 📊 ملخص الاستشارة الاستراتيجية:\n"
                f"1. **المخازن:** لدينا عجز في {len(low_stock)} منتجات بالشارقة. أنصح بتحويل مخزون فوري من دبي.\n"
                f"2. **الأسطول:** هناك {len(delays)} شحنات متأخرة في العين. السبب غالباً لوجستي وليس فني.\n"
                f"3. **توصية الإدارة:** بناءً على معايير (Supply Chain Excellence)، نحتاج لزيادة عدد شاحنات النقل الخفيف في أبوظبي بنسبة 10%.")

    # ج- الرد على أي سؤال عام (المرونة)
    if any(word in q for word in ['شكرا', 'هلا', 'مرحبا', 'انت مين']):
        return "أهلاً بك يا أستاذ طارق. أنا مستشارك الرقمي، جاهز لتحليل المخازن، اقتراح أسرع الطرق، أو تقديم نصائح لزيادة كفاءة التوزيع. بماذا نبدأ اليوم؟"

    # د- تحليل النواقص
    if any(word in q for word in ['نقص', 'ناقص', 'بضاعة', 'خلص']):
        if not low_items.empty:
            return f"رصدت نقصاً حرجاً في **{low_stock.iloc[0]['Product']}**. الكمية الحالية لا تغطي طلبات الـ 48 ساعة القادمة."
        
    return "سؤال جيد يا أستاذ طارق. بالنظر لبياناتنا الحالية، أرى أن هذا يتطلب مراجعة مسارات التوزيع أو إعادة جرد مخزن الشارقة. هل تود أن أعطيك تفاصيل أكثر عن أحدهما؟"

# --- 4. تصميم الواجهة (Sidebar Chat) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="width:100px;border-radius:50%;border:3px solid #1E3A8A;object-fit:cover;"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center'>المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar=user_avatar if msg["role"] == "assistant" else None):
            st.markdown(msg["content"])

    if prompt := st.chat_input("تحدث معي.. اسأل عن الطرق أو المخازن"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        response = get_expert_advice(prompt)
        with st.chat_message("assistant", avatar=user_avatar):
            st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- 5. الواجهة الرئيسية (The Professional Dashboard) ---
st.markdown("<h1 style='text-align: center;'>🏭 Strategic Operations Center</h1>", unsafe_allow_html=True)

# مؤشرات الأداء (KPIs)
m1, m2, m3, m4 = st.columns(4)
m1.metric("إجمالي المخزون", f"{st.session_state.df_inv['Stock'].sum():,}")
m2.metric("شحنات متأخرة", len(st.session_state.df_ord[st.session_state.df_ord['Status'] == 'Delayed 🔴']), delta="-2", delta_color="inverse")
m3.metric("نسبة الإنجاز", f"{(len(st.session_state.df_ord[st.session_state.df_ord['Status'] == 'Delivered ✅'])/len(st.session_state.df_ord))*100:.1f}%")
m4.metric("السائق المثالي", "Saeed")

st.markdown("---")

# الرسوم البيانية المتطورة (مثل التي في الصور)
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 تحليل تدفق المنتجات عبر المدن")
    fig1 = px.area(st.session_state.df_ord.sort_values('City'), x='City', y='Delivery_Time', color='Driver', 
                  title="زمن التسليم لكل مدينة حسب السائق", template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader("💡 نصيحة استشارية")
    st.info("بناءً على اتجاهات السوق، يرتفع الطلب على 'Flour 5kg' في عطلة نهاية الأسبوع. تأكد من دعم مستودع دبي بنسبة 20% إضافية اليوم.")
    
    st.subheader("🌍 مراقبة المواقع")
    # محاكاة الخريطة التي تظهر في صورتك
    map_data = pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]})
    st.map(map_data, zoom=7)

st.subheader("📋 تفاصيل المخزون الحالية")
st.dataframe(st.session_state.df_inv, use_container_width=True)