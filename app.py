import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import base64

# --- 1. وظيفة الأفاتار ---
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    except: return None

# 2. إعدادات الصفحة
st.set_page_config(page_title="Strategic AI Manager", layout="wide", page_icon="👨‍💼")

# 3. تهيئة البيانات
if 'db_init' not in st.session_state:
    st.session_state.lang = "ar"
    prods = ['Cola 330ml', 'Cola 1.5L', 'Water 500ml', 'Flour 5kg', 'Pasta']
    whs = ['Dubai Central', 'Abu Dhabi Main', 'Sharjah Hub']
    
    inv = []
    for p in prods:
        for w in whs:
            inv.append({'Warehouse': w, 'Product': p, 'Stock': np.random.randint(50, 4000)})
    
    drivers = ['Saeed', 'Ahmed', 'Jasim', 'Khaled', 'Mohamed']
    cities = ['Dubai', 'Abu Dhabi', 'Sharjah', 'Al Ain', 'Fujairah']
    orders = []
    for i in range(1, 41):
        orders.append({
            'Customer': f'Client {i}',
            'Status': np.random.choice(['Delivered ✅', 'Delayed 🔴', 'In Transit 🚚']),
            'Driver': np.random.choice(drivers),
            'City': np.random.choice(cities),
            'Priority': np.random.choice(['VIP (AAA)', 'High (AA)', 'Normal (A)']),
            'Truck': f'TRK-{100+i}'
        })
    st.session_state.df_inv = pd.DataFrame(inv)
    st.session_state.df_orders = pd.DataFrame(orders)
    st.session_state.chat_history = [] 
    st.session_state.db_init = True

df_ord = st.session_state.df_orders
df_inv = st.session_state.df_inv
user_avatar = get_image_base64("me.jpg")

# --- 4. منطق "المستشار طارق" المطور (بدون API) ---
def logic_tariq_analyser(query):
    query = query.lower()
    res = ""
    
    # أ- تحليل حالة المخزون العام أو لمنتج معين
    if any(word in query for word in ["مخزون", "نقص", "stock", "low"]):
        low_stock = df_inv[df_inv['Stock'] < 500]
        total_units = df_inv['Stock'].sum()
        res = f"سيدي، إجمالي المخزون في جميع المستودعات هو **{total_units:,} وحدة**. \n\n"
        if not low_stock.empty:
            res += f"⚠️ **تنبيه حرج:** هناك {len(low_stock)} أصناف قاربت على النفاد (أقل من 500 وحدة)، خاصة منتج **{low_stock.iloc[0]['Product']}** في مستودع **{low_stock.iloc[0]['Warehouse']}**."
        else:
            res += "✅ حالة المخزون مستقرة حالياً ولا يوجد نقص حاد."

    # ب- تحليل السائقين والأداء
    elif any(word in query for word in ["سائق", "driver", "أفضل", "best"]):
        top_driver = df_ord[df_ord['Status'] == 'Delivered ✅']['Driver'].value_counts().idxmax()
        count = df_ord[df_ord['Status'] == 'Delivered ✅']['Driver'].value_counts().max()
        res = f"بناءً على سجلات التسليم، السائق الأفضل حالياً هو **{top_driver}** بإتمام **{count} شحنات** ناجحة. أنصح بصرف مكافأة أداء له."

    # ج- تحليل التأخير والمدن
    elif any(word in query for word in ["تأخير", "مشكلة", "delay", "problem"]):
        delayed_city = df_ord[df_ord['Status'] == 'Delayed 🔴']['City'].value_counts()
        if not delayed_city.empty:
            res = f"لدينا مشكلة تأخير متركزة في مدينة **{delayed_city.index[0]}** ({delayed_city.values[0]} شحنات). أقترح مراجعة مسارات الشاحنات المتجهة هناك فوراً."
        else:
            res = "لا توجد أي شحنات متأخرة حالياً، الأسطول يعمل بكفاءة 100%."

    # د- تحليل مستودع معين (دبي، أبوظبي، الشارقة)
    elif any(word in query for word in ["دبي", "أبوظبي", "الشارقة", "dubai", "abu dhabi", "sharjah"]):
        city_name = "Dubai" if "دبي" in query or "dubai" in query else ("Abu Dhabi" if "أبوظبي" in query else "Sharjah")
        sub_df = df_inv[df_inv['Warehouse'].str.contains(city_name, case=False)]
        city_stock = sub_df['Stock'].sum()
        res = f"تحليل مستودع {city_name}: المخزون المتوفر **{city_stock:,} وحدة**. \n\n"
        res += f"أكبر كمية متوفرة هي لمنتج **{sub_df.sort_values(by='Stock', ascending=False).iloc[0]['Product']}**."

    # هـ- في حال لم يفهم السؤال
    else:
        res = "مرحباً بك. يمكنني تحليل (المخزون، أداء السائقين، الشحنات المتأخرة، أو حالة المستودعات بالمدن). بماذا تريدني أن أزودك؟"
    
    return res

# --- 5. الواجهة الجانبية (الشات) ---
with st.sidebar:
    st.session_state.lang = st.selectbox("🌐 Language", ["ar", "en"], index=0 if st.session_state.lang == "ar" else 1)
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="width:100px;border-radius:50%;border:3px solid #1E3A8A;"></div>', unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center'>{'المستشار طارق' if st.session_state.lang == 'ar' else 'Consultant Tariq'}</h3>", unsafe_allow_html=True)
    
    chat_container = st.container(height=400)
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"], avatar=user_avatar if msg["role"] == "assistant" else None):
                st.markdown(msg["content"])

    if prompt := st.chat_input("اسألني أي شيء عن العمليات..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        response = logic_tariq_analyser(prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

# --- 6. الواجهة الرئيسية (Dashboard) ---
st.markdown("<h1 style='text-align: center;'>🏭 Strategic Operations Center</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("إجمالي المخزون", f"{df_inv['Stock'].sum():,}")
col2.metric("شحنات قيد التنفيذ", len(df_ord[df_ord['Status'] == 'In Transit 🚚']))
col3.metric("تنبيهات التأخير", len(df_ord[df_ord['Status'] == 'Delayed 🔴']), delta_color="inverse")

st.markdown("---")
tab1, tab2 = st.tabs(["📊 تحليل المخزون", "🚚 تتبع الأسطول"])

with tab1:
    fig_inv = px.bar(df_inv, x='Product', y='Stock', color='Warehouse', barmode='group', title="توزيع المخزون حسب المستودع")
    st.plotly_chart(fig_inv, use_container_width=True)
    st.dataframe(df_inv, use_container_width=True)

with tab2:
    st.dataframe(df_ord, use_container_width=True)