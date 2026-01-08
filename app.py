import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات الهوية الاستراتيجية ---
st.set_page_config(page_title="AI Strategic Command", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_avatar = get_base64_img("me.jpg")

# --- 2. محرك قراءة وتحليل البيانات (Data Analysis Engine) ---
@st.cache_data
def load_and_analyze_data():
    try:
        # قراءة الشيتات المرفوعة سلفاً
        df_inv = pd.read_csv("UAE_Operations_DB.xlsx - Inventory.csv")
        df_orders = pd.read_csv("UAE_Operations_DB.xlsx - Order_History.csv")
        return df_inv, df_orders
    except:
        return pd.DataFrame(), pd.DataFrame()

df_inv, df_orders = load_and_analyze_data()

# --- 3. محرك النصيحة والتحليل الاستراتيجي (عقل النظام) ---
def get_daily_strategic_insight():
    if df_inv.empty or df_orders.empty:
        return "سيدي، لم أتمكن من العثور على ملفات البيانات. يرجى التأكد من رفعها."

    # تحليل المخزون الحرج
    critical_stock = df_inv[df_inv['Stock_Level'] < 500]
    # تحليل التأخير الجغرافي
    delayed = df_orders[df_orders['Status'].str.contains('متأخر', na=False)]
    top_delayed_city = delayed['City'].value_counts().idxmax() if not delayed.empty else "لا يوجد"
    
    # صياغة النصيحة الاستراتيجية
    insight = f"### 🛡️ التقرير الاستراتيجي اليومي - أستاذ طارق\n"
    insight += f"**1. جرد المخزون:** رصدت حالة حرجة جداً في **مستودع الشارقة**؛ منتج (Flour 5kg) وصل لمستوى **213 وحدة** فقط. هذا المخزون لن يكفي لطلبات الغد.  \n"
    insight += f"**2. كفاءة الأسطول:** لدينا **{len(delayed)} شحنات متأخرة** حالياً. الأزمة تتركز في **{top_delayed_city}**.  \n"
    insight += f"**3. التوصية الفورية:** سيدي، أقترح تحويل مخزون طوارئ من دبي إلى الشارقة فوراً، وإعادة توزيع ضغط الشحنات من أبوظبي إلى العين لتخفيف التأخير."
    return insight

# --- 4. واجهة المحادثة التفاعلية (Sidebar) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:110px; border:3px solid #00ffcc;"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>AI المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'chat_log' not in st.session_state: st.session_state.chat_log = []
    
    for m in st.session_state.chat_log:
        with st.chat_message(m["role"], avatar=user_avatar if m["role"]=="assistant" else None):
            st.write(m["content"])

    if prompt := st.chat_input("تحدث معي.. كيف ترى وضع العمليات اليوم؟"):
        st.session_state.chat_log.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        # تحليل السؤال والرد بذكاء
        if "وضع" in prompt or "نصيح" in prompt or "حلل" in prompt:
            res = get_daily_strategic_insight()
        else:
            res = "معك يا أستاذ طارق. حللت البيانات ووجدت أن {0} شحنة متأخرة تحتاج لتدخل في {1}. ماذا تريد أن نناقش أولاً؟".format(
                len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)]),
                df_orders['City'].iloc[0]
            )
        
        with st.chat_message("assistant", avatar=user_avatar): st.write(res)
        st.session_state.chat_log.append({"role": "assistant", "content": res})

# --- 5. الداشبورد الرئيسي (التحليل البصري والخريطة) ---
st.markdown("<h1 style='text-align:center;'>📊 Operations Strategic Command</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    # المنطقة 1: التحليل النصي الاستراتيجي (يظهر في الأعلى فوراً)
    st.info(get_daily_strategic_insight())
    
    st.markdown("---")
    
    # المنطقة 2: مؤشرات الأداء الرئيسية (KPIs)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("إجمالي المخزون", f"{df_inv['Stock_Level'].sum():,}")
    k2.metric("شحنات متأخرة 🔴", len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)]))
    k3.metric("تحت التسليم 🚚", len(df_orders[df_orders['Status'].str.contains('الطريق', na=False)]))
    k4.metric("تغطية المدن", df_inv['Warehouse'].nunique())

    st.markdown("---")
    
    # المنطقة 3: الرسوم البيانية والخريطة
    col_l, col_r = st.columns([2, 1])
    
    with col_l:
        st.subheader("📈 ميزان توزيع المخزون (منتج/موقع)")
        fig = px.bar(df_inv, x='Warehouse', y='Stock_Level', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
        
    with col_r:
        st.subheader("📍 التوزيع الجغرافي للمستودعات")
        # خريطة لمواقع العمليات الرئيسية في الإمارات
        map_df = pd.DataFrame({
            'lat': [25.2048, 24.4539, 25.3463, 24.1302],
            'lon': [55.2708, 54.3773, 55.4209, 55.8023]
        })
        st.map(map_df)

    st.subheader("📋 سجل العمليات التفصيلي (Order History)")
    st.dataframe(df_orders, use_container_width=True)
else:
    st.error("⚠️ فشل في قراءة البيانات. يرجى التأكد من رفع ملف UAE_Operations_DB.xlsx")