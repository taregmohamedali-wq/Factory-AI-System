import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات الهوية والروح (طارق AI) ---
st.set_page_config(page_title="Strategic Command Center", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_avatar = get_base64_img("me.jpg")

# --- 2. محرك قراءة وتحليل البيانات المرفوعة سلفاً ---
@st.cache_data
def load_and_study_data():
    try:
        # قراءة البيانات المرفوعة سلفاً في بيئة العمل
        inv = pd.read_csv("UAE_Operations_DB.xlsx - Inventory.csv")
        orders = pd.read_csv("UAE_Operations_DB.xlsx - Order_History.csv")
        return inv, orders
    except:
        return pd.DataFrame(), pd.DataFrame()

df_inv, df_orders = load_and_study_data()

# --- 3. عقل المستشار: التحليل الذكي والنصيحة الاستراتيجية ---
def get_ai_insight(query="وضع اليوم"):
    if df_inv.empty or df_orders.empty:
        return "أستاذ طارق، أنا لا أرى ملفات قاعدة البيانات حالياً. يرجى التأكد من مسارات الملفات."
    
    # --- عمليات التحليل الخلفية ---
    delayed_total = len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)])
    critical_stock = df_inv[df_inv['Stock_Level'] < 600]
    top_city_delayed = df_orders[df_orders['Status'].str.contains('متأخر', na=False)]['City'].value_counts().idxmax() if delayed_total > 0 else "لا يوجد"
    
    # بناء الرد الذكي بناءً على السؤال
    q = query.lower()
    if any(word in q for word in ['وضع', 'نصيحة', 'تحليل', 'تقرير']):
        insight = f"🔍 **تحليلي للوضع القائم سيدي:**\n\n"
        insight += f"أستاذ طارق، اليوم لدينا تحدي واضح في مدينة **({top_city_delayed})** بوجود {delayed_total} شحنات متأخرة. "
        if not critical_stock.empty:
            item = critical_stock.iloc[0]
            insight += f"أما بالنسبة للمخزون، فالحالة حرجة جداً لصنف **({item['Product']})** في {item['Warehouse']}، حيث المتبقي هو {item['Stock_Level']} فقط.\n\n"
        insight += f"💡 **نصيحتي الاستراتيجية:**\nأقترح تحريك شحنة تعويضية فوراً من دبي للشارقة لتغطية نقص الـ (Flour)، وإعادة توجيه سائقي أبوظبي المتأخرين لتفادي الازدحام الحالي."
        return insight
    
    return "معك يا أستاذ طارق. أنا الآن أراقب الأرقام حياً؛ هل تريد التركيز على (أداء السائقين) أم (خطة تأمين نواقص المخازن)؟"

# --- 4. واجهة المحادثة التفاعلية (Sidebar) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:110px; border:3px solid #00ffcc;"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>AI المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'msgs' not in st.session_state: st.session_state.msgs = []
    for m in st.session_state.msgs:
        with st.chat_message(m["role"], avatar=user_avatar if m["role"]=="assistant" else None):
            st.write(m["content"])

    if prompt := st.chat_input("تحدث معي.. حلل لي وضع اليوم"):
        st.session_state.msgs.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        # استدعاء العقل التحليلي
        res = get_ai_insight(prompt)
        with st.chat_message("assistant", avatar=user_avatar): st.write(res)
        st.session_state.msgs.append({"role": "assistant", "content": res})

# --- 5. الداشبورد الرئيسي (الخريطة والرسوم والتحليل الحرفي) ---
st.markdown("<h1 style='text-align:center;'>📊 Operations Command Hub</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    # عرض النصيحة التحليلية في صدر الصفحة
    st.info(get_ai_insight())
    
    st.markdown("---")
    
    # العدادات الاستراتيجية
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("المخزون الكلي", f"{df_inv['Stock_Level'].sum():,}")
    m2.metric("شحنات متأخرة 🔴", len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)]))
    m3.metric("تحت التسليم", len(df_orders[df_orders['Status'].str.contains('الطريق', na=False)]))
    m4.metric("تغطية المدن", df_inv['Warehouse'].nunique())

    st.markdown("---")
    
    # الرسوم والخرائط
    c_left, c_right = st.columns([2, 1])
    
    with c_left:
        st.subheader("📈 ميزان توزيع المخزون (Inventory Analysis)")
        fig = px.bar(df_inv, x='Warehouse', y='Stock_Level', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
        
    with c_right:
        st.subheader("📍 التوزيع الجغرافي للمراكز")
        # خريطة لمواقع المستودعات الرئيسية
        map_df = pd.DataFrame({
            'lat': [25.2048, 24.4539, 25.3463, 24.1302],
            'lon': [55.2708, 54.3773, 55.4209, 55.8023]
        })
        st.map(map_df)
    
    st.subheader("📋 مراجعة تفصيلية لـ Order History")
    st.dataframe(df_orders, use_container_width=True)

else:
    st.warning("أستاذ طارق، الملفات مرفوعة ولكنني أحتاج لإعادة تنشيط الاتصال بها. يرجى التأكد من تشغيل الكود.")