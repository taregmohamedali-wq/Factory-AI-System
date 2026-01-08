import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات الهوية ---
st.set_page_config(page_title="المستشار طارق - التحليل اليومي", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_avatar = get_base64_img("me.jpg")

# --- 2. محرك جلب وتحليل البيانات ---
@st.cache_data
def load_and_analyze():
    try:
        inv = pd.read_csv("UAE_Operations_DB.xlsx - Inventory.csv")
        orders = pd.read_csv("UAE_Operations_DB.xlsx - Order_History.csv")
        return inv, orders
    except:
        return pd.DataFrame(), pd.DataFrame()

df_inv, df_orders = load_and_analyze()

# --- 3. محرك النصيحة الاستراتيجية (ذكاء المحادثة) ---
def get_strategic_advice(query="وضع اليوم"):
    if df_inv.empty or df_orders.empty:
        return "سيدي، أحتاج للوصول للملفات لأعطيك نصيحة دقيقة."

    # تحليل التأخير
    delayed = df_orders[df_orders['Status'].str.contains('متأخر', na=False)]
    # تحليل المخزون الحرج
    critical_stock = df_inv[df_inv['Stock_Level'] < 300]
    
    analysis = ""
    if "وضع" in query or "نصيحه" in query or "تحليل" in query:
        analysis = f"### 🛡️ التقرير الاستراتيجي للأستاذ طارق\n"
        analysis += f"**أولاً: الأسطول:** رصدت {len(delayed)} شحنة متأخرة اليوم. المشكلة تتركز في مسار دبي-أبوظبي.  \n"
        if not critical_stock.empty:
            analysis += f"**ثانياً: المخزون:** تحذير عالي الخطورة! صنف ({critical_stock.iloc[0]['Product']}) في {critical_stock.iloc[0]['Warehouse']} شارف على النفاذ ({critical_stock.iloc[0]['Stock_Level']} وحدة فقط).  \n"
        analysis += f"**النصيحة:** سيدي، أقترح تحويل شحنة طوارئ من دبي إلى الشارقة فوراً، وتوجيه السائق {delayed.iloc[0]['Driver'] if not delayed.empty else ''} لتغيير المسار لتفادي الازدحام."
    
    return analysis

# --- 4. واجهة المحادثة (Sidebar) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:120px; border:3px solid #00ffcc;"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>AI المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'chat' not in st.session_state: st.session_state.chat = []
    
    for m in st.session_state.chat:
        with st.chat_message(m["role"], avatar=user_avatar if m["role"]=="assistant" else None):
            st.write(m["content"])

    if p := st.chat_input("تحدث معي.. اسأل عن وضع اليوم"):
        st.session_state.chat.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        
        response = get_strategic_advice(p)
        with st.chat_message("assistant", avatar=user_avatar): st.write(response)
        st.session_state.chat.append({"role": "assistant", "content": response})

# --- 5. الداشبورد والرسوم البيانية ---
st.markdown("<h1 style='text-align: center;'>🏗️ Operations Command Center</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    # المنطقة العلوية: التحليل الفوري
    st.markdown(get_strategic_advice(), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # العدادات
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("إجمالي المخزون", f"{df_inv['Stock_Level'].sum():,}")
    c2.metric("شحنات متأخرة 🔴", len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)]))
    c3.metric("تحت التسليم 🚚", len(df_orders[df_orders['Status'].str.contains('الطريق', na=False)]))
    c4.metric("كفاءة اليوم", "88%", "-2%")

    st.markdown("---")

    # الرسوم البيانية والخريطة
    col_graph, col_map = st.columns([2, 1])
    
    with col_graph:
        st.subheader("📊 ميزان المخزون لكل منتج وموقع")
        fig = px.bar(df_inv, x='Warehouse', y='Stock_Level', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
        
    with col_map:
        st.subheader("📍 مواقع العمليات النشطة")
        # خريطة افتراضية لمواقع المستودعات في الإمارات
        map_data = pd.DataFrame({
            'lat': [25.2048, 24.4539, 25.3463, 24.1302],
            'lon': [55.2708, 54.3773, 55.4209, 55.8023],
            'name': ['Dubai', 'Abu Dhabi', 'Sharjah', 'Al Ain']
        })
        st.map(map_data)

    st.subheader("📋 سجل الطلبات والعمليات التفصيلي")
    st.dataframe(df_orders, use_container_width=True)

else:
    st.error("⚠️ سيدي، لا توجد بيانات للتحليل. تأكد من وجود الملفات.")