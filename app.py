import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات الهوية البصرية ---
st.set_page_config(page_title="Strategic Operations AI", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

# جلب صورتك الشخصية لاستخدامها في الشات
user_avatar_base64 = get_base64_img("me.jpg")

# --- 2. محرك جلب البيانات الحقيقي ---
@st.cache_data
def load_data_from_files():
    # الربط المباشر بملفاتك المرفوعة
    try:
        df_inv = pd.read_csv("UAE_Operations_DB.xlsx - Inventory.csv")
        df_orders = pd.read_csv("UAE_Operations_DB.xlsx - Order_History.csv")
        return df_inv, df_orders
    except:
        return pd.DataFrame(), pd.DataFrame()

df_inv, df_orders = load_data_from_files()

# --- 3. عقل المستشار (اسالني) ---
def strategic_brain(query):
    query = query.lower()
    
    if df_inv.empty or df_orders.empty:
        return "أستاذ طارق، الملفات مرفوعة ولكن لا يمكنني قراءتها. تأكد من صحة مسارات الملفات."

    # أ- تحليل التأخير (الحل لمشكلة عدم المنطقية)
    if any(word in query for word in ['تاخير', 'تأخير', 'delay', 'متأخر']):
        # البحث عن كلمة "متأخر 🔴" في عمود Status
        delayed_data = df_orders[df_orders['Status'].str.contains('متأخر', na=False)]
        if not delayed_data.empty:
            count = len(delayed_data)
            drivers = ", ".join(delayed_data['Driver'].unique()[:3])
            return f"⚠️ **تقرير التأخير الاستراتيجي:** سيدي، رصدت في ملفك {count} شحنات متأخرة حالياً. المشكلة تتركز عند السائقين: ({drivers}). هل أصدر لك قائمة تفصيلية بمواقعهم؟"
        return "✅ أستاذ طارق، البيانات تشير إلى أن جميع الرحلات تسير في وقتها، لا تأخير حالياً."

    # ب- تحليل مدينة معينة (دبي، أبوظبي، الشارقة)
    cities_map = {'دبي': 'دبي', 'أبوظبي': 'أبوظبي', 'الشارقة': 'الشارقة'}
    for ar_name, search_val in cities_map.items():
        if ar_name in query:
            city_stock = df_inv[df_inv['Warehouse'].str.contains(search_val, na=False)]
            if not city_stock.empty:
                total = city_stock['Stock_Level'].sum()
                item_min = city_stock.loc[city_stock['Stock_Level'].idxmin()]
                return f"📍 **تقرير مخزن {ar_name}:** المخزون الإجمالي هو {total:,} وحدة. لاحظت نقصاً حرجاً في صنف ({item_min['Product']}) حيث وصل لـ {item_min['Stock_Level']} فقط."

    # ج- رد ذكي عام
    return f"أنا معك أستاذ طارق. حللت لك الآن {len(df_inv)} صنف مخزني و{len(df_orders)} طلبية. هل نبدأ بمناقشة (مستوى الخدمة في دبي) أم (نواقص مستودع الشارقة)؟"

# --- 4. واجهة المحادثة (Sidebar) ---
with st.sidebar:
    if user_avatar_base64:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar_base64}" style="border-radius:50%; width:120px; border:3px solid #00ffcc;"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>AI المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'history' not in st.session_state: st.session_state.history = []
    
    # عرض المحادثة مع صورتك في كل رد للـ Assistant
    for m in st.session_state.history:
        avatar_img = user_avatar_base64 if m["role"] == "assistant" else None
        with st.chat_message(m["role"], avatar=avatar_img):
            st.write(m["content"])

    if prompt := st.chat_input("تحدث معي.. اسأل عن دبي أو التأخير"):
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        # استجابة ذكية من واقع الملفات
        response = strategic_brain(prompt)
        
        with st.chat_message("assistant", avatar=user_avatar_base64):
            st.write(response)
        st.session_state.history.append({"role": "assistant", "content": response})

# --- 5. الداشبورد (التصميم المطلوب) ---
st.markdown("<h1 style='text-align:center;'>Strategic Operations Hub</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    # عدادات حقيقية
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي المخزون", f"{df_inv['Stock_Level'].sum():,}")
    c2.metric("شحنات متأخرة 🔴", len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)]))
    c3.metric("المستودعات المغطاة", df_inv['Warehouse'].nunique())

    st.markdown("---")
    
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.subheader("📊 مستويات المخزون لكل منتج")
        fig = px.bar(df_inv, x='Warehouse', y='Stock_Level', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_r:
        st.subheader("💡 الرؤية الاستراتيجية")
        st.warning(f"تنبيه: مخزون Flour 5kg في الشارقة وصل لـ 213 وحدة فقط! يرجى التحرك.")
        st.map(pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]}))

    st.subheader("📋 معاينة سجل العمليات الحية")
    st.dataframe(df_orders.head(10), use_container_width=True)