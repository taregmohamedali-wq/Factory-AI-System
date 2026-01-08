import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. بناء الهوية البصرية ---
st.set_page_config(page_title="Strategic Operations Command", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_avatar = get_base64_img("me.jpg")

# --- 2. محرك قراءة البيانات (الربط المباشر بملفاتك) ---
@st.cache_data
def load_all_files():
    try:
        # الربط بملفاتك المرفوعة سلفاً بنفس أسمائها الدقيقة
        inv = pd.read_csv("UAE_Operations_DB.xlsx - Inventory.csv")
        orders = pd.read_csv("UAE_Operations_DB.xlsx - Order_History.csv")
        return inv, orders
    except:
        return pd.DataFrame(), pd.DataFrame()

df_inv, df_orders = load_all_files()

# --- 3. عقل المستشار (الذكاء الذي يفهم ويحلل) ---
def strategic_thinking(query):
    if df_inv.empty or df_orders.empty:
        return "أستاذ طارق، لم أتمكن من العثور على البيانات. يرجى التأكد من مسار الملفات."

    # استخلاص حقائق اللحظة
    delayed_df = df_orders[df_orders['Status'].str.contains('متأخر', na=False)]
    critical_stock = df_inv[df_inv['Stock_Level'] < 500]
    
    q = query.lower()
    
    # منطق "التحليل الاستباقي"
    if any(word in q for word in ['وضع', 'تحليل', 'نصيحة', 'ماذا', 'تقرير']):
        top_city = delayed_df['City'].value_counts().idxmax() if not delayed_df.empty else "المسارات مستقرة"
        
        # ربط الحقائق ببعضها
        response = f"### 🛡️ قراءتي للموقف العملياتي الآن:\n\n"
        response += f"سيدي، بعد تحليل سجلات اليوم، رصدت **{len(delayed_df)}** شحنات متأخرة، والمشكلة تتركز بوضوح في **{top_city}**. "
        
        if not critical_stock.empty:
            item = critical_stock.iloc[0]
            response += f"بينما تظهر البيانات خطراً في مستودع **{item['Warehouse']}** لنفاذ صنف **({item['Product']})** (الرصيد: {item['Stock_Level']}).\n\n"
        
        response += "💡 **قراري المقترح:** أستاذ طارق، الأولوية الآن لتحريك مخزون طوارئ للشارقة، وإعادة توجيه 3 سائقين من دبي لدعم مسار أبوظبي لتفادي تفاقم التأخير."
        return response

    return "معك يا أستاذ طارق. أنا الآن أراقب الأرقام حياً؛ هل تريد التركيز على (كفاءة السائقين) أم (خطة تأمين نواقص المخازن)؟"

# --- 4. واجهة المحادثة التفاعلية (SideBar) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:110px; border:3px solid #00ffcc; box-shadow: 0px 4px 15px rgba(0,255,204,0.3);"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>المستشار الذكي طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'messages' not in st.session_state: st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"], avatar=user_avatar if m["role"]=="assistant" else None):
            st.write(m["content"])

    if prompt := st.chat_input("تحدث معي.. كيف ترى وضع العمليات؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        # استدعاء العقل التحليلي
        res = strategic_thinking(prompt)
        with st.chat_message("assistant", avatar=user_avatar): st.write(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

# --- 5. الداشبورد الاحترافي الكامل (تصميم Command Center) ---
st.markdown("<h1 style='text-align:center;'>📊 Operations Command Hub</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    # المنطقة 1: التحليل الذكي التلقائي (في أعلى الصفحة دائماً)
    st.info(strategic_thinking("تحليل عام"))
    
    st.markdown("---")
    
    # المنطقة 2: مؤشرات الأداء (KPIs)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("المخزون الكلي", f"{df_inv['Stock_Level'].sum():,}")
    k2.metric("شحنات متأخرة 🔴", len(delayed_df))
    k3.metric("تحت التسليم", len(df_orders[df_orders['Status'].str.contains('طريق', na=False)]))
    k4.metric("كفاءة الأداء", "91%")

    st.markdown("---")
    
    # المنطقة 3: التحليل البصري والخريطة
    col_chart, col_map = st.columns([2, 1])
    
    with col_chart:
        st.subheader("📈 توازن المخزون (منتج/مستودع)")
        fig = px.bar(df_inv, x='Warehouse', y='Stock_Level', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
        
    with col_map:
        st.subheader("📍 خارطة الانتشار اللوجستي")
        # خريطة افتراضية لمراكز الإمارات
        map_df = pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]})
        st.map(map_df)

    # المنطقة 4: عرض البيانات الحية
    st.subheader("📋 مراجعة سجلات العمليات (Order History)")
    st.dataframe(df_orders, use_container_width=True)

else:
    st.error("⚠️ لم أتمكن من ربط البيانات. يرجى التأكد من أسماء الملفات في بيئة العمل.")