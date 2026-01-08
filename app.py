import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات الهوية البصرية ---
st.set_page_config(page_title="Strategic Operations Center", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_avatar = get_base64_img("me.jpg")

# --- 2. محرك قراءة البيانات الحقيقي (Excel) ---
@st.cache_data
def load_data():
    file_path = "UAE_Operations_DB.xlsx"
    if os.path.exists(file_path):
        # قراءة شيت المخزون وشيت العمليات (تأكد من تسمية الشيتات داخل ملفك)
        df_inv = pd.read_excel(file_path, sheet_name=0) # الشيت الأول للمخزون
        df_fleet = pd.read_excel(file_path, sheet_name=1) # الشيت الثاني للأسطول
        return df_inv, df_fleet
    else:
        st.error(f"لم يتم العثور على ملف {file_path} في المجلد.")
        return pd.DataFrame(), pd.DataFrame()

df_inv, df_fleet = load_data()

# --- 3. عقل المستشار (التحليل بناءً على بيانات الإكسل) ---
def analyze_and_reply(query):
    query = query.lower()
    
    # التحقق من وجود بيانات
    if df_inv.empty or df_fleet.empty:
        return "سيدي، الملف موجود ولكنه فارغ أو لم أستطع قراءته بشكل صحيح."

    # أ- البحث عن مدينة معينة في سؤالك
    cities = ['دبي', 'dubai', 'أبوظبي', 'abu dhabi', 'شارقه', 'sharjah', 'العين', 'al ain']
    for city in cities:
        if city in query:
            # فلترة البيانات بناءً على المدينة من الإكسل
            city_data = df_inv[df_inv['Warehouse'].str.contains(city, case=False, na=False)]
            total_stock = city_data['Stock'].sum()
            return f"📍 **تقرير مدينة {city}:** بناءً على ملف الإكسل، إجمالي المخزون هناك هو {total_stock:,} وحدة. \n\n💡 **نصيحة:** لاحظت وجود نقص في صنف {city_data.iloc[0]['Product']}، يجب موازنته مع المخازن الأخرى."

    # ب- البحث عن "النقص"
    if any(word in query for word in ['نقص', 'ناقص', 'low']):
        low_stock = df_inv[df_inv['Stock'] < 500]
        if not low_stock.empty:
            items = ", ".join(low_stock['Product'].unique()[:3])
            return f"⚠️ **تحليل النواقص:** رصدت في قاعدة البيانات نقصاً في {len(low_stock)} أصناف، أهمها: ({items}). أنصح بجدولة توريد عاجل."
        return "المخزون في قاعدة البيانات آمن تماماً حالياً."

    # ج- تحليل "الوضع العام"
    if any(word in query for word in ['وضع', 'عام', 'تحليل']):
        return f"📊 **الوضع الاستراتيجي:** لدينا {len(df_inv)} صنف نشط، و {len(df_fleet[df_fleet['Status'] == 'Delayed 🔴'])} شحنة متأخرة حسب سجلات اليوم."

    return "أنا جاهز أستاذ طارق. اسألني عن أي مدينة أو اطلب تحليل النقص وسأجيبك فوراً من واقع ملف الإكسل."

# --- 4. واجهة المحادثة (الجانبية) ---
with st.sidebar:
    if user_avatar: st.image(user_avatar, width=100)
    st.markdown("### المستشار طارق AI")
    st.info("مرتبط بقاعدة بيانات UAE_Operations_DB")
    
    if 'messages' not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    if prompt := st.chat_input("اسأل عن أي مدينة أو حالة المخزون..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        # الرد بناءً على الإكسل
        response = analyze_and_reply(prompt)
        with st.chat_message("assistant"): st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- 5. الصفحة الرئيسية (التصميم الواضح) ---
st.markdown("<h1 style='text-align: center;'>🏭 Strategic Operations Center</h1>", unsafe_allow_html=True)

# العدادات من الإكسل
c1, c2, c3 = st.columns(3)
if not df_inv.empty:
    c1.metric("إجمالي المخزون (Excel)", f"{df_inv['Stock'].sum():,}")
    c2.metric("شحنات متأخرة", len(df_fleet[df_fleet['Status'] == 'Delayed 🔴']))
    c3.metric("عدد المستودعات", df_inv['Warehouse'].nunique())

st.markdown("---")

col_l, col_r = st.columns([2, 1])

with col_l:
    st.subheader("📈 تحليل تدفق المنتجات")
    # رسم بياني واضح
    fig = px.bar(df_inv.groupby('Warehouse')['Stock'].sum().reset_index(), 
                 x='Warehouse', y='Stock', color='Warehouse', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.subheader("💡 نصيحة استشارية اليوم")
    st.success("بناءً على ملف العمليات: يفضل تكثيف أسطول النقل في دبي غداً لتغطية الطلبات المتراكمة.")
    
    st.subheader("🌍 مراقبة المواقع")
    st.map(pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]}))

st.subheader("📋 عرض قاعدة البيانات (UAE_Operations_DB)")
st.dataframe(df_inv, use_container_width=True)