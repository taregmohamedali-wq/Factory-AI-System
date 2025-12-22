import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. إعدادات الصفحة
st.set_page_config(page_title="AI Operations Hub", layout="wide")

# 2. تهيئة البيانات والذاكرة
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

# تعريف المتغيرات للاستخدام العام
df_ord = st.session_state.df_orders
df_inv = st.session_state.df_inv

# --- القائمة الجانبية: المستشار الذكي (Open AI Style) ---
with st.sidebar:
    st.header("👨‍💼 المستشار الاستراتيجي AI")
    st.markdown("---")
    
    # عرض سجل المحادثة
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("تحدث معي بحرية عن حالة المصنع..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            q = prompt.lower()
            delayed = df_ord[df_ord['الحالة'] == 'متأخر 🔴']
            low_stock = df_inv[df_inv['الرصيد'] < 500]

            # --- محرك التحليل والدردشة المفتوحة ---
            if any(word in q for word in ["أين", "تاخير", "تاخر", "وين", "مشكلة"]):
                if not delayed.empty:
                    c_list = delayed['المدينة'].unique()
                    response = f"أستاذ طارق، لقد فحصت مسارات الأسطول فوراً. **التأخير يتركز في: {', '.join(c_list)}**. \n\n"
                    response += f"لدينا {len(delayed)} شحنات متعثرة حالياً. \n\n"
                    response += "💡 **تحليل وحلول:** يبدو أن هناك ضغطاً لوجستياً في تلك المناطق. أنصح بإعادة جدولة الرحلات غير العاجلة لتفريغ الشاحنات لطلبيات الـ VIP، أو التواصل مع السائقين للتأكد من عدم وجود أعطال فنية."
                else:
                    response = "فحصت النظام بالكامل؛ لا يوجد أي تأخير حالياً والعمليات تسير بكفاءة 100%."

            elif any(word in q for word in ["نصيحة", "رايك", "حل", "اقتراح", "تطوير"]):
                response = "بصفتي مستشارك الاستراتيجي، إليك رؤيتي بناءً على أرقام اليوم: \n\n"
                response += f"1. **إدارة المخزون:** هناك {len(low_stock)} أصناف قاربت على النفاد. تأخير الطلب سيكلفنا حصة سوقية. \n"
                response += "2. **كفاءة النقل:** أقترح دمج الشحنات لتقليل استهلاك الوقود (Load Optimization). \n"
                response += "3. **التحول الرقمي:** هل فكرت في تفعيل نظام التنبؤ بالطلب (Demand Forecasting) لتجنب هذه النواقص مستقبلاً؟"

            elif any(word in q for word in ["اهلا", "كيف حالك", "مرحبا", "يا"]):
                eff = 100 - (len(delayed)/len(df_ord)*100)
                response = f"أهلاً بك يا أستاذ طارق! أنا في حالة تأهب قصوى. كفاءة العمليات اليوم هي {eff:.1f}%. لدي ملاحظات حول بعض النواقص في المخازن، هل نناقشها؟"

            else:
                response = "أنا معك تماماً. يمكننا نقاش أي شيء من تحسين أداء السائقين إلى استراتيجيات التوسع في المخازن. أخبرني بماذا تفكر؟"

            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- الواجهة الرئيسية (Dashboard) ---
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏛️ مركز الإدارة والتحليل الاستراتيجي</h1>", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
k1.metric("كفاءة النظام", f"{100 - (len(delayed)/len(df_ord)*100):.1f}%")
k2.metric("شاحنات نشطة", len(df_ord[df_ord['الحالة'] != 'تم التسليم ✅']))
k3.metric("تأخيرات 🔴", len(delayed), delta_color="inverse")
k4.metric("إجمالي الرصيد", f"{df_inv['الرصيد'].sum():,}")

st.markdown("---")
t1, t2, t3 = st.tabs(["🚛 الرقابة الجغرافية", "📦 حالة المستودعات", "📊 التحليلات"])

with t1:
    st.dataframe(df_ord.sort_values(by='الأهمية'), use_container_width=True)
with t2:
    st.dataframe(df_inv, use_container_width=True)
with t3:
    c_l, c_r = st.columns(2)
    with c_l: st.plotly_chart(px.pie(df_ord, names='الحالة', hole=0.4, title="حالة الأسطول"), use_container_width=True)
    with c_r: st.plotly_chart(px.bar(df_inv, x='المنتج', y='الرصيد', color='المستودع', barmode='group', title="توزيع المخزون"), use_container_width=True)