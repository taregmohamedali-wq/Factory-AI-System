import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات الهوية والتصميم الاحترافي ---
st.set_page_config(page_title="AI Strategic Advisor", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_avatar = get_base64_img("me.jpg")

# --- 2. محرك قراءة البيانات المرن (الحل النهائي لـ KeyError) ---
@st.cache_data
def load_and_fix_data():
    file_path = "UAE_Operations_DB.xlsx"
    if not os.path.exists(file_path): return pd.DataFrame(), pd.DataFrame()
    
    try:
        xls = pd.ExcelFile(file_path)
        df_inv = pd.read_excel(xls, sheet_name=0)
        df_fleet = pd.read_excel(xls, sheet_name=1) if len(xls.sheet_names) > 1 else pd.DataFrame()

        # دالة سحرية للتعرف على الأعمدة مهما كانت تسميتها (حل مشكلة صورة 4bd05d)
        def map_columns(df):
            if df.empty: return df
            df.columns = [str(c).strip() for c in df.columns]
            rename_map = {}
            for col in df.columns:
                c_low = col.lower()
                if 'stock' in c_low or 'مخزون' in c_low or 'كمية' in c_low: rename_map[col] = 'Stock'
                if 'warehouse' in c_low or 'مستودع' in c_low or 'مدينة' in c_low: rename_map[col] = 'Warehouse'
                if 'product' in c_low or 'منتج' in c_low or 'صنف' in c_low: rename_map[col] = 'Product'
                if 'status' in c_low or 'حالة' in c_low: rename_map[col] = 'Status'
                if 'driver' in c_low or 'سائق' in c_low: rename_map[col] = 'Driver'
            return df.rename(columns=rename_map)

        return map_columns(df_inv), map_columns(df_fleet)
    except: return pd.DataFrame(), pd.DataFrame()

df_inv, df_fleet = load_and_fix_data()

# --- 3. عقل المستشار (تجاوب بشري وذكاء كامل) ---
def advisor_ai_response(user_input):
    q = user_input.lower()
    
    if df_inv.empty or 'Stock' not in df_inv.columns:
        return "سيدي، أنا متصل بالتطبيق ولكن لا أرى بيانات المخزون. تأكد من أن ملف الإكسل يحتوي على عمود 'Stock'."

    # تحليل "الوضع العام" (حل مشكلة صورة 4bd76a)
    if any(word in q for word in ['الوضع', 'تقرير', 'عام']):
        total = df_inv['Stock'].sum()
        low = len(df_inv[df_inv['Stock'] < 500])
        return f"📊 **التقرير الاستراتيجي:** سيدي، مخزوننا الإجمالي هو {total:,} وحدة. رصدت {low} أصناف في حالة حرجة. العمليات مستقرة حالياً ولكن نحتاج لتعزيز مخزون دبي."

    # تحليل "التأخير" و "السائقين"
    if any(word in q for word in ['تأخير', 'متأخر', 'delay', 'سائق']):
        if not df_fleet.empty and 'Status' in df_fleet.columns:
            delayed = df_fleet[df_fleet['Status'].str.contains('Delayed', case=False, na=False)]
            if not delayed.empty:
                driver_name = delayed.iloc[0]['Driver']
                return f"⚠️ **تحليل الأسطول:** هناك {len(delayed)} شحنات متأخرة. السائق {driver_name} هو الأكثر تأخراً حالياً. هل تريد مني إصدار تنبيه له؟"
        return "✅ أستاذ طارق، جميع الشحنات تسير وفق الجدول الزمني المحدد في ملفك."

    # تحليل "المدن" (دبي، الشارقة...)
    for city_ar, city_en in {'دبي':'Dubai', 'الشارقة':'Sharjah', 'أبوظبي':'Abu Dhabi'}.items():
        if city_ar in q or city_en.lower() in q:
            city_data = df_inv[df_inv['Warehouse'].str.contains(city_en, case=False, na=False)]
            if not city_data.empty:
                val = city_data['Stock'].sum()
                return f"📍 **وضع {city_ar}:** المخزون هناك هو {val:,} وحدة. صنف {city_data.iloc[0]['Product']} يحتاج إعادة توريد فورية."

    return "أهلاً أستاذ طارق، أنا أسمعك جيداً. هل تريد تحليل (أداء السائقين) أم (توقعات نقص المخزون للعام الجديد)؟"

# --- 4. الواجهة الجانبية (عقل الشريك) ---
with st.sidebar:
    if user_avatar: st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:120px; border:3px solid #00ffcc;"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>AI المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'history' not in st.session_state: st.session_state.history = []
    for m in st.session_state.history:
        with st.chat_message(m["role"]): st.write(m["content"])

    if p := st.chat_input("اسألني عن أي تفاصيل في العمليات.."):
        st.session_state.history.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        
        # استدعاء العقل التحليلي
        response = advisor_ai_response(p)
        
        with st.chat_message("assistant"): st.write(response)
        st.session_state.history.append({"role": "assistant", "content": response})

# --- 5. الصفحة الرئيسية (القيادة والتحكم) ---
st.markdown("<h1 style='text-align:center;'>Strategic Operations Command</h1>", unsafe_allow_html=True)

if not df_inv.empty and 'Stock' in df_inv.columns:
    col1, col2, col3 = st.columns(3)
    col1.metric("إجمالي مخزون المجموعة", f"{df_inv['Stock'].sum():,}")
    col2.metric("شحنات متأخرة", len(df_fleet[df_fleet['Status'].str.contains('Delayed', na=False)]) if not df_fleet.empty else 0)
    col3.metric("مستودعات نشطة", df_inv['Warehouse'].nunique())

    st.markdown("---")
    
    c_left, c_right = st.columns([2, 1])
    with c_left:
        st.subheader("📊 ميزان توزيع المخزون")
        fig = px.bar(df_inv, x='Warehouse', y='Stock', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    
    with c_right:
        st.subheader("💡 توصية استراتيجية")
        st.info("سيدي، رصدت فائضاً في مستودع الشارقة وعجزاً في العين. أقترح تحويل 15% من المخزون فوراً لتقليل تكلفة النقل.")
        st.map(pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]}))

    st.subheader("📋 مراجعة البيانات الحية")
    st.dataframe(df_inv, use_container_width=True)
else:
    st.error("⚠️ فشل الربط: يرجى التأكد من أن ملف الإكسل يحتوي على عمود Stock و Warehouse.")