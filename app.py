import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
import os

# --- 1. إعداد الهوية والمرئيات ---
st.set_page_config(page_title="Strategic AI Partner", layout="wide", page_icon="👨‍💼")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    return None

user_avatar = get_image_base64("me.jpg")

# --- 2. محرك البيانات الاستراتيجي (Session State) ---
if 'db_init' not in st.session_state:
    # بيانات المخزون
    st.session_state.df_inv = pd.DataFrame([
        {'Warehouse': w, 'Product': p, 'Stock': np.random.randint(50, 4000)}
        for w in ['Dubai Central', 'Abu Dhabi Main', 'Sharjah Hub']
        for p in ['Cola 330ml', 'Cola 1.5L', 'Water 500ml', 'Flour 5kg', 'Pasta']
    ])
    # بيانات العمليات
    st.session_state.df_ord = pd.DataFrame([
        {
            'Order_ID': f'ORD-{100+i}',
            'Status': np.random.choice(['Delivered ✅', 'Delayed 🔴', 'In Transit 🚚']),
            'City': np.random.choice(['Dubai', 'Abu Dhabi', 'Sharjah', 'Al Ain']),
            'Driver': np.random.choice(['Saeed', 'Ahmed', 'Jasim', 'Khaled']),
            'Priority': np.random.choice(['VIP', 'High', 'Normal'])
        } for i in range(50)
    ])
    st.session_state.chat_history = []
    st.session_state.db_init = True

# --- 3. محرك الاستشارة المرن (The Thinking Brain) ---
def tariaq_flexible_ai(prompt):
    q = prompt.lower()
    df_i = st.session_state.df_inv
    df_o = st.session_state.df_ord
    
    # تحضير ملخص البيانات للتحليل
    total_stock = df_i['Stock'].sum()
    low_stock_count = len(df_i[df_i['Stock'] < 500])
    delayed_orders = len(df_o[df_o['Status'] == 'Delayed 🔴'])
    top_driver = df_o[df_o['Status'] == 'Delivered ✅']['Driver'].value_counts().idxmax()

    # القاموس المرن للذكاء الاصطناعي
    responses = {
        "status": (["وضع", "تحليل", "كامل", "تقرير", "status", "analysis"], 
                  f"سيدي طارق، إليك التحليل الاستراتيجي الشامل:\n\n"
                  f"* **العمليات:** لدينا {delayed_orders} شحنات متأخرة تحتاج تدخل.\n"
                  f"* **المخازن:** الإجمالي {total_stock:,} وحدة، مع {low_stock_count} أصناف حرجة.\n"
                  f"* **الأداء:** السائق {top_driver} يتصدر قائمة الكفاءة.\n"
                  f"💡 **نصيحة:** أنصح بتوجيه دعم إضافي لمستودع دبي لتفادي تأخيرات الغد."),
        
        "inventory": (["مخزون", "نقص", "كمية", "بضاعة", "stock", "low"], 
                     f"بالنظر للمخزون، يوجد عجز في {low_stock_count} صنفاً. أهمها منتج {df_i.sort_values('Stock').iloc[0]['Product']}. "
                     "هل تريد مني جدولة أمر توريد افتراضي؟"),
        
        "logistics": (["طريق", "شارع", "خريطة", "أسرع", "route", "map", "traffic"], 
                     "بناءً على محاكاة حركة المرور في الإمارات:\n"
                     "* **شارع E11:** مزدحم حالياً عند دبي مارينا.\n"
                     "* **المسار البديل:** شارع الخيل (E44) يوفر 12 دقيقة للوصول لأبوظبي.\n"
                     "* **توصية:** وجه الشاحنات بالتحرك قبل الساعة 4 عصراً لتفادي وقت الذروة."),
        
        "strategy": (["نصيحة", "مستقبل", "تطوير", "advice", "future"], 
                    "استراتيجياً، أرى أننا بحاجة لتفعيل 'نظام التنبؤ المبكر'. البيانات تشير لزيادة طلب متوقعة بنسبة 15% الأسبوع القادم في العين.")
    }

    # البحث المرن (Flexible Matching)
    for key, (words, response) in responses.items():
        if any(word in q for word in words):
            return response

    # رد افتراضي ذكي إذا لم يتطابق السؤال مع القاموس
    return "أهلاً بك يا أستاذ طارق. سؤالك يقع ضمن اهتماماتي الاستشارية؛ هل تود أن أحلل لك (أداء العمليات، المسارات اللوجستية، أو وضع المخازن) بشكل أعمق؟"

# --- 4. تصميم الشات المرن (Sidebar) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="width:100px;border-radius:50%;border:2px solid #00CC96;object-fit:cover;"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center'>المستشار طارق AI</h3>", unsafe_allow_html=True)
    st.markdown("---")

    # عرض تاريخ الدردشة
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar=user_avatar if msg["role"] == "assistant" else None):
            st.markdown(msg["content"])

    if prompt := st.chat_input("اسألني عن أي شيء (مثلاً: ما هو الوضع العام؟)"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        response = tariaq_flexible_ai(prompt)
        
        with st.chat_message("assistant", avatar=user_avatar):
            st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- 5. الواجهة الرئيسية (Strategic Dashboard) ---
st.title("🌐 Strategic Operations Center")

# صف المؤشرات (KPIs)
c1, c2, c3, c4 = st.columns(4)
c1.metric("إجمالي المخزون", f"{st.session_state.df_inv['Stock'].sum():,}")
c2.metric("شحنات متأخرة", len(st.session_state.df_ord[st.session_state.df_ord['Status'] == 'Delayed 🔴']), delta="-5%", delta_color="inverse")
c3.metric("كفاءة الأسطول", "94.2%", "+2%")
c4.metric("الحالة العامة", "مستقرة ✅")

st.markdown("---")
# الرسوم البيانية
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 توزيع المخزون عبر المناطق")
    fig = px.bar(st.session_state.df_inv, x='Warehouse', y='Stock', color='Product', barmode='group', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("🚚 حالة التوصيل الحالية")
    fig2 = px.pie(st.session_state.df_ord, names='Status', hole=0.5, color_discrete_sequence=['#00CC96', '#EF553B', '#636EFA'])
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("📋 سجل البيانات التفصيلي")
st.dataframe(st.session_state.df_inv, use_container_width=True)