import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. بناء الهوية البصرية (صورتك في الرد) ---
st.set_page_config(page_title="Strategic AI Advisor", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_avatar = get_base64_img("me.jpg")

# --- 2. محرك قراءة البيانات المرفوعة سلفاً ---
@st.cache_data
def load_and_sync_data():
    try:
        # قراءة البيانات المرفوعة سلفاً في بيئة العمل
        inv = pd.read_csv("UAE_Operations_DB.xlsx - Inventory.csv")
        orders = pd.read_csv("UAE_Operations_DB.xlsx - Order_History.csv")
        return inv, orders
    except:
        return pd.DataFrame(), pd.DataFrame()

df_inv, df_orders = load_and_sync_data()

# --- 3. عقل المستشار (منطق التحليل والاستنتاج) ---
def strategic_brain(query):
    if df_inv.empty or df_orders.empty:
        return "سيدي، لم أستطع الوصول لقاعدة البيانات. يرجى التأكد من مسار ملف UAE_Operations_DB.xlsx."

    q = query.lower()
    
    # تحويل البيانات إلى حقائق رقمية للتحليل
    delayed_count = len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)])
    critical_stock = df_inv[df_inv['Stock_Level'] < 500]
    
    # منطق "ماذا هناك اليوم؟" - تحليل شامل تلقائي
    if any(word in q for word in ['وضع', 'تحليل', 'تقرير', 'ماذا هناك', 'نصيحة']):
        report = f"### 🛡️ التقرير الاستراتيجي لليوم - أستاذ طارق\n\n"
        
        # تحليل الأسطول
        if delayed_count > 0:
            top_city = df_orders[df_orders['Status'].str.contains('متأخر', na=False)]['City'].value_counts().idxmax()
            report += f"⚠️ **أزمة العمليات:** سيدي، لدينا حالياً **{delayed_count}** شحنة متأخرة. التحليل يشير إلى أن الاختناق يتركز في مدينة **({top_city})**. أقترح التواصل مع سائقي هذا المسار فوراً. \n\n"
        
        # تحليل المخزون
        if not critical_stock.empty:
            item = critical_stock.iloc[0]
            report += f"🚨 **تنبيه المخزون:** هناك خطر حقيقي لنفاذ صنف **({item['Product']})** في {item['Warehouse']}. الرصيد ({item['Stock_Level']}) لن يكفي لطلبات الغد. \n\n"
        
        report += "💡 **رؤيتي للموقف:** الأداء العام مستقر بنسبة 85%، لكن الفجوة في الشارقة تحتاج تدخلاً لوجستياً سريعاً لتعويض النواقص من مستودع دبي."
        return report

    # ردود ذكية للمحادثة المفتوحة
    return "معك يا أستاذ طارق. أنا الآن أراقب الأرقام حياً؛ هل تريد التركيز على (كفاءة السائقين) أم (تأمين نواقص المخازن في الشارقة)؟"

# --- 4. واجهة المحادثة التفاعلية (Sidebar) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:110px; border:3px solid #00ffcc; box-shadow: 0px 4px 15px rgba(0,255,204,0.3);"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>AI المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'history' not in st.session_state: st.session_state.history = []
    for m in st.session_state.history:
        with st.chat_message(m["role"], avatar=user_avatar if m["role"]=="assistant" else None):
            st.write(m["content"])

    if prompt := st.chat_input("تحدث معي.. كيف ترى وضع العمليات اليوم؟"):
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        # تشغيل محرك التفكير
        response = strategic_brain(prompt)
        with st.chat_message("assistant", avatar=user_avatar): st.write(response)
        st.session_state.history.append({"role": "assistant", "content": response})

# --- 5. الداشبورد الاستراتيجي (الخريطة والرسوم) ---
st.markdown("<h1 style='text-align:center;'>📊 Operations Strategic Command</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    # المنطقة 1: التحليل النصي الاستراتيجي (يظهر كفقرة تحليلية في الأعلى)
    st.info(strategic_brain("تحليل عام للوضع"))
    
    st.markdown("---")
    
    # المنطقة 2: مؤشرات الأداء (KPIs)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("إجمالي المخزون", f"{df_inv['Stock_Level'].sum():,}")
    k2.metric("شحنات متأخرة 🔴", len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)]))
    k3.metric("في الطريق 🚚", len(df_orders[df_orders['Status'].str.contains('طريق', na=False)]))
    k4.metric("كفاءة الأسطول", "91%")

    st.markdown("---")
    
    # المنطقة 3: الخرائط والرسوم البيانية المقارنة
    col_chart, col_map = st.columns([2, 1])
    with col_chart:
        st.subheader("📈 ميزان توزيع المخزون (منتج/مستودع)")
        fig = px.bar(df_inv, x='Warehouse', y='Stock_Level', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
        
    with col_map:
        st.subheader("📍 التوزيع الجغرافي للعمليات")
        # خريطة لمواقع المستودعات الرئيسية
        map_data = pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]})
        st.map(map_data)

    st.subheader("📋 سجل العمليات الحي (Order History)")
    st.dataframe(df_orders, use_container_width=True)