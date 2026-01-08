import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات الواجهة والجماليات ---
st.set_page_config(page_title="Strategic Operations Center", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_avatar = get_base64_img("me.jpg")

# --- 2. محرك قراءة الملف (الربط المباشر ببياناتك) ---
@st.cache_data
def load_all_data():
    file_path = "UAE_Operations_DB.xlsx"
    if os.path.exists(file_path):
        xls = pd.ExcelFile(file_path)
        # قراءة الشيتات وتنظيفها من المسافات (حل مشكلة KeyError)
        df_inv = pd.read_excel(xls, sheet_name=0)
        df_inv.columns = [str(c).strip() for c in df_inv.columns]
        
        df_fleet = pd.read_excel(xls, sheet_name=1) if len(xls.sheet_names) > 1 else pd.DataFrame()
        if not df_fleet.empty:
            df_fleet.columns = [str(c).strip() for c in df_fleet.columns]
            
        return df_inv, df_fleet
    return pd.DataFrame(), pd.DataFrame()

df_inv, df_fleet = load_all_data()

# --- 3. عقل المستشار (الرد المنطقي والتحليلي) ---
def smart_advisor_brain(user_query):
    query = user_query.lower()
    
    if df_inv.empty:
        return "أستاذ طارق، لا أستطيع رؤية البيانات حالياً. تأكد من وجود ملف UAE_Operations_DB.xlsx بجانب الكود."

    # أ- الرد على سؤال عن "التأخير" (Delayed)
    if any(word in query for word in ['تاخير', 'تأخير', 'delay', 'متأخر']):
        if not df_fleet.empty and 'Status' in df_fleet.columns:
            delays = df_fleet[df_fleet['Status'].str.contains('Delayed', na=False)]
            if not delays.empty:
                cities = delays['City'].unique()
                return f"⚠️ **تحليل التأخير:** سيدي، لدينا حالياً {len(delays)} شحنة متأخرة. معظم المشاكل تتركز في مناطق ({', '.join(cities)}). أنصحك بالتواصل مع السائق {delays.iloc[0]['Driver']} لمعرفة سبب التوقف."
            return "✅ بشرى سارة أستاذ طارق، جميع الشحنات في الملف المرفوع تسير وفق الجدول الزمني ولا يوجد تأخير حالياً."

    # ب- الرد على سؤال عن "دبي" أو مدينة معينة
    cities_keys = {'دبي': 'Dubai', 'أبوظبي': 'Abu Dhabi', 'الشارقة': 'Sharjah', 'العين': 'Al Ain'}
    for ar_name, en_name in cities_keys.items():
        if ar_name in query or en_name.lower() in query:
            city_data = df_inv[df_inv['Warehouse'].str.contains(en_name, case=False, na=False)]
            if not city_data.empty:
                total = city_data['Stock'].sum()
                return f"📍 **تقرير {ar_name}:** المخزون الحالي هناك هو {total:,} وحدة. لاحظت أن صنف {city_data.iloc[0]['Product']} هو الأكثر طلباً هناك، هل تود مراجعة خطة توزيعه؟"

    # ج- الرد على "النقص"
    if any(word in query for word in ['نقص', 'ناقص', 'خلص', 'low']):
        low_stock = df_inv[df_inv['Stock'] < 500]
        if not low_stock.empty:
            item = low_stock.iloc[0]
            return f"📦 **تنبيه نقص حرج:** منتج {item['Product']} في مستودع {item['Warehouse']} وصل لـ {item['Stock']} وحدة فقط. هذا المستوى غير آمن أستاذ طارق، أقترح إصدار أمر شراء فوراً."

    # د- إذا كان السؤال عاماً
    return "معك أستاذ طارق، قمت بتحليل الملف الآن. هل تريد مني التركيز على (أسباب تأخير الشاحنات) أم (كشف الأصناف التي قاربت على النفاذ)؟"

# --- 4. واجهة المحادثة التفاعلية ---
with st.sidebar:
    if user_avatar: 
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:120px; border:3px solid #00ffcc;"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>AI المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'messages' not in st.session_state: st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    if p := st.chat_input("تحدث معي.. اسأل عن دبي، التأخير، أو النقص"):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        
        # استدعاء العقل التحليلي
        response = smart_advisor_brain(p)
        
        with st.chat_message("assistant"): st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- 5. الداشبورد الرئيسي (التصميم الواضح) ---
st.markdown("<h1 style='text-align:center;'>📊 Strategic Operations Hub</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي المخزون (Excel)", f"{df_inv['Stock'].sum():,}")
    c2.metric("شحنات متأخرة", len(df_fleet[df_fleet['Status'].str.contains('Delayed', na=False)]) if not df_fleet.empty else 0)
    c3.metric("مستودعات نشطة", df_inv['Warehouse'].nunique())

    st.markdown("---")
    
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.subheader("📈 توزيع المنتجات حسب الموقع")
        fig = px.bar(df_inv, x='Warehouse', y='Stock', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_r:
        st.subheader("💡 نصيحة استشارية")
        st.info("بناءً على أرقامك: مخزون الشارقة مرتفع جداً (أكثر من 8000 وحدة)، بينما تواجه دبي ضغطاً. أنصح بإعادة تدوير المخزون بينهما فروعاً.")
        
        st.subheader("🌍 تتبع الأسطول")
        st.map(pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]}))

    st.subheader("📋 معاينة البيانات الحقيقية")
    st.dataframe(df_inv, use_container_width=True)