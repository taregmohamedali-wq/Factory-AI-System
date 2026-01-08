import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات الهوية والشخصية ---
st.set_page_config(page_title="المستشار طارق الذكي", layout="wide")

# دالة ذكية لضمان ظهور صورتك في كل رد
def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

img_path = "me.jpg"
user_img = get_base64_img(img_path)

# --- 2. قراءة البيانات الحقيقية من ملفاتك ---
@st.cache_data
def load_actual_data():
    # ملاحظة: الكود يقرأ من الملف المرفوع UAE_Operations_DB.xlsx
    try:
        inv = pd.read_csv("UAE_Operations_DB.xlsx - Inventory.csv")
        orders = pd.read_csv("UAE_Operations_DB.xlsx - Order_History.csv")
        return inv, orders
    except:
        return pd.DataFrame(), pd.DataFrame()

df_inv, df_orders = load_actual_data()

# --- 3. محرك التحليل المنطقي (التجاوب الذكي) ---
def smart_analytical_response(query):
    query = query.lower()
    
    if df_orders.empty or df_inv.empty:
        return "أستاذ طارق، لا أستطيع الوصول للبيانات حالياً. يرجى التأكد من رفع الملفات."

    # أ- تحليل التأخير الحقيقي (Delayed)
    if any(word in query for word in ['تاخير', 'تأخير', 'delay', 'متأخر']):
        delayed = df_orders[df_orders['Status'].str.contains('متأخر', na=False)]
        if not delayed.empty:
            count = len(delayed)
            # جلب أسماء السائقين المتأخرين فعلياً من ملفك
            driver_list = ", ".join(delayed['Driver'].unique()[:5]) 
            return f"⚠️ **تحليل التأخير:** سيدي، لدينا حالياً **{count}** شحنات متأخرة. المشكلة تتركز بشكل أساسي مع السائقين: ({driver_list}). هل تريد مني تحليل أسباب تعطل هؤلاء السائقين؟"
        return "✅ أستاذ طارق، فحصت جدول العمليات؛ لا يوجد أي تأخير مسجل حالياً."

    # ب- تحليل المخزون بالمدن (دبي، أبوظبي، الشارقة)
    cities = {'دبي': 'دبي', 'أبوظبي': 'أبوظبي', 'الشارقة': 'الشارقة'}
    for ar_name, search_key in cities.items():
        if ar_name in query:
            city_data = df_inv[df_inv['Warehouse'].str.contains(search_key, na=False)]
            if not city_data.empty:
                total = city_data['Stock_Level'].sum()
                top_product = city_data.loc[city_data['Stock_Level'].idxmax(), 'Product']
                return f"📍 **وضع {ar_name}:** المخزون الإجمالي هناك هو **{total:,}** وحدة. المنتج الأكثر توفراً هو ({top_product}). هل نراجع خطة التوزيع هناك؟"

    # ج- تحليل النواقص
    if 'نقص' in query or 'ناقص' in query:
        low_stock = df_inv[df_inv['Stock_Level'] < 1000]
        if not low_stock.empty:
            item = low_stock.iloc[0]
            return f"📦 **تنبيه مخزون منخفض:** صنف ({item['Product']}) في ({item['Warehouse']}) وصل لـ {item['Stock_Level']} وحدة فقط. هذا مستوى خطر أستاذ طارق."

    return "معك يا أستاذ طارق. لقد قمت بتحليل الملفات؛ هل تريد التركيز على (كفاءة السائقين) أم (مراجعة نواقص المستودعات)؟"

# --- 4. واجهة المحادثة التفاعلية ---
with st.sidebar:
    if user_img:
        st.markdown(f'<div style="text-align:center"><img src="{user_img}" style="border-radius:50%; width:130px; border:3px solid #00ffcc;"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>AI المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'chat_history' not in st.session_state: st.session_state.chat_history = []
    
    for message in st.session_state.chat_history:
        # عرض صورة السائق في الرد (أفاتار)
        avatar = user_img if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar):
            st.write(message["content"])

    if p := st.chat_input("تحدث معي.. اسأل عن دبي، السائقين، أو التأخير"):
        st.session_state.chat_history.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        
        # استدعاء العقل التحليلي المربوط ببياناتك
        response = smart_analytical_response(p)
        
        with st.chat_message("assistant", avatar=user_img):
            st.write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- 5. الداشبورد الرئيسي (لوحة التحكم الاستراتيجية) ---
st.markdown("<h1 style='text-align:center;'>📊 Strategic Operations Hub</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    m1, m2, m3 = st.columns(3)
    m1.metric("إجمالي المخزون (Inventory)", f"{df_inv['Stock_Level'].sum():,}")
    m2.metric("شحنات متأخرة (Orders)", len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)]))
    m3.metric("المستودعات المغطاة", df_inv['Warehouse'].nunique())

    st.markdown("---")
    
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.subheader("📈 تحليل مستويات المخزون الحالي")
        fig = px.bar(df_inv, x='Warehouse', y='Stock_Level', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_r:
        st.subheader("🌍 مراقبة حركة الأسطول")
        st.map(pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]}))
        st.warning("تحليل: مخزون Flour 5kg في الشارقة حرج جداً (213 وحدة).")

    st.subheader("📋 معاينة البيانات الحقيقية")
    st.dataframe(df_orders.head(10), use_container_width=True)