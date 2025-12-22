import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
import base64

# --- 1. وظيفة تقنية لتحويل الصورة لضمان ظهورها كـ Avatar ---
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    except:
        return None

# --- 2. إعدادات الصفحة ---
st.set_page_config(page_title="Strategic AI Manager", layout="wide", page_icon="👨‍💼")

# --- 3. تهيئة البيانات المركزية (Global State) ---
if 'db_init' not in st.session_state:
    prods = ['Cola 330ml', 'Cola 1.5L', 'Water 500ml', 'Flour 5kg', 'Pasta']
    whs = ['مستودع دبي المركزي', 'مستودع أبوظبي الرئيسي', 'مستودع الشارقة']
    inv = []
    for p in prods:
        for w in whs:
            inv.append({'المستودع': w, 'المنتج': p, 'الرصيد': np.random.randint(50, 4000)})
    
    drivers = ['سعيد محمد', 'أحمد علي', 'جاسم عبدالله', 'خالد إبراهيم', 'محمد حسن']
    cities = ['دبي', 'أبوظبي', 'الشارقة', 'العين', 'الفجيرة']
    orders = []
    for i in range(1, 41):
        orders.append({
            'العميل': f'عميل {i}',
            'الحالة': np.random.choice(['تم التسليم ✅', 'متأخر 🔴', 'في الطريق 🚚']),
            'السائق': np.random.choice(drivers),
            'المدينة': np.random.choice(cities),
            'الأهمية': np.random.choice(['VIP (AAA)', 'High (AA)', 'Normal (A)']),
            'الشاحنة': f'TRK-{100+i}'
        })
    st.session_state.df_inv = pd.DataFrame(inv)
    st.session_state.df_orders = pd.DataFrame(orders)
    st.session_state.chat_history = [] 
    st.session_state.db_init = True

# تعريف المتغيرات للتحليل العام (تجنب NameError)
df_ord = st.session_state.df_orders
df_inv = st.session_state.df_inv
delayed = df_ord[df_ord['الحالة'] == 'متأخر 🔴']
low_stock = df_inv[df_inv['الرصيد'] < 500]
efficiency = 100 - (len(delayed)/len(df_ord)*100) if len(df_ord) > 0 else 100

# تحضير صورة "المستشار طارق"
avatar_data = get_image_base64("me.jpg")

# --- 4. القائمة الجانبية (Sidebar) مع AI تفاعلي وصورة شخصية ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    
    if avatar_data:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center;">
                <img src="{avatar_data}" 
                     style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 3px solid #1E3A8A;">
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.warning("يرجى التأكد من وجود ملف me.jpg بجانب app.py")

    st.markdown("<h3 style='text-align: center; margin-bottom: 0;'>المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #1E3A8A; font-weight: bold;'>مدير العمليات الذكي</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # عرض سجل المحادثة بأسلوب الذكاء الاصطناعي الكامل
    for msg in st.session_state.chat_history:
        # استخدام صورتك me.jpg كأيقونة لردود المساعد
        msg_avatar = avatar_data if msg["role"] == "assistant" else None
        with st.chat_message(msg["role"], avatar=msg_avatar):
            st.markdown(msg["content"])

    if prompt := st.chat_input("تحدث معي.. كيف ترى وضع المصنع اليوم؟"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=avatar_data):
            q = prompt.lower()
            # منطق الرد الاستشاري المفتوح (AI)
            if any(word in q for word in ["أين", "تاخير", "تاخر", "وين", "مشكلة"]):
                cities_affected = delayed['المدينة'].unique()
                response = f"أستاذ طارق، بناءً على التحليل اللحظي، رصدت تأخيرات في: **{', '.join(cities_affected)}**. \n\n"
                response += f"لدينا حالياً {len(delayed)} شحنة متأثرة. أقترح إعادة توزيع الأحمال فوراً لضمان رضا العملاء."
            
            elif any(word in q for word in ["نصيحة", "رايك", "حل", "اقتراح", "خطة"]):
                response = "بصفتي شريكك الاستراتيجي، أنصحك بالآتي: \n 1. **توازن المخزون:** هناك نقص في بعض الأصناف، يجب المبادرة بطلب توريد. \n 2. **تحسين المسارات:** دمج الرحلات المتقاربة جغرافياً لتقليل تكلفة الوقود."
            
            elif any(word in q for word in ["اهلا", "كيف حالك", "مرحبا"]):
                response = f"أهلاً بك يا أستاذ طارق. كفاءة النظام اليوم {efficiency:.1f}%. أنا مستعد لنقاش أي حلول استباقية معك."
            
            else:
                response = "فهمت قصدك تماماً. هل نركز الآن على تحليل أداء السائقين أم ننتقل لمراجعة تقرير المستودعات؟"

            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- 5. الواجهة الرئيسية (Dashboard) ---
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏛️ مركز الإدارة والتحليل الاستراتيجي</h1>", unsafe_allow_html=True)

# صف المؤشرات الرئيسية (KPIs)
k1, k2, k3, k4 = st.columns(4)
k1.metric("كفاءة النظام", f"{efficiency:.1f}%")
k2.metric("شاحنات نشطة", len(df_ord[df_ord['الحالة'] != 'تم التسليم ✅']))
k3.metric("تأخيرات 🔴", len(delayed), delta_color="inverse")
k4.metric("إجمالي المخزون", f"{df_inv['الرصيد'].sum():,}")

st.markdown("---")
tab1, tab2, tab3 = st.tabs(["🚛 الرقابة الجغرافية", "📦 حالة المستودعات", "📊 الرؤية البيانية"])

with tab1:
    st.subheader("تفاصيل حركة الأسطول")
    st.dataframe(df_ord.sort_values(by='الأهمية'), use_container_width=True)

with tab2:
    st.subheader("مستويات المخزون الحالية")
    st.dataframe(df_inv, use_container_width=True)

with tab3:
    c_l, c_r = st.columns(2)
    with c_l:
        st.plotly_chart(px.pie(df_ord, names='الحالة', hole=0.4, title="تحليل كفاءة التسليم"), use_container_width=True)
    with c_r:
        st.plotly_chart(px.bar(df_inv, x='المنتج', y='الرصيد', color='المستودع', barmode='group', title="توزيع المخزون الاستراتيجي"), use_container_width=True)