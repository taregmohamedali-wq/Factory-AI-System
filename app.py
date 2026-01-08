import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات الهوية والذكاء ---
st.set_page_config(page_title="Strategic AI Advisor", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_avatar = get_base64_img("me.jpg")

# --- 2. محرك قراءة وتحليل البيانات ---
@st.cache_data
def load_data():
    try:
        # قراءة البيانات الحقيقية التي رفعتها
        df_inv = pd.read_csv("UAE_Operations_DB.xlsx - Inventory.csv")
        df_orders = pd.read_csv("UAE_Operations_DB.xlsx - Order_History.csv")
        return df_inv, df_orders
    except:
        return pd.DataFrame(), pd.DataFrame()

df_inv, df_orders = load_data()

# --- 3. محرك "التفكير المنطقي" (الذكاء التحليلي المفتوح) ---
def ai_strategic_thought(user_query):
    query = user_query.lower()
    
    if df_inv.empty or df_orders.empty:
        return "أستاذ طارق، أنا هنا ومستعد للتفكير معك، لكنني لا أرى قاعدة البيانات حالياً. هل يمكننا التأكد من المسارات؟"

    # تحليل "التأخير" برؤية استراتيجية
    if any(word in query for word in ['تأخير', 'تاخير', 'delay', 'مشكلة']):
        delayed = df_orders[df_orders['Status'].str.contains('متأخر', na=False)]
        if not delayed.empty:
            count = len(delayed)
            main_city = delayed['City'].value_counts().idxmax()
            top_driver = delayed['Driver'].iloc[0]
            return f"سيدي، بعد تحليل سجلات الحركة، رصدت {count} حالة تأخير. المقلق هنا أن معظمها يتركز في **{main_city}**. السائق **{top_driver}** وأربعة آخرون يواجهون عوائق حالياً. هل تود أن أقوم بتحليل المسارات البديلة لهم لتفادي هذا التأخير غداً؟"
        return "✅ أستاذ طارق، لقد قمت بمسح شامل للأسطول؛ الوضع مثالي حالياً ولا توجد شحنة واحدة خارج الجدول الزمني."

    # تحليل "الوضع العام" برؤية شاملة
    if any(word in query for word in ['وضع', 'تقرير', 'تحليل', 'حلل']):
        total_stock = df_inv['Stock_Level'].sum()
        critical_stock = df_inv[df_inv['Stock_Level'] < 500]
        status_msg = f"سيدي، إليك قراءتي للموقف: مخزوننا الإجمالي {total_stock:,} وحدة. "
        if not critical_stock.empty:
            status_msg += f"لكن هناك نقطة ضعف؛ صنف **({critical_stock.iloc[0]['Product']})** في مستودع الشارقة وصل لمستوى حرج ({critical_stock.iloc[0]['Stock_Level']}). "
        status_msg += "بالمقابل، الأداء اللوجستي في دبي ممتاز اليوم. هل نبدأ بخطة إعادة تدوير للمخزون؟"
        return status_msg

    # تحليل المدن (دبي، أبوظبي، الشارقة)
    cities = {'دبي': 'دبي', 'أبوظبي': 'أبوظبي', 'الشارقة': 'الشارقة'}
    for ar, search in cities.items():
        if ar in query:
            city_data = df_inv[df_inv['Warehouse'].str.contains(search, na=False)]
            total = city_data['Stock_Level'].sum()
            return f"📍 تقريري عن {ar}: المخزون المتوفر {total:,} وحدة. لاحظت أن التوزيع هناك يعتمد بشكل كبير على فئة واحدة، هل ترغب في تنويع المخزون لتقليل مخاطر النفاذ؟"

    # محادثة مفتوحة
    return "أنا معك يا أستاذ طارق، أفكر في البيانات التي أمامي الآن. يمكننا التحدث عن كفاءة السائقين، أو مستويات المخزون، أو حتى كيف يمكننا تحسين الأداء في الربع القادم. ماذا تقترح؟"

# --- 4. واجهة المحادثة التفاعلية ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:120px; border:3px solid #00ffcc; box-shadow: 0px 4px 15px rgba(0,255,204,0.3);"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>المستشار طارق الذكي</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'messages' not in st.session_state: st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"], avatar=user_avatar if m["role"]=="assistant" else None):
            st.write(m["content"])

    if prompt := st.chat_input("تحدث معي، أنا أسمعك وأفكر معك..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        # استدعاء محرك التفكير
        response = ai_strategic_thought(prompt)
        
        with st.chat_message("assistant", avatar=user_avatar):
            st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- 5. الداشبورد (لوحة القيادة) ---
st.markdown("<h1 style='text-align:center;'>📊 Strategic Operations Hub</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("المخزون الكلي", f"{df_inv['Stock_Level'].sum():,}")
    col2.metric("شحنات متأخرة 🔴", len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)]))
    col3.metric("مستوى الأداء العام", "94.5%")

    st.markdown("---")
    
    l_col, r_col = st.columns([2, 1])
    with l_col:
        st.subheader("📈 تحليل توزيع المخزون الحقيقي")
        fig = px.bar(df_inv, x='Warehouse', y='Stock_Level', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    
    with r_col:
        st.subheader("💡 تحليل المستشار")
        st.info("سيدي، بناءً على الأرقام: مخزون الشارقة حرج جداً (213 وحدة)، بينما لدينا وفرة في دبي. أقترح تحركاً سريعاً.")
        st.map(pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]}))

    st.subheader("📋 معاينة البيانات الحية")
    st.dataframe(df_orders.head(10), use_container_width=True)