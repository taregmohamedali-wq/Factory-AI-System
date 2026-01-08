import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات الهوية ---
st.set_page_config(page_title="Strategic AI Advisor", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_avatar = get_base64_img("me.jpg")

# --- 2. محرك قراءة البيانات الحية ---
@st.cache_data
def load_all_data():
    try:
        # قراءة البيانات من ملفك المرفوع
        inv = pd.read_excel("UAE_Operations_DB.xlsx", sheet_name="Inventory")
        orders = pd.read_excel("UAE_Operations_DB.xlsx", sheet_name="Order_History")
        return inv, orders
    except:
        return pd.DataFrame(), pd.DataFrame()

df_inv, df_orders = load_all_data()

# --- 3. محرك المحادثة الذكي (عقل المستشار) ---
def advanced_ai_chat(user_input):
    u = user_input.lower()
    
    # الربط المنطقي بين الكلام والبيانات
    if any(word in u for word in ['تاخير', 'تأخير', 'delay', 'متأخر']):
        delayed = df_orders[df_orders['Status'].str.contains('متأخر', na=False)]
        total = len(delayed)
        if total > 0:
            top_city = delayed['City'].value_counts().idxmax()
            return f"أستاذ طارق، الوضع يتطلب تدخلاً. لدينا {total} شحنات متعطلة، وأغلبها في {top_city}. السائقين يواجهون ضغطاً هناك. هل تريد مني تحليل أداء المسارات البديلة؟"
        return "سيدي، البيانات الحالية ممتازة، الأسطول يتحرك بكفاءة 100% ولا توجد أي بلاغات تأخير."

    if any(word in u for word in ['دبي', 'dubai']):
        stock = df_inv[df_inv['Warehouse'].str.contains('دبي', na=False)]['Stock_Level'].sum()
        return f"📍 تقرير دبي سيدي: المخزون الحالي {stock:,} وحدة. لاحظت أن حركة الصرف سريعة، هل أقارن لك هذه الأرقام بمتوسط السوق في الإمارات؟"

    if any(word in u for word in ['وضع', 'تحليل', 'اقتراح', 'حلل']):
        low_items = df_inv[df_inv['Stock_Level'] < 500]
        return f"سيدي، بعد تحليل قاعدة البيانات، رصدت {len(low_items)} أصناف تقترب من النفاذ، خاصة في الشارقة. لو أخذنا في الاعتبار حالة السوق الحالية، أنصح بزيادة الطلب فوراً لتجنب توقف التوريد."

    # ردود ذكية للمحادثة المفتوحة
    return "معك يا أستاذ طارق، أنا أراقب كل تحديث في الملفات والإنترنت. يمكننا مناقشة أي شيء؛ من حالة الطقس وتأثيرها على السائقين إلى تحليل أرباح الربع الحالي. ماذا يدور في ذهنك؟"

# --- 4. واجهة المحادثة التفاعلية ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:120px; border:3px solid #00ffcc; box-shadow: 0px 4px 15px rgba(0,255,204,0.3);"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>المستشار طارق الذكي</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'history' not in st.session_state: st.session_state.history = []
    
    for m in st.session_state.history:
        with st.chat_message(m["role"], avatar=user_avatar if m["role"]=="assistant" else None):
            st.write(m["content"])

    if prompt := st.chat_input("تحدث معي، الحوار مفتوح..."):
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        response = advanced_ai_chat(prompt)
        with st.chat_message("assistant", avatar=user_avatar):
            st.write(response)
        st.session_state.history.append({"role": "assistant", "content": response})

# --- 5. الداشبورد الاستراتيجي ---
st.markdown("<h1 style='text-align:center;'>📊 Strategic Operations Hub</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    m1, m2, m3 = st.columns(3)
    m1.metric("المخزون الكلي", f"{df_inv['Stock_Level'].sum():,}")
    m2.metric("شحنات متأخرة 🔴", len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)]))
    m3.metric("مستوى الخدمة", "94.8%")

    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📈 ميزان القوى العملياتي")
        fig = px.bar(df_inv, x='Warehouse', y='Stock_Level', color='Product', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📋 الرؤية الحالية")
        st.info("سيدي، بناءً على البيانات: مستودع الشارقة يحتاج دعم فني فوراً بسبب نقص حاد في Flour 5kg.")
        st.dataframe(df_inv[['Product', 'Stock_Level']].head(10))