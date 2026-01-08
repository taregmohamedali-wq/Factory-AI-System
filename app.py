import streamlit as st
import pandas as pd
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

# 3. تهيئة البيانات (تأكد من ثبات البيانات لضمان منطقية الإجابة)
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
    for i in range(1, 51):
        orders.append({
            'Order_ID': f'ORD-{1000+i}',
            'Status': np.random.choice(['Delivered ✅', 'Delayed 🔴', 'In Transit 🚚']),
            'Driver': np.random.choice(drivers),
            'City': np.random.choice(cities),
            'Priority': np.random.choice(['VIP (AAA)', 'High (AA)', 'Normal (A)'])
        })
    st.session_state.df_inv = pd.DataFrame(inv)
    st.session_state.df_orders = pd.DataFrame(orders)
    st.session_state.chat_history = [] 
    st.session_state.db_init = True

df_ord = st.session_state.df_orders
df_inv = st.session_state.df_inv
user_avatar = get_image_base64("me.jpg")

# --- 4. محرك الإجابة المنطقية الشامل (Logic Engine) ---
def advanced_analyser(query):
    q = query.lower()
    df_i = st.session_state.df_inv
    df_o = st.session_state.df_orders
    
    # قائمة الكلمات المفتاحية الذكية
    keywords = {
        'inventory': ['مخزون', 'بضاعة', 'كمية', 'stock', 'inventory'],
        'low_stock': ['نقص', 'قليل', 'خلص', 'low', 'shortage'],
        'drivers': ['سائق', 'سواق', 'أفضل', 'driver', 'performance'],
        'delays': ['تأخير', 'متأخر', 'مشكلة', 'delay', 'late'],
        'locations': ['دبي', 'أبوظبي', 'الشارقة', 'العين', 'dubai', 'abu dhabi', 'sharjah']
    }

    # 1. تحليل المخزون (Inventory Analysis)
    if any(word in q for word in keywords['inventory'] + keywords['low_stock']):
        total = df_i['Stock'].sum()
        low = df_i[df_i['Stock'] < 500]
        if "دبي" in q or "dubai" in q:
            val = df_i[df_i['Warehouse'].str.contains('Dubai')]['Stock'].sum()
            return f"سيدي، مخزون مستودع دبي حالياً هو **{val:,}** وحدة. " + (f"وهناك نقص في {len(df_i[(df_i['Warehouse'].str.contains('Dubai')) & (df_i['Stock'] < 500)])} أصناف." if val > 0 else "")
        
        res = f"إجمالي المخزون العام هو **{total:,}** وحدة. "
        if not low.empty:
            res += f"\n\n⚠️ **تنبيه:** يوجد عجز في الأصناف التالية: {', '.join(low['Product'].unique())}."
        return res

    # 2. تحليل السائقين والأداء (Driver Analysis)
    if any(word in q for word in keywords['drivers']):
        best_driver = df_o[df_o['Status'] == 'Delivered ✅']['Driver'].value_counts()
        if not best_driver.empty:
            name = best_driver.index[0]
            count = best_driver.values[0]
            return f"بناءً على البيانات، السائق **{name}** هو الأكثر كفاءة حالياً بإتمام **{count}** عمليات تسليم ناجحة."
        return "لا توجد بيانات تسليم مكتملة لتقييم السائقين حالياً."

    # 3. تحليل التأخير (Delay Analysis)
    if any(word in q for word in keywords['delays']):
        delayed = df_o[df_o['Status'] == 'Delayed 🔴']
        if not delayed.empty:
            city_focus = delayed['City'].value_counts().index[0]
            return f"لدينا **{len(delayed)}** شحنات متأخرة. المشكلة تتركز بشكل أساسي في مدينة **{city_focus}**. أنصح بالتحقق من حالة الطقس أو مسارات الطريق هناك."
        return "أبشرك، لا توجد أي شحنات متأخرة في النظام حتى هذه اللحظة."

    # 4. تحليل المدن والمواقع (Location Analysis)
    if any(word in q for word in keywords['locations']):
        for city in ['Dubai', 'Abu Dhabi', 'Sharjah', 'دبي', 'أبوظبي', 'الشارقة']:
            if city.lower() in q:
                c_en = "Dubai" if city in ["دبي", "Dubai"] else ("Abu Dhabi" if city in ["أبوظبي", "Abu Dhabi"] else "Sharjah")
                count_ord = len(df_o[df_o['City'].str.contains(c_en, case=False)])
                return f"تحليل مدينة {city}: يوجد **{count_ord}** طلبات نشطة حالياً. حالة العمليات هناك مستقرة بشكل عام."

    return "مرحباً أستاذ طارق. أنا جاهز لتحليل المخزون، تقييم السائقين، أو متابعة التأخيرات. كيف يمكنني مساعدتك الآن؟"

# --- 5. واجهة المستخدم (Sidebar & Chat) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="width:100px;border-radius:50%;border:3px solid #FF4B4B;"></div>', unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center'>المستشار طارق</h2>", unsafe_allow_html=True)
    
    # حاوية الشات
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar=user_avatar if msg["role"] == "assistant" else None):
            st.markdown(msg["content"])

    if prompt := st.chat_input("اسألني عن المخزون أو السائقين..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        response = advanced_analyser(prompt)
        
        with st.chat_message("assistant", avatar=user_avatar):
            st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- 6. الواجهة الرئيسية (Dashboard) ---
st.title("🏭 Strategic Operations Center")
m1, m2, m3 = st.columns(3)
m1.metric("إجمالي المخزون", f"{df_inv['Stock'].sum():,}")
m2.metric("شحنات متأخرة", len(df_ord[df_ord['Status'] == 'Delayed 🔴']))
m3.metric("كفاءة التسليم", f"{(len(df_ord[df_ord['Status'] == 'Delivered ✅'])/len(df_ord))*100:.1f}%")

st.markdown("---")
st.subheader("📋 تفاصيل المخزون الحالية")
st.dataframe(df_inv, use_container_width=True)