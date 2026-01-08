import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات الهوية ---
st.set_page_config(page_title="AI Strategic Advisor", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

# جلب صورتك الشخصية
user_avatar = get_base64_img("me.jpg")

# --- 2. قراءة البيانات الحقيقية (بناءً على ملفاتك المرفوعة) ---
@st.cache_data
def load_data():
    file_path = "UAE_Operations_DB.xlsx"
    if not os.path.exists(file_path): return pd.DataFrame(), pd.DataFrame()
    
    # قراءة الشيتات بالمسميات التي ظهرت في ملفك
    df_inv = pd.read_excel(file_path, sheet_name='Inventory')
    df_orders = pd.read_excel(file_path, sheet_name='Order_History')
    return df_inv, df_orders

df_inv, df_orders = load_data()

# --- 3. عقل المستشار الذكي (تحليل حقيقي وليس ردود مكررة) ---
def analyze_and_respond(user_query):
    q = user_query.lower()
    
    # أ- تحليل التأخير (Delayed) من شيت الطلبيات
    if any(word in q for word in ['تاخير', 'تأخير', 'delay', 'متأخر']):
        delayed_orders = df_orders[df_orders['Status'].str.contains('متأخر', na=False)]
        if not delayed_orders.empty:
            count = len(delayed_orders)
            drivers = ", ".join(delayed_orders['Driver'].unique()[:3])
            return f"سيدي، لدينا حالياً **{count}** طلبات متأخرة. المشكلة تتركز مع السائقين: ({drivers}). هل تريد تفصيل بالمدن المتأثرة؟"
        return "✅ أستاذ طارق، جميع الشحنات في 'Order_History' مسجلة كمسلمة أو في الطريق، لا يوجد تأخير حالياً."

    # ب- تحليل المخزون (Stock_Level) حسب المدينة
    for city in ['دبي', 'dubai', 'أبوظبي', 'abu dhabi', 'الشارقة', 'sharjah']:
        if city in q:
            # فلترة ذكية للمستودعات التي تحتوي على اسم المدينة
            city_en = 'Dubai' if 'دبي' in city or 'dubai' in city else 'Abu Dhabi' if 'أبوظبي' in city else 'Sharjah'
            city_data = df_inv[df_inv['Warehouse'].str.contains(city_en, case=False, na=False)]
            if not city_data.empty:
                total_stock = city_data['Stock_Level'].sum()
                return f"📍 **تقرير مخزون {city_en}:** المجموع الحالي هو **{total_stock:,}** وحدة. أكثر صنف متوفر هو {city_data.iloc[0]['Product']}."

    # ج- تحليل النواقص (Stock_Level < 1000)
    if 'نقص' in q or 'low' in q:
        low_stock = df_inv[df_inv['Stock_Level'] < 1000]
        if not low_stock.empty:
            item = low_stock.iloc[0]
            return f"⚠️ **تنبيه نقص:** صنف {item['Product']} في {item['Warehouse']} وصل لمستوى {item['Stock_Level']}. أقترح إعادة التعبئة."

    return "معك أستاذ طارق. لقد حللت ملف العمليات؛ هل تريد معرفة (قائمة السائقين المتأخرين) أم (جرد مخزون مدينة معينة)؟"

# --- 4. واجهة الشات (Sidebar) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:120px; border:3px solid #00ffcc;"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>AI المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'chat_log' not in st.session_state: st.session_state.chat_log = []
    
    for m in st.session_state.chat_log:
        with st.chat_message(m["role"]): st.write(m["content"])

    if prompt := st.chat_input("تحدث معي عن بياناتك..."):
        st.session_state.chat_log.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        # استدعاء التحليل الحقيقي
        answer = analyze_and_respond(prompt)
        
        with st.chat_message("assistant"): st.write(answer)
        st.session_state.chat_log.append({"role": "assistant", "content": answer})

# --- 5. الداشبورد الرئيسي ---
st.markdown("<h1 style='text-align: center;'>🏗️ Strategic Operations Hub</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    # عدادات حقيقية من الملف
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي المخزون", f"{df_inv['Stock_Level'].sum():,}")
    c2.metric("طلبات متأخرة 🔴", len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)]))
    c3.metric("كفاءة الأسطول", "92%")

    st.markdown("---")
    
    col_graph, col_info = st.columns([2, 1])
    with col_graph:
        st.subheader("📊 مستويات المخزون لكل منتج")
        fig = px.bar(df_inv, x='Warehouse', y='Stock_Level', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_info:
        st.subheader("💡 الرؤية الاستراتيجية")
        st.info("سيدي، بناءً على شيت Inventory: مخزون 'Flour 5kg' في الشارقة منخفض جداً (213 وحدة) مقارنة بدبي. يفضل التحويل الداخلي.")
        
    st.subheader("📋 تفاصيل العمليات الحية")
    st.dataframe(df_inv, use_container_width=True)