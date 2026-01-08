import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
import os

# --- 1. التصميم الكلاسيكي الواضح (Dark Mode) ---
st.set_page_config(page_title="Strategic Operations Center", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return f"data:image/jpeg;base64,{base64.encodebytes(f.read()).decode()}"
    return None

img_bg = get_base64_img("me.jpg")

# --- 2. تهيئة البيانات ---
if 'data_init' not in st.session_state:
    st.session_state.df_inv = pd.DataFrame([
        {'Warehouse': w, 'Product': p, 'Stock': np.random.randint(50, 4000)}
        for w in ['Dubai Central', 'Abu Dhabi Main', 'Sharjah Hub']
        for p in ['Cola 330ml', 'Cola 1.5L', 'Water 500ml', 'Flour 5kg', 'Pasta']
    ])
    st.session_state.df_fleet = pd.DataFrame([
        {'Order': f'ORD-{i}', 'Status': np.random.choice(['Delivered ✅', 'Delayed 🔴', 'In Transit 🚚']),
         'City': np.random.choice(['Dubai', 'Abu Dhabi', 'Sharjah', 'Al Ain']),
         'Driver': np.random.choice(['Saeed', 'Ahmed', 'Jasim', 'Khaled', 'Mohamed']),
         'Time': np.random.randint(50, 500)} for i in range(1, 61)
    ])
    st.session_state.chat_history = []
    st.session_state.data_init = True

# --- 3. محرك الفهم (الرد على السؤال فعلياً) ---
def smart_reply(user_query):
    query = user_query.lower()
    inv = st.session_state.df_inv
    fleet = st.session_state.df_fleet
    
    # رد مباشر عن "الشارقة" أو "دبي"
    if any(city in query for city in ['دبي', 'dubai', 'شارقه', 'sharjah', 'ابوظبي', 'abu dhabi']):
        target = "Dubai" if "دبي" in query or "dubai" in query else "Sharjah" if "شارقه" in query or "sharjah" in query else "Abu Dhabi"
        city_stock = inv[inv['Warehouse'].str.contains(target)]['Stock'].sum()
        city_delays = len(fleet[(fleet['City'].str.contains(target)) & (fleet['Status'] == 'Delayed 🔴')])
        return f"📍 **وضع {target} حالياً:** المخزون المتوفر {city_stock:,} وحدة، ولدينا {city_delays} شحنات متأخرة. أنصح بمتابعة الشحنات المتجهة هناك فوراً."

    # رد مباشر عن "التأخير"
    if any(word in query for word in ['تاخير', 'تأخير', 'delayed']):
        delays = fleet[fleet['Status'] == 'Delayed 🔴']
        return f"⚠️ **تحليل التأخير:** رصدت {len(delays)} شحنة متأخرة. السائق الأكثر تأخراً هو **{delays['Driver'].value_counts().idxmax()}**. هل تود التواصل معه؟"

    # رد مباشر عن "النقص"
    if any(word in query for word in ['نقص', 'ناقص', 'اين']):
        low = inv[inv['Stock'] < 600]
        if not low.empty:
            item = low.sort_values('Stock').iloc[0]
            return f"📦 **تنبيه نقص:** أقل صنف هو **{item['Product']}** في مستودع {item['Warehouse']} برصيد {item['Stock']} وحدة فقط. يجب التوريد حالاً."
        return "المخزون آمن حالياً ولا يوجد نقص حرج."

    # رد استشاري عام
    return "معك أستاذ طارق. بتحليل البيانات الآن، أنصحك بالنظر في (تأخيرات الأسطول) أو (مراجعة مخزن الشارقة) حيث تتركز المشاكل حالياً. ماذا تريد أن نفحص؟"

# --- 4. واجهة المحادثة (Sidebar) ---
with st.sidebar:
    if img_bg: st.image(img_bg, width=110)
    st.markdown("### AI المستشار طارق")
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    if prompt := st.chat_input("تحدث معي.. اسأل عن مدينة أو التأخير"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        # الحصول على الرد الحقيقي
        ans = smart_reply(prompt)
        with st.chat_message("assistant"): st.write(ans)
        st.session_state.chat_history.append({"role": "assistant", "content": ans})

# --- 5. الصفحة الرئيسية (التصميم السابق الواضح) ---
st.markdown("<h1 style='text-align: center;'>📊 Strategic Operations Center</h1>", unsafe_allow_html=True)

# العدادات العلوية الواضحة
m1, m2, m3, m4 = st.columns(4)
m1.metric("إجمالي المخزون", f"{st.session_state.df_inv['Stock'].sum():,}")
m2.metric("شحنات متأخرة", len(st.session_state.df_fleet[st.session_state.df_fleet['Status'] == 'Delayed 🔴']), delta="-2")
m3.metric("نسبة الإنجاز", "85.2%")
m4.metric("السائق المثالي", "Saeed")

st.markdown("---")

col_l, col_r = st.columns([2, 1])

with col_l:
    st.subheader("📈 تحليل تدفق المنتجات (الرسم الواضح)")
    # رسم بياني خطي بسيط وواضح بدلاً من المتشابك
    fig = px.line(st.session_state.df_fleet.sort_values('City'), x='City', y='Time', color='Driver', 
                  markers=True, template="plotly_dark", title="زمن التوصيل حسب المدن")
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    # مربع النصيحة الاستشارية المطلوب
    st.subheader("💡 نصيحة استشارية اليوم")
    st.info("""
    **تحليل السوق:** بناءً على بيانات الاستهلاك، يرتفع الطلب على 'Flour 5kg' في عطلة نهاية الأسبوع. 
    تأكد من دعم مخزن **أبوظبي** بنسبة 20% إضافية اليوم لتحسين التدفق النقدي.
    """)
    
    st.subheader("🌍 مراقبة المواقع")
    st.map(pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]}))

st.subheader("📋 تفاصيل المخزون الحالية")
st.dataframe(st.session_state.df_inv, use_container_width=True)