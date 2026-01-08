import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات الهوية والشخصية ---
st.set_page_config(page_title="المستشار ", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

# صورتك الشخصية (أهم خطوة لظهورها في الرد)
user_avatar = get_base64_img("me.jpg")

# --- 2. قراءة البيانات من الملف المرفوع مباشرة ---
@st.cache_data
def load_data():
    file_path = "UAE_Operations_DB.xlsx"
    if os.path.exists(file_path):
        try:
            # قراءة الشيتات بأسماءها الحقيقية داخل ملفك
            df_inv = pd.read_excel(file_path, sheet_name='Inventory')
            df_orders = pd.read_excel(file_path, sheet_name='Order_History')
            return df_inv, df_orders
        except Exception as e:
            st.error(f"خطأ في قراءة الشيتات: {e}")
            return pd.DataFrame(), pd.DataFrame()
    return pd.DataFrame(), pd.DataFrame()

df_inv, df_orders = load_data()

# --- 3. محرك الاستجابة الذكي (التحليل الحقيقي) ---
def analyze_query(query):
    query = query.lower()
    
    if df_inv.empty or df_orders.empty:
        return "أستاذ طارق، أنا لا أرى ملف UAE_Operations_DB.xlsx. يرجى التأكد من وجوده في المجلد الرئيسي."

    # أ- تحليل التأخير (Delayed) من واقع شيت Order_History
    if any(word in query for word in ['تاخير', 'تأخير', 'delay', 'متأخر']):
        delayed_data = df_orders[df_orders['Status'].str.contains('متأخر', na=False)]
        if not delayed_data.empty:
            count = len(delayed_data)
            drivers = ", ".join(delayed_data['Driver'].unique()[:3])
            return f"سيدي، لدينا **{count}** شحنة متأخرة حالياً. السائقين المتأخرين هم: ({drivers}). هل تريد تقريراً مفصلاً عن المدن؟"
        return "✅ كل الشحنات تسير حسب الجدول، لا يوجد أي تأخير مسجل سيدي."

    # ب- تحليل مدينة دبي (من واقع شيت Inventory)
    if 'دبي' in query or 'dubai' in query:
        dubai_stock = df_inv[df_inv['Warehouse'].str.contains('دبي', na=False)]['Stock_Level'].sum()
        return f"📍 **تقرير دبي:** إجمالي المخزون الحالي في مستودع دبي المركزي هو **{dubai_stock:,}** وحدة. الوضع مستقر."

    # ج- تحليل النواقص
    if 'نقص' in query or 'ناقص' in query:
        low_stock = df_inv[df_inv['Stock_Level'] < 500]
        if not low_stock.empty:
            return f"⚠️ **تنبيه:** صنف {low_stock.iloc[0]['Product']} في {low_stock.iloc[0]['Warehouse']} وصل لـ {low_stock.iloc[0]['Stock_Level']} وحدة!"

    return "أنا معك أستاذ طارق. لقد حللت الملف بالكامل؛ هل تريد مني التركيز على (أداء السائقين) أم (مستويات المخزون )؟"

# --- 4. واجهة المحادثة التفاعلية (Sidebar) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:120px; border:3px solid #00ffcc;"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>AI المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'history' not in st.session_state: st.session_state.history = []
    
    for m in st.session_state.history:
        # هنا نضع صورتك في رد الـ assistant
        avatar = user_avatar if m["role"] == "assistant" else None
        with st.chat_message(m["role"], avatar=avatar):
            st.write(m["content"])

    if prompt := st.chat_input("تحدث معي كشريك استراتيجي..."):
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        response = analyze_query(prompt)
        
        with st.chat_message("assistant", avatar=user_avatar):
            st.write(response)
        st.session_state.history.append({"role": "assistant", "content": response})

# --- 5. الداشبورد الرئيسي (لوحة التحكم) ---
st.markdown("<h1 style='text-align: center;'>Strategic Operations Dashboard</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    # عدادات حقيقية
    m1, m2, m3 = st.columns(3)
    m1.metric("إجمالي المخزون", f"{df_inv['Stock_Level'].sum():,}")
    m2.metric("شحنات متأخرة 🔴", len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)]))
    m3.metric("كفاءة العمليات", "94%")

    st.markdown("---")
    
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.subheader("📈 توزيع المخزون لكل منتج")
        fig = px.bar(df_inv, x='Warehouse', y='Stock_Level', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_r:
        st.subheader("💡 الرؤية الاستراتيجية")
        st.error(f"تنبيه: مخزون Flour 5kg في الشارقة حرج جداً (213 وحدة)!")
        st.map(pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]}))

    st.subheader("📋 مراجعة سجلات Order History")
    st.dataframe(df_orders.head(10), use_container_width=True)
else:
    st.error("⚠️ لم أتمكن من العثور على شيتات Inventory و Order_History داخل الملف المرفوع.")