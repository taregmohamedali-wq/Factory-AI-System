import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. بناء الشخصية الاستراتيجية ---
st.set_page_config(page_title="Strategic AI Partner", layout="wide")

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
        # الربط المباشر بملفات الإكسل المرفوعة سلفاً
        inv = pd.read_csv("UAE_Operations_DB.xlsx - Inventory.csv")
        orders = pd.read_csv("UAE_Operations_DB.xlsx - Order_History.csv")
        return inv, orders
    except:
        return pd.DataFrame(), pd.DataFrame()

df_inv, df_orders = load_all_data()

# --- 3. محرك "الذكاء الاستنتاجي" (الرد حسب السياق) ---
def advanced_thinking_engine(user_input):
    if df_inv.empty or df_orders.empty:
        return "أستاذ طارق، الملفات غير مقروءة. تأكد من وجودها في المسار الصحيح لنبدأ التحليل."

    u = user_input.lower()
    
    # تحضير "الحقائق" للذكاء الاصطناعي
    delayed_df = df_orders[df_orders['Status'].str.contains('متأخر', na=False)]
    low_stock_df = df_inv[df_inv['Stock_Level'] < 500]
    
    # الحالة 1: سؤال عن "ماذا يحدث؟" أو "تحليل عام"
    if any(word in u for word in ['ماذا', 'وضع', 'تقرير', 'حلل', 'نصيحة']):
        msg = "### 🛡️ رؤيتي للموقف الحالي سيدي:\n\n"
        if not delayed_df.empty:
            worst_city = delayed_df['City'].value_counts().idxmax()
            msg += f"أستاذ طارق، هناك خلل في سلاسل التوريد المتجهة إلى **{worst_city}**. لدينا {len(delayed_df)} شحنة عالقة. "
        
        if not low_stock_df.empty:
            item = low_stock_df.iloc[0]
            msg += f"بالتوازي مع ذلك، رصدت نقصاً حاداً في **{item['Product']}** بمستودع {item['Warehouse']}. \n\n"
            msg += f"💡 **القرار المقترح:** لا ننتظر حتى الغد؛ اقترح تحويل شحنة تعويضية من دبي الآن، واستدعاء السائقين المسؤولين عن مسار {worst_city} للتحقيق في سبب التعطيل."
        return msg

    # الحالة 2: سؤال عن "المدن" أو "المناطق"
    for city in ['دبي', 'أبوظبي', 'الشارقة', 'العين']:
        if city in u:
            city_stock = df_inv[df_inv['Warehouse'].str.contains(city, na=False)]['Stock_Level'].sum()
            city_delays = len(df_orders[(df_orders['City'].str.contains(city, na=False)) & (df_orders['Status'].str.contains('متأخر', na=False))])
            return f"📍 **تحليل منطقة {city}:** المخزون هناك {city_stock:,} وحدة. المقلق هو وجود {city_delays} شحنات متأخرة. هل تود أن أعرض لك قائمة السائقين المتأخرين في {city} الآن؟"

    # الحالة 3: حوار مفتوح (إجابات ذكية غير مبرمجة)
    return f"أسمعك جيداً يا أستاذ طارق. أنا الآن أراقب {len(df_inv)} صنفاً في المخازن و {len(df_orders)} رحلة على الطريق. هل تريدني أن أركز على (تقليل الهالك في المخزون) أم (تحسين زمن وصول السائقين)؟"

# --- 4. واجهة المحادثة التفاعلية (Sidebar) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:110px; border:3px solid #00ffcc;"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'messages' not in st.session_state: st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"], avatar=user_avatar if m["role"]=="assistant" else None):
            st.write(m["content"])

    if prompt := st.chat_input("تحدث معي كشريك عمل.. ماذا يدور بذهنك؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        # استدعاء محرك التفكير المطور
        response = advanced_thinking_engine(prompt)
        with st.chat_message("assistant", avatar=user_avatar): st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- 5. الداشبورد الاحترافي (الخريطة والرسوم) ---
st.markdown("<h1 style='text-align:center;'>📊 Operations Strategic Command</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    # المنطقة 1: النصيحة الاستراتيجية الحية (تظهر فوراً بناءً على البيانات)
    st.info(advanced_thinking_engine("تحليل عام"))
    
    st.markdown("---")
    
    # المنطقة 2: مؤشرات الأداء (KPIs)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("إجمالي المخزون", f"{df_inv['Stock_Level'].sum():,}")
    k2.metric("شحنات متأخرة 🔴", len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)]))
    k3.metric("تغطية الأسطول", f"{len(df_orders)} رحلة")
    k4.metric("كفاءة العمليات", "89%", "-2%")

    st.markdown("---")
    
    # المنطقة 3: الرسوم البيانية والخريطة
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.subheader("📈 توازن المخزون بين المناطق والمنتجات")
        fig = px.bar(df_inv, x='Warehouse', y='Stock_Level', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
        
    with col_r:
        st.subheader("📍 خارطة المراكز اللوجستية")
        map_data = pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]})
        st.map(map_data)

    st.subheader("📋 سجل العمليات الحي (Order History)")
    st.dataframe(df_orders, use_container_width=True)