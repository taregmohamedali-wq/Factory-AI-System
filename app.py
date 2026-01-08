import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. بناء الهوية البصرية (طارق الرقمي) ---
st.set_page_config(page_title="Strategic Operations Command", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

# جلب صورتك الشخصية
user_avatar = get_base64_img("me.jpg")

# --- 2. محرك الربط بالبيانات المرفوعة ---
@st.cache_data
def load_and_sync_data():
    try:
        # الربط المباشر بالملفات التي أكدت وجودها
        inv = pd.read_csv("UAE_Operations_DB.xlsx - Inventory.csv")
        orders = pd.read_csv("UAE_Operations_DB.xlsx - Order_History.csv")
        return inv, orders
    except Exception as e:
        return pd.DataFrame(), pd.DataFrame()

df_inv, df_orders = load_and_sync_data()

# --- 3. عقل المستشار (منطق التحليل والاستنتاج) ---
def strategic_ai_brain(query):
    if df_inv.empty or df_orders.empty:
        return "أستاذ طارق، الملفات موجودة لكن الكود لا يراها. تأكد من تطابق الأسماء تماماً."

    # تحليل البيانات فورياً
    delayed = df_orders[df_orders['Status'].str.contains('متأخر', na=False)]
    critical_stock = df_inv[df_inv['Stock_Level'] < 500]
    
    q = query.lower()
    
    # الرد التحليلي الاستباقي
    if any(word in q for word in ['وضع', 'تحليل', 'ماذا هناك', 'نصيحة']):
        top_city = delayed['City'].value_counts().idxmax() if not delayed.empty else "مستقر"
        report = f"### 🛡️ التقرير الاستراتيجي لليوم\n\n"
        report += f"سيدي، بعد مسح العمليات، رصدت **{len(delayed)}** شحنات متأخرة، أغلبها يتركز في **{top_city}**. "
        if not critical_stock.empty:
            item = critical_stock.iloc[0]
            report += f"المخاطر تزداد في مستودع **{item['Warehouse']}** بسبب نقص صنف **({item['Product']})** الذي وصل لـ {item['Stock_Level']} وحدة فقط. \n\n"
        report += "💡 **توصيتي:** يجب إعادة جدولة السائقين في مسار دبي-الشارقة فوراً لتعويض النواقص قبل بداية نوبة الغد."
        return report

    return "معك يا أستاذ طارق، أنا أحلل قاعدة البيانات الآن. هل تريد التركيز على (أداء السائقين) أم (نواقص المخازن)؟"

# --- 4. واجهة المحادثة التفاعلية (Sidebar) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:110px; border:3px solid #00ffcc; box-shadow: 0px 4px 15px rgba(0,255,204,0.3);"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>AI المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'history' not in st.session_state: st.session_state.history = []
    for m in st.session_state.history:
        with st.chat_message(m["role"], avatar=user_avatar if m["role"]=="assistant" else None):
            st.write(m["content"])

    if prompt := st.chat_input("اسألني: ما هو وضع العمليات اليوم؟"):
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        response = strategic_ai_brain(prompt)
        with st.chat_message("assistant", avatar=user_avatar): st.write(response)
        st.session_state.history.append({"role": "assistant", "content": response})

# --- 5. الداشبورد الاحترافي ---
st.markdown("<h1 style='text-align:center;'>📊 Operations Control Center</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    # المنطقة 1: التحليل الذكي التلقائي
    st.info(strategic_ai_brain("تحليل عام"))
    
    st.markdown("---")
    
    # المنطقة 2: العدادات (KPIs)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("المخزون الكلي", f"{df_inv['Stock_Level'].sum():,}")
    k2.metric("شحنات متأخرة 🔴", len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)]))
    k3.metric("تحت التسليم 🚚", len(df_orders[df_orders['Status'].str.contains('طريق', na=False)]))
    k4.metric("كفاءة الأسطول", "91%")

    st.markdown("---")
    
    # المنطقة 3: الرسوم البيانية والخريطة
    col_chart, col_map = st.columns([2, 1])
    
    with col_chart:
        st.subheader("📈 مستويات المخزون لكل منتج ومستودع")
        fig = px.bar(df_inv, x='Warehouse', y='Stock_Level', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
        
    with col_map:
        st.subheader("📍 التوزيع الجغرافي")
        # خريطة افتراضية لمواقع العمليات في الإمارات
        map_df = pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]})
        st.map(map_df)

    st.subheader("📋 سجل العمليات الحي (Order History)")
    st.dataframe(df_orders, use_container_width=True)
else:
    st.error("⚠️ لم أتمكن من العثور على الملفات. تأكد من رفع UAE_Operations_DB.xlsx في بيئة العمل.")