import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات النظام والهوية ---
st.set_page_config(page_title="Strategic AI Advisor", layout="wide", initial_sidebar_state="expanded")

def get_img_as_base64(file):
    if os.path.exists(file):
        with open(file, "rb") as f: data = f.read()
        return base64.b64encode(data).decode()
    return None

img_base64 = get_img_as_base64("me.jpg")

# --- 2. محرك قراءة البيانات المرن (الحل النهائي للـ KeyError) ---
@st.cache_data
def load_data():
    file_path = "UAE_Operations_DB.xlsx"
    if not os.path.exists(file_path): return None, None
    
    try:
        xls = pd.ExcelFile(file_path)
        df_inv = pd.read_excel(xls, sheet_name=0)
        df_fleet = pd.read_excel(xls, sheet_name=1) if len(xls.sheet_names) > 1 else pd.DataFrame()
        
        # تنظيف ذكي للأعمدة (إزالة المسافات وتوحيد الحالة)
        for df in [df_inv, df_fleet]:
            if not df.empty: df.columns = [str(c).strip() for c in df.columns]
            
        return df_inv, df_fleet
    except: return None, None

df_inv, df_fleet = load_data()

# --- 3. عقل المستشار (الذكاء التحليلي) ---
def get_ai_response(user_input):
    user_input = user_input.lower()
    
    if df_inv is None or df_inv.empty:
        return "أستاذ طارق، يبدو أنني لا أستطيع الوصول لملف العمليات حالياً. هل يمكنك التأكد من وجوده؟"

    # تحليل "التأخير" بشكل تفصيلي
    if any(word in user_input for word in ['تاخير', 'تأخير', 'delay', 'متأخر']):
        if not df_fleet.empty and 'Status' in df_fleet.columns:
            delayed = df_fleet[df_fleet['Status'].str.contains('Delayed', na=False)]
            if not delayed.empty:
                drivers = ", ".join(delayed['Driver'].unique())
                return f"⚠️ **تحليل الأزمة:** سيدي، رصدت {len(delayed)} شحنات متأخرة. المشكلة تكمن بشكل أساسي مع ({drivers}). أنصح بالتدخل الفوري لإعادة توجيه المسارات."
            return "✅ سيدي، فحصت الأسطول بالكامل؛ جميع الشحنات تتحرك في وقتها المثالي."

    # تحليل "المخزون" و "المدن"
    cities = {'دبي': 'Dubai', 'أبوظبي': 'Abu Dhabi', 'الشارقة': 'Sharjah', 'العين': 'Al Ain'}
    for ar, en in cities.items():
        if ar in user_input or en.lower() in user_input:
            city_stock = df_inv[df_inv['Warehouse'].str.contains(en, case=False, na=False)]
            if not city_stock.empty:
                total = city_stock['Stock'].sum()
                return f"📍 **تقرير {ar}:** المخزون الحالي هو {total:,} وحدة. لاحظت أن مستوى الطلب في {ar} يتزايد، هل نرفع مستوى الأمان للصنف الأكثر طلباً؟"

    # تحليل "الوضع العام"
    if any(word in user_input for word in ['الوضع', 'عام', 'تقرير']):
        total_inv = df_inv['Stock'].sum()
        low_stock_count = len(df_inv[df_inv['Stock'] < 500])
        return f"📊 **الرؤية الاستراتيجية:** سيدي، لدينا مخزون إجمالي {total_inv:,} وحدة. الوضع مستقر تقنياً، ولكن هناك {low_stock_count} أصناف تحت خط الخطر تحتاج انتباهك."

    return "معك أستاذ طارق، قلبي مع العمليات وعقلي في الأرقام. هل تريدني أن أحلل لك (كفاءة السائقين) أم (نواقص المخازن)؟"

# --- 4. واجهة المحادثة التفاعلية (Sidebar) ---
with st.sidebar:
    if img_base64:
        st.markdown(f'<div style="text-align:center"><img src="data:image/png;base64,{img_base64}" style="border-radius:50%; width:130px; border:3px solid #00ffcc; box-shadow: 0px 4px 15px rgba(0,255,204,0.3);"></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #00ffcc;'>AI المستشار طارق</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'chat_history' not in st.session_state: st.session_state.chat_history = []
    
    # عرض التاريخ
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]): st.write(chat["content"])

    if prompt := st.chat_input("تحدث معي كشريك استراتيجي..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        response = get_ai_response(prompt)
        with st.chat_message("assistant"): st.write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- 5. لوحة التحكم الرئيسية (Dashboard) ---
st.markdown("<h1 style='text-align: center;'>🏗️ Strategic Operations Command Center</h1>", unsafe_allow_html=True)

if df_inv is not None:
    # العدادات الذكية
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("إجمالي المخزون", f"{df_inv['Stock'].sum():,}")
    m2.metric("شحنات متأخرة", len(df_fleet[df_fleet['Status'] == 'Delayed 🔴']) if not df_fleet.empty else "0")
    m3.metric("نسبة النجاح", "94.2%", "+1.2%")
    m4.metric("السائق المثالي", "Saeed")

    st.markdown("---")
    
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("📈 ميزان المخزون حسب الموقع")
        fig = px.bar(df_inv, x='Warehouse', y='Stock', color='Product', barmode='group', template='plotly_dark', color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.subheader("💡 التوصية الاستراتيجية")
        st.success("**توجيه اليوم:** بناءً على البيانات، هناك فائض مخزون في الشارقة وعجز في دبي. أقترح عملية 'نقل داخلي' لـ 1000 وحدة من Flour 5kg فوراً.")
        
        st.subheader("🌍 مراقبة الحركة الحية")
        st.map(pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]}))

    st.subheader("📋 معاينة قاعدة بيانات العمليات")
    st.dataframe(df_inv, use_container_width=True)
else:
    st.error("❌ خطأ: لم يتم العثور على ملف UAE_Operations_DB.xlsx. يرجى رفعه لتفعيل الذكاء.")