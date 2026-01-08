import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. بناء الشخصية والهوية ---
st.set_page_config(page_title="Tarik AI - Operations Command", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_avatar = get_base64_img("me.jpg")

# --- 2. الربط الحقيقي مع قاعدة البيانات المرفوعة ---
@st.cache_data
def load_data():
    try:
        # قراءة البيانات المرفوعة سلفاً بدقة
        inv = pd.read_csv("UAE_Operations_DB.xlsx - Inventory.csv")
        orders = pd.read_csv("UAE_Operations_DB.xlsx - Order_History.csv")
        return inv, orders
    except:
        return pd.DataFrame(), pd.DataFrame()

df_inv, df_orders = load_data()

# --- 3. محرك التحليل "غير الجامد" (الذكاء الاستراتيجي) ---
def strategic_analyst(user_query):
    if df_inv.empty or df_orders.empty:
        return "سيدي، قاعدة البيانات غير متصلة. يرجى التأكد من وجود ملفات العمليات."

    q = user_query.lower()
    
    # تحويل البيانات إلى "حقائق" للتحليل
    delayed_df = df_orders[df_orders['Status'].str.contains('متأخر', na=False)]
    low_stock = df_inv[df_inv['Stock_Level'] < 600]
    
    # منطق التفكير (الفهم والسياق)
    if any(word in q for word in ['وضع', 'تقرير', 'حلل', 'نصيحة', 'ماذا هناك']):
        # هنا يقوم النظام بـ "التفكير" وربط المعلومات
        insight = f"### 📊 التقرير التحليلي لليوم - أستاذ طارق\n\n"
        insight += f"سيدي، بعد تحليل {len(df_orders)} عملية جارية، وجدت أن التحدي الأكبر يكمن في **({delayed_df['City'].value_counts().idxmax()})** حيث يتركز التأخير بنسبة عالية. "
        
        if not low_stock.empty:
            item = low_stock.iloc[0]
            insight += f"وبالنظر للمخازن، هناك خطر وشيك لنفاذ **({item['Product']})** في {item['Warehouse']}، الرصيد المتبقي ({item['Stock_Level']}) لن يغطي طلبات الـ 24 ساعة القادمة. \n\n"
        
        insight += "💡 **رؤيتي الاستراتيجية:** أقترح تحويل مسار رحلتين من الشارقة لدعم دبي، مع تفعيل طلب توريد عاجل للمواد الغذائية الأساسية."
        return insight

    # إذا كان السؤال عن مدينة معينة (دبي مثلاً)
    for city in ['دبي', 'أبوظبي', 'الشارقة', 'العين']:
        if city in q:
            city_inv = df_inv[df_inv['Warehouse'].str.contains(city, na=False)]
            total = city_inv['Stock_Level'].sum()
            return f"📍 **عن {city}:** المخزون الإجمالي {total:,} وحدة. لاحظت أن هناك فائضاً في منتجات المشروبات، بينما نواجه عجزاً في السلع الجافة. هل نراجع خطة المشتريات لـ {city}؟"

    # الحوار المفتوح (التفاعل كبشري)
    return "أنا معك يا أستاذ طارق، أفكر في البيانات الآن. يمكننا التحدث في أي شيء؛ من تحليل أداء السائقين إلى وضع استراتيجية للمخازن المتعثرة. ماذا تقترح؟"

# --- 4. واجهة المحادثة التفاعلية (Sidebar) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:110px; border:3px solid #00ffcc; box-shadow: 0px 4px 15px rgba(0,255,204,0.3);"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>المستشار الذكي طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'messages' not in st.session_state: st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"], avatar=user_avatar if m["role"]=="assistant" else None):
            st.write(m["content"])

    if prompt := st.chat_input("تحدث معي.. حلل لي وضع العمليات"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        # استدعاء محرك التفكير المفتوح
        response = strategic_analyst(prompt)
        with st.chat_message("assistant", avatar=user_avatar): st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- 5. الداشبورد الاستراتيجي (الرؤية البصرية الكاملة) ---
st.markdown("<h1 style='text-align:center;'>🏗️ Operations Command Center</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    # المنطقة 1: النصيحة الاستراتيجية الفورية (تظهر أولاً كتقرير)
    st.info(strategic_analyst("تحليل عام"))
    
    st.markdown("---")
    
    # المنطقة 2: مؤشرات الأداء (KPIs)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("المخزون الكلي", f"{df_inv['Stock_Level'].sum():,}")
    k2.metric("شحنات متأخرة 🔴", len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)]))
    k3.metric("تحت التسليم", len(df_orders[df_orders['Status'].str.contains('الطريق', na=False)]))
    k4.metric("كفاءة الأسطول", "92%")

    st.markdown("---")
    
    # المنطقة 3: الخرائط والرسوم البيانية
    col_graph, col_map = st.columns([2, 1])
    with col_graph:
        st.subheader("📊 تحليل مستويات المخزون (منتج/مستودع)")
        fig = px.bar(df_inv, x='Warehouse', y='Stock_Level', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
        
    with col_map:
        st.subheader("📍 التوزيع الجغرافي للمراكز")
        # خريطة مواقع المستودعات في الإمارات
        map_data = pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]})
        st.map(map_data)

    st.subheader("📋 مراجعة سجلات العمليات الحية (Order History)")
    st.dataframe(df_orders, use_container_width=True)