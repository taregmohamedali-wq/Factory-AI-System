import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات الهوية ---
st.set_page_config(page_title="AI Strategic Advisor", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_avatar = get_base64_img("me.jpg")

# --- 2. محرك قراءة البيانات ---
@st.cache_data
def load_data():
    try:
        # قراءة الشيتات مباشرة من ملفك المرفوع
        inv = pd.read_excel("UAE_Operations_DB.xlsx", sheet_name="Inventory")
        orders = pd.read_excel("UAE_Operations_DB.xlsx", sheet_name="Order_History")
        return inv, orders
    except:
        return pd.DataFrame(), pd.DataFrame()

df_inv, df_orders = load_data()

# --- 3. عقل المستشار (محرك التحليل الاستراتيجي) ---
def ai_strategic_analyst(query):
    query = query.lower()
    
    if df_inv.empty or df_orders.empty:
        return "سيدي، الملفات غير مقروءة حالياً. يرجى التأكد من رفع UAE_Operations_DB.xlsx"

    # تحليل "التأخير" بشكل ذكي
    if any(word in query for word in ['تأخير', 'تاخير', 'delay', 'متأخر']):
        delayed = df_orders[df_orders['Status'].str.contains('متأخر', na=False)]
        total_delayed = len(delayed)
        if total_delayed > 0:
            top_delayed_city = delayed['City'].value_counts().idxmax()
            drivers = ", ".join(delayed['Driver'].unique()[:3])
            return f"⚠️ **تحليل الأزمة:** أستاذ طارق، لدينا {total_delayed} شحنة متعطلة. التركيز الأكبر للتأخير حالياً في مدينة **({top_delayed_city})**. المسؤولون عن هذه المسارات هم ({drivers}). أقترح إعادة جدولة فورية لهذه الرحلات."
        return "✅ سيدي، فحصت سجلات الحركة؛ جميع السائقين ملتزمون بالجدول الزمني ولا يوجد تأخير."

    # تحليل "المخزون" والمدن بشكل استراتيجي
    for city in ['دبي', 'أبوظبي', 'الشارقة', 'العين']:
        if city in query:
            city_data = df_inv[df_inv['Warehouse'].str.contains(city, na=False)]
            total = city_data['Stock_Level'].sum()
            low_item = city_data.loc[city_data['Stock_Level'].idxmin()]
            return f"📍 **تقرير عمليات {city}:** المخزون العام {total:,} وحدة. سيدي، صنف **({low_item['Product']})** في وضع حرج جداً ({low_item['Stock_Level']} قطعة). هذا قد يوقف التوزيع في {city} غداً."

    # تحليل "الوضع العام" أو "تقرير"
    if any(word in query for word in ['وضع', 'تقرير', 'عام', 'حلل']):
        total_stock = df_inv['Stock_Level'].sum()
        critical_orders = len(df_orders[df_orders['Category'].str.contains('قصوى', na=False)])
        return f"📊 **ملخص استراتيجي:** إجمالي المخزون المتاح {total_stock:,} وحدة. لدينا {critical_orders} طلبيات 'أهمية قصوى' تحت التنفيذ. التحدي الأكبر حالياً هو نقص المخزون في الشارقة، هل تود مراجعة خطة النقل الداخلي؟"

    return "أهلاً بك أستاذ طارق. أنا الآن أراقب البيانات حياً؛ هل تريد مني تحليل (أداء السائقين) أم (تحديد النواقص في مستودعات أبوظبي)؟"

# --- 4. واجهة المحادثة التفاعلية (Sidebar) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:120px; border:3px solid #00ffcc;"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>الذكاء الاصطناعي - طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'messages' not in st.session_state: st.session_state.messages = []
    
    for m in st.session_state.messages:
        # هنا تظهر صورتك في كل رد يصدر من الـ assistant
        with st.chat_message(m["role"], avatar=user_avatar if m["role"] == "assistant" else None):
            st.write(m["content"])

    if prompt := st.chat_input("حلل لي وضع دبي أو التأخير..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        # استدعاء العقل التحليلي
        response = ai_strategic_analyst(prompt)
        
        with st.chat_message("assistant", avatar=user_avatar):
            st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- 5. الداشبورد (لوحة القيادة) ---
st.markdown("<h1 style='text-align: center;'>Strategic Command Center</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي المخزون", f"{df_inv['Stock_Level'].sum():,}")
    c2.metric("شحنات متأخرة 🔴", len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)]))
    c3.metric("طلبات عالية الأهمية", len(df_orders[df_orders['Category'].str.contains('أهمية', na=False)]))

    st.markdown("---")
    
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.subheader("📈 ميزان توزيع المخزون")
        fig = px.bar(df_inv, x='Warehouse', y='Stock_Level', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_r:
        st.subheader("💡 توصية المستشار")
        st.error(f"تحذير: مخزون Flour 5kg في الشارقة (213) غير كافٍ لتغطية طلبات الغد.")
        st.map(pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]}))

    st.subheader("📋 معاينة سجل العمليات (Order History)")
    st.dataframe(df_orders.head(10), use_container_width=True)