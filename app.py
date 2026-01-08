import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
import os

# --- 1. التصميم والهوية البصرية (Dark Professional) ---
st.set_page_config(page_title="Expert AI Advisor", layout="wide", page_icon="👨‍💼")

def img_to_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_avatar = img_to_base64("me.jpg")

# --- 2. محرك البيانات (Real-time Data Simulation) ---
if 'init' not in st.session_state:
    # بيانات المخزون
    st.session_state.inv = pd.DataFrame([
        {'Warehouse': w, 'Product': p, 'Stock': np.random.randint(20, 3000)}
        for w in ['Dubai Central', 'Abu Dhabi Main', 'Sharjah Hub']
        for p in ['Cola 330ml', 'Cola 1.5L', 'Water 500ml', 'Flour 5kg', 'Pasta']
    ])
    # بيانات الأسطول
    st.session_state.fleet = pd.DataFrame([
        {'Order': f'ORD-{i}', 'Status': np.random.choice(['Delivered ✅', 'Delayed 🔴', 'In Transit 🚚']),
         'City': np.random.choice(['Dubai', 'Abu Dhabi', 'Sharjah', 'Al Ain']),
         'Driver': np.random.choice(['Saeed', 'Ahmed', 'Jasim', 'Khaled']),
         'Efficiency': np.random.randint(60, 100)} for i in range(1, 51)
    ])
    st.session_state.history = []
    st.session_state.init = True

# --- 3. محرك "عقل المستشار" (فهم المنطق والرد على السؤال) ---
def get_strategic_response(user_input):
    text = user_input.lower()
    inv = st.session_state.inv
    fleet = st.session_state.fleet
    
    # تحليلات فورية للبيانات
    low_stock = inv[inv['Stock'] < 500]
    delays = fleet[fleet['Status'] == 'Delayed 🔴']
    
    # أ- تحليل المناطق (دبي، الشارقة، أبوظبي)
    for city in ['dubai', 'دبي', 'sharjah', 'شارقه', 'abu dhabi', 'أبوظبي']:
        if city in text:
            city_name = "Dubai Central" if "dubai" in city or "دبي" in city else \
                        "Sharjah Hub" if "sharjah" in city or "شارقه" in city else "Abu Dhabi Main"
            city_data = inv[inv['Warehouse'] == city_name]
            city_delays = fleet[(fleet['City'].str.contains(city_name.split()[0])) & (fleet['Status'] == 'Delayed 🔴')]
            
            return (f"### 📍 تقرير فرع {city_name}:\n"
                    f"* **المخزون:** الإجمالي حالياً {city_data['Stock'].sum():,} وحدة.\n"
                    f"* **التحديات:** رصدت {len(city_delays)} تأخيرات في التوصيل لهذه المنطقة.\n"
                    f"💡 **نصيحة استشارية:** فرع {city_name} يحتاج لدعم في صنف '{city_data.sort_values('Stock').iloc[0]['Product']}' فوراً لتجنب النفاذ.")

    # ب- تحليل التأخير والمشاكل
    if any(word in text for word in ['تاخير', 'تأخير', 'delay', 'مشكلة', 'delayed']):
        return (f"### ⚠️ تحليل المعوقات اللوجستية:\n"
                f"أستاذ طارق، لدينا حالياً **{len(delays)} شحنة متأخرة**. \n"
                f"أكثر سائق يواجه صعوبات هو **{delays['Driver'].value_counts().idxmax()}**. \n"
                f"أنصح بإعادة مراجعة مسار 'شارع الشيخ زايد' واستخدام 'شارع الإمارات' البديل لتجاوز الزحام.")

    # ج- تحليل النواقص
    if any(word in text for word in ['نقص', 'ناقص', 'خلص', 'stock', 'low']):
        return (f"### 📦 تقرير النواقص الحرجة:\n"
                f"يوجد **{len(low_stock)}** منتجات تحت خط الأمان. \n"
                f"الأكثر خطورة: **{low_stock.sort_values('Stock').iloc[0]['Product']}** في {low_stock.sort_values('Stock').iloc[0]['Warehouse']}.\n"
                f"💡 **الإجراء المقترح:** تحويل مخزون من دبي لتغطية العجز في الفروع الأخرى.")

    # د- رد ذكي عام (بمنطقي أنا)
    return ("معك يا أستاذ طارق. لقد قمت بمسح البيانات الآن.. هل تريدني أن أركز على (أسباب التأخير في الأسطول) أم (تجهيز قائمة مشتريات للنواقص)؟")

# --- 4. واجهة المحادثة (Sidebar) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="width:110px;height:110px;border-radius:50%;border:3px solid #00FFCC;object-fit:cover;"></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#00FFCC;'>المستشار طارق AI</h2>", unsafe_allow_html=True)
    st.markdown("---")

    for msg in st.session_state.history:
        with st.chat_message(msg["role"], avatar=user_avatar if msg["role"] == "assistant" else None):
            st.markdown(msg["content"])

    if prompt := st.chat_input("تحدث معي.. اسأل عن دبي، التأخير، أو النقص"):
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        # استدعاء العقل المدبر
        response = get_strategic_response(prompt)
        
        with st.chat_message("assistant", avatar=user_avatar):
            st.markdown(response)
        st.session_state.history.append({"role": "assistant", "content": response})

# --- 5. الداشبورد الرئيسي (التصميم الاحترافي) ---
st.markdown("<h1 style='text-align: center;'>🌐 Strategic Operations Center</h1>", unsafe_allow_html=True)

# العدادات العلوية
c1, c2, c3, c4 = st.columns(4)
c1.metric("إجمالي المخزون", f"{st.session_state.inv['Stock'].sum():,}")
c2.metric("شحنات متأخرة", len(st.session_state.fleet[st.session_state.fleet['Status'] == 'Delayed 🔴']), delta="-2", delta_color="inverse")
c3.metric("كفاءة الأسطول", f"{st.session_state.fleet['Efficiency'].mean():.1f}%")
c4.metric("السائق المثالي", "Saeed")

st.markdown("---")
# الرسوم البيانية (Area Chart & Map)
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📈 تحليل تدفق المنتجات وزمن التسليم")
    fig = px.area(st.session_state.fleet, x='City', y='Efficiency', color='Driver', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("💡 نصيحة استشارية")
    st.success("بناءً على اتجاهات الاستهلاك، نقترح تكثيف شحنات 'Cola 330ml' لأبوظبي قبل عطلة نهاية الأسبوع.")
    
    st.subheader("🌍 مراقبة المسارات (Live Map)")
    st.map(pd.DataFrame({'lat': [25.2, 24.4, 25.3, 24.1], 'lon': [55.3, 54.4, 55.4, 55.7]}))

st.subheader("📋 تفاصيل الحالة التشغيلية للمستودعات")
st.dataframe(st.session_state.inv, use_container_width=True)