import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات الصفحة والهوية ---
st.set_page_config(page_title="Strategic AI Advisor", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_avatar = get_base64_img("me.jpg")

# --- 2. محرك قراءة البيانات ---
@st.cache_data
def load_data():
    try:
        df_inv = pd.read_csv("UAE_Operations_DB.xlsx - Inventory.csv")
        df_orders = pd.read_csv("UAE_Operations_DB.xlsx - Order_History.csv")
        return df_inv, df_orders
    except:
        return pd.DataFrame(), pd.DataFrame()

df_inv, df_orders = load_data()

# --- 3. محرك التفكير والتحليل (منطق طارق الرقمي) ---
def advanced_strategic_logic(query):
    if df_inv.empty or df_orders.empty: return "سيدي، قاعدة البيانات غير متصلة."
    
    q = query.lower()
    delayed = df_orders[df_orders['Status'].str.contains('متأخر', na=False)]
    critical_items = df_inv[df_inv['Stock_Level'] < 500]
    
    # منطق التحليل الشامل
    if any(word in q for word in ['وضع', 'تحليل', 'نصيح', 'ماذا']):
        top_delayed_city = delayed['City'].value_counts().idxmax() if not delayed.empty else "مستقر"
        
        analysis = f"### 🛡️ رؤيتي التحليلية لليوم سيدي:\n"
        analysis += f"أستاذ طارق، رصدت **{len(delayed)}** حالات تأخير، التركيز الأكبر حالياً في **{top_delayed_city}**. "
        
        if not critical_items.empty:
            item = critical_items.iloc[0]
            analysis += f"هناك نقطة ضعف في مستودع **{item['Warehouse']}** لنفاذ صنف **({item['Product']})**. \n\n"
        
        analysis += "💡 **التوصية:** أقترح تحويل مخزون طوارئ من دبي لتعويض عجز الشارقة، وإعادة جدولة مسارات أبوظبي لتفادي الازدحام."
        return analysis

    return "معك يا أستاذ طارق، أنا أحلل الأرقام الآن. هل نبدأ بمراجعة (أداء السائقين) أم (نواقص المستودعات)؟"

# --- 4. واجهة المحادثة التفاعلية (SideBar) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:110px; border:3px solid #00ffcc;"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>المستشار الذكي</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'messages' not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"], avatar=user_avatar if m["role"]=="assistant" else None):
            st.write(m["content"])

    if prompt := st.chat_input("تحدث معي.. كيف ترى العمليات اليوم؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        res = advanced_strategic_logic(prompt)
        with st.chat_message("assistant", avatar=user_avatar): st.write(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

# --- 5. الداشبورد الاحترافي (الواجهة الرئيسية) ---
st.markdown("<h1 style='text-align:center;'>📊 Operations Command Center</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    # المنطقة 1: النصيحة الاستراتيجية الفورية
    st.info(advanced_strategic_logic("تحليل عام"))
    
    st.markdown("---")
    
    # المنطقة 2: العدادات (KPIs)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("المخزون الكلي", f"{df_inv['Stock_Level'].sum():,}")
    k2.metric("شحنات متأخرة 🔴", len(delayed))
    k3.metric("في الطريق 🚚", len(df_orders[df_orders['Status'].str.contains('طريق', na=False)]))
    k4.metric("كفاءة اليوم", "92%")

    st.markdown("---")
    
    # المنطقة 3: الرسوم البيانية والخريطة
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.subheader("📈 ميزان توزيع المخزون")
        fig = px.bar(df_inv, x='Warehouse', y='Stock_Level', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
        
    with col_r:
        st.subheader("📍 التوزيع الجغرافي")
        map_data = pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]})
        st.map(map_data)

    st.subheader("📋 سجل العمليات الحي")
    st.dataframe(df_orders, use_container_width=True)