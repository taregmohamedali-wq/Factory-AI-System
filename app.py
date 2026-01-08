import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات الهوية والتصميم ---
st.set_page_config(page_title="Strategic AI Advisor", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_avatar = get_base64_img("me.jpg")

# --- 2. محرك قراءة البيانات (الحل النهائي لخطأ KeyError) ---
@st.cache_data
def load_and_clean_data():
    file_path = "UAE_Operations_DB.xlsx"
    if os.path.exists(file_path):
        xls = pd.ExcelFile(file_path)
        df_inv = pd.read_excel(xls, sheet_name=0)
        # تنظيف آلي لأسماء الأعمدة لضمان عدم حدوث الخطأ الأحمر
        df_inv.columns = [str(c).strip() for c in df_inv.columns]
        
        df_fleet = pd.read_excel(xls, sheet_name=1) if len(xls.sheet_names) > 1 else pd.DataFrame()
        if not df_fleet.empty:
            df_fleet.columns = [str(c).strip() for c in df_fleet.columns]
        return df_inv, df_fleet
    return pd.DataFrame(), pd.DataFrame()

df_inv, df_fleet = load_and_clean_data()

# --- 3. عقل المستشار (تجاوب ذكي ومنطقي) ---
def smart_advisor(query):
    query = query.lower()
    
    if df_inv.empty:
        return "سيدي، لم أستطع قراءة ملف العمليات. تأكد من رفعه بشكل صحيح على GitHub."

    # أ- تحليل التأخير (رد مفصل)
    if any(word in query for word in ['تاخير', 'تأخير', 'delay', 'متأخر']):
        if not df_fleet.empty and 'Status' in df_fleet.columns:
            delayed = df_fleet[df_fleet['Status'].str.contains('Delayed', na=False)]
            if not delayed.empty:
                names = ", ".join(delayed['Driver'].unique())
                return f"⚠️ **تقرير التأخير:** أستاذ طارق، رصدت {len(delayed)} شحنات متأخرة حالياً. المشكلة تتركز مع السائقين ({names}). هل ترغب في أن أقوم بجدولة اتصال معهم؟"
            return "✅ سيدي، فحصت حالة الأسطول الآن؛ جميع الشحنات تسير في وقتها المحدد."

    # ب- تحليل المدن (دبي، الشارقة، إلخ)
    cities = {'دبي': 'Dubai', 'الشارقة': 'Sharjah', 'أبوظبي': 'Abu Dhabi', 'العين': 'Al Ain'}
    for ar, en in cities.items():
        if ar in query or en.lower() in query:
            data = df_inv[df_inv['Warehouse'].str.contains(en, case=False, na=False)]
            if not data.empty:
                total = data['Stock'].sum()
                return f"📍 **وضع {ar}:** المخزون الحالي هو {total:,} وحدة. لاحظت أن صنف '{data.iloc[0]['Product']}' لديه أعلى مخزون هناك. هل نتحقق من معدل التوزيع؟"

    # ج- رد ذكي عام
    return f"معك يا أستاذ طارق. قمت بمسح بيانات {len(df_inv)} صنف مخزني حالاً. هل نبدأ بتحليل (النواقص الحرجة) أم (مراقبة السائقين المتأخرين)؟"

# --- 4. واجهة الشات التفاعلية (Sidebar) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:120px; border:3px solid #00ffcc;"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>AI المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'history' not in st.session_state: st.session_state.history = []
    
    for m in st.session_state.history:
        with st.chat_message(m["role"]): st.write(m["content"])

    if prompt := st.chat_input("تحدث معي.. اسأل عن دبي أو التأخير"):
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        # استدعاء العقل الذكي
        res = smart_advisor(prompt)
        
        with st.chat_message("assistant"): st.write(res)
        st.session_state.history.append({"role": "assistant", "content": res})

# --- 5. الصفحة الرئيسية (الداشبورد الواضح) ---
st.markdown("<h1 style='text-align: center;'>📊 Strategic Operations Hub</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    # العدادات من واقع الملف
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي المخزون بالملف", f"{df_inv['Stock'].sum():,}")
    c2.metric("شحنات متأخرة", len(df_fleet[df_fleet['Status'].str.contains('Delayed', na=False)]) if not df_fleet.empty else 0)
    c3.metric("المستودعات النشطة", df_inv['Warehouse'].nunique())

    st.markdown("---")
    
    # الرسم البياني الواضح
    st.subheader("📈 توزيع المخزون (تحليل مرئي)")
    fig = px.bar(df_inv, x='Warehouse', y='Stock', color='Product', barmode='group', template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 معاينة البيانات المربوطة")
    st.dataframe(df_inv, use_container_width=True)