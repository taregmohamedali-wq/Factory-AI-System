import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات الهوية ---
st.set_page_config(page_title="Strategic Operations Hub", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_avatar = get_base64_img("me.jpg")

# --- 2. محرك قراءة البيانات المرن (البحث عن الأعمدة مهما كان اسمها) ---
@st.cache_data
def load_and_map_data():
    file_path = "UAE_Operations_DB.xlsx"
    if not os.path.exists(file_path): return pd.DataFrame(), pd.DataFrame()
    
    xls = pd.ExcelFile(file_path)
    df_inv = pd.read_excel(xls, sheet_name=0)
    df_fleet = pd.read_excel(xls, sheet_name=1) if len(xls.sheet_names) > 1 else pd.DataFrame()

    # تنظيف وتوحيد أسماء الأعمدة لتجنب KeyError
    def clean_columns(df):
        if df.empty: return df
        df.columns = [str(c).strip() for c in df.columns]
        mapping = {}
        for c in df.columns:
            low_c = c.lower()
            if 'stock' in low_c or 'مخزون' in low_c or 'الرصيد' in low_c: mapping[c] = 'Stock'
            if 'warehouse' in low_c or 'مستودع' in low_c or 'مدينة' in low_c: mapping[c] = 'Warehouse'
            if 'product' in low_c or 'منتج' in low_c or 'صنف' in low_c: mapping[c] = 'Product'
            if 'status' in low_c or 'حالة' in low_c: mapping[c] = 'Status'
            if 'driver' in low_c or 'سائق' in low_c: mapping[c] = 'Driver'
        return df.rename(columns=mapping)

    return clean_columns(df_inv), clean_columns(df_fleet)

df_inv, df_fleet = load_and_map_data()

# --- 3. عقل المستشار (الذكاء التفاعلي) ---
def smart_brain(query):
    query = query.lower()
    if df_inv.empty or 'Stock' not in df_inv.columns:
        return "أستاذ طارق، لم أجد عمود المخزون في ملفك. تأكد من تسمية الأعمدة بوضوح (Warehouse, Product, Stock)."

    # تحليل "دبي" أو أي مدينة
    cities = {'دبي': 'Dubai', 'الشارقة': 'Sharjah', 'أبوظبي': 'Abu Dhabi', 'العين': 'Al Ain'}
    for ar, en in cities.items():
        if ar in query or en.lower() in query:
            city_data = df_inv[df_inv['Warehouse'].astype(str).str.contains(en, case=False, na=False)]
            if not city_data.empty:
                total = city_data['Stock'].sum()
                return f"📍 **تقرير {ar}:** سيدي، المخزون الحالي هناك هو {total:,} وحدة. بناءً على بياناتي، الوضع يحتاج لمتابعة في صنف {city_data.iloc[0]['Product']}."

    # تحليل "التأخير"
    if any(word in query for word in ['تاخير', 'تأخير', 'delay', 'متأخر']):
        if not df_fleet.empty and 'Status' in df_fleet.columns:
            delayed = df_fleet[df_fleet['Status'].astype(str).str.contains('Delayed', case=False, na=False)]
            if not delayed.empty:
                return f"⚠️ **تحذير الأسطول:** رصدت {len(delayed)} شحنات متأخرة حالياً. السائق {delayed.iloc[0]['Driver']} يواجه عطلاً في الطريق."
        return "✅ كل الشحنات تسير حسب الجدول، لا يوجد أي تأخير مسجل في ملفك."

    return "أهلاً أستاذ طارق، أنا الآن " + ("مربوط ببياناتك" if not df_inv.empty else "أنتظر الملف") + ". اسألني عن (مخزون مدينة) أو (حالة السائقين)."

# --- 4. واجهة المحادثة (Sidebar) ---
with st.sidebar:
    if user_avatar: st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:120px; border:2px solid #00ffcc;"></div>', unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>AI المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'msgs' not in st.session_state: st.session_state.msgs = []
    for m in st.session_state.msgs:
        with st.chat_message(m["role"]): st.write(m["content"])

    if p := st.chat_input("تحدث معي كخبير استراتيجي.."):
        st.session_state.msgs.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        response = smart_brain(p)
        with st.chat_message("assistant"): st.write(response)
        st.session_state.msgs.append({"role": "assistant", "content": response})

# --- 5. العرض الرئيسي (Dashboard) ---
st.markdown("<h1 style='text-align: center;'>Strategic Operations Command</h1>", unsafe_allow_html=True)

if not df_inv.empty and 'Stock' in df_inv.columns:
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي المخزون المكتشف", f"{df_inv['Stock'].sum():,}")
    c2.metric("عدد المدن", df_inv['Warehouse'].nunique())
    c3.metric("كفاءة الربط", "100%")
    
    st.markdown("---")
    fig = px.bar(df_inv, x='Warehouse', y='Stock', color='Product', barmode='group', template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_inv, use_container_width=True)
else:
    st.error("⚠️ ملف UAE_Operations_DB.xlsx موجود ولكن لم أجد أعمدة (Warehouse, Stock) بداخله.")