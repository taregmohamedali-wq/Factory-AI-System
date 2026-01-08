import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات الهوية ---
st.set_page_config(page_title="Strategic Hub - Tarik", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_img = get_base64_img("me.jpg")

# --- 2. قراءة البيانات الحقيقية (التي أرفقتها) ---
@st.cache_data
def load_data():
    try:
        # الربط بملفاتك المرفوعة بدقة
        df_inv = pd.read_csv("UAE_Operations_DB.xlsx - Inventory.csv")
        df_orders = pd.read_csv("UAE_Operations_DB.xlsx - Order_History.csv")
        return df_inv, df_orders
    except Exception as e:
        return pd.DataFrame(), pd.DataFrame()

df_inv, df_orders = load_data()

# --- 3. عقل المستشار (الاستجابة المنطقية) ---
def smart_advisor(query):
    query = query.lower()
    if df_inv.empty or df_orders.empty:
        return "سيدي، النظام لا يرى الملفات حالياً. تأكد من وجود الملفات في المسار الصحيح."

    # أ- تحليل التأخير (من واقع ملف Order_History)
    if any(word in query for word in ['تأخير', 'متأخر', 'delay']):
        delayed = df_orders[df_orders['Status'].str.contains('متأخر', na=False)]
        if not delayed.empty:
            return f"⚠️ **تقرير التأخير:** سيدي، رصدت {len(delayed)} شحنة متأخرة. السائقين الأكثر تأثيراً هم {', '.join(delayed['Driver'].unique()[:3])}. هل نراجع الأسباب؟"
        return "✅ أستاذ طارق، لا يوجد أي تأخير مسجل في السجلات الحالية."

    # ب- تحليل المخزون (من واقع ملف Inventory)
    if 'دبي' in query or 'dubai' in query:
        dubai_stock = df_inv[df_inv['Warehouse'].str.contains('دبي', na=False)]['Stock_Level'].sum()
        return f"📍 **مخزون دبي:** المجموع الحالي هو {dubai_stock:,} وحدة. الوضع مستقر بشكل عام."

    return "أنا معك أستاذ طارق، الداشبورد يعمل الآن بالبيانات الحقيقية. هل تريد تحليل (أداء السائقين) أم (نواقص المستودعات)؟"

# --- 4. واجهة المحادثة (Sidebar) ---
with st.sidebar:
    if user_img:
        st.markdown(f'<div style="text-align:center"><img src="{user_img}" style="border-radius:50%; width:120px; border:3px solid #00ffcc;"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>AI المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'chat_history' not in st.session_state: st.session_state.chat_history = []
    
    for m in st.session_state.chat_history:
        # استخدام صورتك كأفاتار في كل رد
        with st.chat_message(m["role"], avatar=user_img if m["role"]=="assistant" else None):
            st.write(m["content"])

    if prompt := st.chat_input("تحدث معي.."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        response = smart_advisor(prompt)
        with st.chat_message("assistant", avatar=user_img): st.write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- 5. الداشبورد الرئيسي (الذي لم يكن يظهر) ---
st.markdown("<h1 style='text-align:center;'>📊 Strategic Operations Center</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    # العدادات الحقيقية
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي المخزون", f"{df_inv['Stock_Level'].sum():,}")
    c2.metric("طلبات متأخرة 🔴", len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)]))
    c3.metric("المستودعات المغطاة", df_inv['Warehouse'].nunique())

    st.markdown("---")
    
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.subheader("📈 مستويات المخزون الحقيقية")
        fig = px.bar(df_inv, x='Warehouse', y='Stock_Level', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_r:
        st.subheader("💡 الرؤية الاستراتيجية")
        # تحليل تلقائي للنواقص
        low_stock_item = df_inv.loc[df_inv['Stock_Level'].idxmin()]
        st.error(f"تنبيه: مخزون {low_stock_item['Product']} في {low_stock_item['Warehouse']} منخفض جداً ({low_stock_item['Stock_Level']})!")
        st.map(pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]}))

    st.subheader("📋 معاينة سجل العمليات المرفوع")
    st.dataframe(df_orders.head(10), use_container_width=True)
else:
    st.error("⚠️ لم أتمكن من قراءة البيانات. تأكد من رفع ملفات CSV المرفقة بجانب الكود.")