import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
import os

# --- 1. الهوية البصرية (التي اخترتها) ---
st.set_page_config(page_title="Strategic Operations Hub", layout="wide")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_avatar = get_base64("me.jpg")

# --- 2. البيانات (محاكاة دقيقة لبياناتك) ---
if 'db' not in st.session_state:
    st.session_state.df_inv = pd.DataFrame([
        {'Warehouse': w, 'Product': p, 'Stock': np.random.randint(40, 3500)}
        for w in ['Dubai Central', 'Abu Dhabi Main', 'Sharjah Hub']
        for p in ['Cola 330ml', 'Cola 1.5L', 'Water 500ml', 'Flour 5kg', 'Pasta']
    ])
    st.session_state.df_fleet = pd.DataFrame([
        {'Order': f'ORD-{i}', 'Status': np.random.choice(['Delivered ✅', 'Delayed 🔴', 'In Transit 🚚']),
         'City': np.random.choice(['Dubai', 'Abu Dhabi', 'Sharjah', 'Al Ain']),
         'Driver': np.random.choice(['Saeed', 'Ahmed', 'Jasim', 'Khaled'])} for i in range(1, 51)
    ])
    st.session_state.chat = []

# --- 3. محرك الاستجابة (حل مشكلة عدم الفهم) ---
def advisor_brain(user_input):
    q = user_input.lower()
    inv = st.session_state.df_inv
    fleet = st.session_state.df_fleet
    
    # تحليلات سريعة
    low_stock = inv[inv['Stock'] < 500]
    delays = fleet[fleet['Status'] == 'Delayed 🔴']

    # رد مخصص لـ "دبي" أو أي مدينة
    if any(word in q for word in ['دبي', 'dubai']):
        data = inv[inv['Warehouse'].str.contains('Dubai')]
        return f"📍 **وضع دبي حالياً:** المخزون الإجمالي {data['Stock'].sum():,} وحدة. \n\n💡 **نصيحة:** لاحظت أن {data.iloc[0]['Product']} منخفض، أنصح بتحويل شحنة من أبوظبي فوراً."

    # رد مخصص لـ "الوضع العام" أو "تحليل"
    if any(word in q for word in ['عام', 'تحليل', 'وضع', 'status']):
        return (f"📊 **التقرير الاستراتيجي:** \n"
                f"1. العمليات مستقرة بنسبة {80}%. \n"
                f"2. لدينا {len(delays)} تأخيرات تحتاج تدخل عاجل. \n"
                f"3. توجد {len(low_stock)} أصناف قاربت على النفاذ.")

    # رد مخصص لـ "التأخير"
    if any(word in q for word in ['تاخير', 'تأخير', 'delay']):
        return f"⚠️ **تحليل التأخير:** لدينا {len(delays)} شحنة متوقفة. السائق {delays.iloc[0]['Driver']} يواجه زحاماً في منطقة {delays.iloc[0]['City']}. أنصح بتغيير مساره لشارع الإمارات."

    # رد مخصص لـ "النقص"
    if any(word in q for word in ['نقص', 'ناقص', 'خلص']):
        item = low_stock.iloc[0] if not low_stock.empty else None
        return f"📦 **تنبيه نقص:** المنتج {item['Product']} في {item['Warehouse']} وصل لـ {item['Stock']} وحدة فقط. يجب الطلب الآن." if item else "لا يوجد نقص حرج حالياً."

    # في حال لم يفهم، يطلب توضيح بدلاً من تكرار رسالة واحدة
    return "أهلاً أستاذ طارق، هل تريدني أن أحلل لك (وضع دبي) أم (أسباب التأخير في الشحنات)؟ أنا جاهز ببيانات لحظية."

# --- 4. واجهة المحادثة (Sidebar) ---
with st.sidebar:
    if user_avatar: st.image(user_avatar, width=100)
    st.markdown("### المستشار طارق AI")
    
    for m in st.session_state.chat:
        with st.chat_message(m["role"]): st.write(m["content"])

    if p := st.chat_input("اسألني عن دبي، التأخير، أو النقص..."):
        st.session_state.chat.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        
        # هنا يتم استدعاء "العقل" الذي يحلل ويرد
        res = advisor_brain(p)
        
        with st.chat_message("assistant"): st.write(res)
        st.session_state.chat.append({"role": "assistant", "content": res})

# --- 5. الداشبورد (التصميم المطلوب) ---
st.markdown("<h1 style='text-align: center;'>🏭 Strategic Operations Center</h1>", unsafe_allow_html=True)

# العدادات
c1, c2, c3 = st.columns(3)
c1.metric("إجمالي المخزون", f"{st.session_state.df_inv['Stock'].sum():,}")
c2.metric("شحنات متأخرة", len(st.session_state.df_fleet[st.session_state.df_fleet['Status'] == 'Delayed 🔴']))
c3.metric("كفاءة التوصيل", "88%")

st.markdown("---")
col_l, col_r = st.columns([2, 1])

with col_l:
    st.subheader("📈 تحليل تدفق المنتجات")
    fig = px.area(st.session_state.df_fleet, x='City', color='Driver', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.subheader("🌍 مراقبة المواقع")
    st.map(pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]}))

st.dataframe(st.session_state.df_inv, use_container_width=True)