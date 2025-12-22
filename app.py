import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. إعدادات الصفحة
st.set_page_config(page_title="مدير العمليات طارق ", layout="wide")

# 2. بناء قاعدة البيانات (الأسطول والمخازن)
if 'db' not in st.session_state:
    # بيانات المخازن
    prods = ['Cola 330ml', 'Cola 1.5L', 'Water 500ml', 'Flour 5kg', 'Pasta']
    whs = ['مستودع دبي المركزي', 'مستودع أبوظبي الرئيسي', 'مستودع الشارقة']
    inv = []
    for p in prods:
        for w in whs:
            inv.append({'المستودع': w, 'المنتج': p, 'الرصيد': np.random.randint(50, 4000)})
    
    # بيانات الأسطول
    drivers = ['سعيد محمد', 'أحمد علي', 'جاسم عبدالله', 'خالد إبراهيم', 'محمد حسن']
    cities = ['دبي', 'أبوظبي', 'الشارقة', 'العين', 'الفجيرة']
    orders = []
    for i in range(1, 31):
        orders.append({
            'العميل': f'عميل {i}',
            'الحالة': np.random.choice(['تم التسليم ✅', 'متأخر 🔴', 'في الطريق 🚚']),
            'السائق': np.random.choice(drivers),
            'المدينة': np.random.choice(cities),
            'الشاحنة': f'TRK-{100+i}'
        })
    
    st.session_state.df_inv = pd.DataFrame(inv)
    st.session_state.df_orders = pd.DataFrame(orders)
    st.session_state.messages = [] 
    st.session_state.db = True

# --- القائمة الجانبية: محرك الدردشة الذكي ---
with st.sidebar:
    st.header("👨‍💼 مدير العمليات طارق")
    st.write("اسألني عن المدن، السائقين، أو المخازن وسأجيبك بدقة.")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("مثلاً: ما هي المدن التي فيها تأخير؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            q = prompt.lower()
            df_ord = st.session_state.df_orders
            df_inv = st.session_state.df_inv
            
            # --- منطق الاستجابة التحليلي الدقيق ---

            # 1. السؤال عن المدن المتأخرة (إصلاح المشكلة المطلوبة)
            if any(word in q for word in ["مدن", "مدينه", "المدن", "المدينة"]):
                delayed_orders = df_ord[df_ord['الحالة'] == 'متأخر 🔴']
                if not delayed_orders.empty:
                    cities_list = delayed_orders['المدينة'].unique()
                    response = f"سيدي، قمت بمراجعة حركة الأسطول الآن. المدن التي تشهد تأخيراً حالياً هي: **{', '.join(cities_list)}**.\n\n"
                    response += "📝 **التفاصيل:**\n"
                    for city in cities_list:
                        count = len(delayed_orders[delayed_orders['المدينة'] == city])
                        response += f"- في **{city}**: يوجد {count} شحنات متأخرة.\n"
                else:
                    response = "أبشرك، لا يوجد أي تأخير في أي مدينة حالياً، جميع الرحلات تسير حسب الجدول."

            # 2. السؤال عن السائقين
            elif any(word in q for word in ["سائق", "سواق", "السائقين"]):
                delayed_drivers = df_ord[df_ord['الحالة'] == 'متأخر 🔴']
                if not delayed_drivers.empty:
                    response = "بخصوص السائقين، رصدت تأخيراً عند السادة:\n"
                    for _, row in delayed_drivers.head(3).iterrows():
                        response += f"- **{row['السائق']}** (شاحنة {row['الشاحنة']}) في {row['المدينة']}.\n"
                else:
                    response = "جميع السائقين في وضع سليم وتسليماتهم منضبطة."

            # 3. السؤال عن المخزون
            elif any(word in q for word in ["مخزن", "بضاعة", "نقص", "نواقص"]):
                critical = df_inv[df_inv['الرصيد'] < 300]
                if not critical.empty:
                    response = "هناك نقص في الأصناف التالية:\n"
                    for _, row in critical.head(3).iterrows():
                        response += f"- **{row['المنتج']}** في **{row['المستودع']}** (الرصيد: {row['الرصيد']}).\n"
                else:
                    response = "المخزون متوفر في جميع المستودعات ولا توجد نواقص حالياً."

            # 4. التحية
            elif any(word in q for word in ["أهلا", "مرحبا", "هلا", "كيف حالك"]):
                response = "أهلاً بك أستاذ طارق! أنا بخير ومستعد لتحليل كافة العمليات معك. بماذا أخدمك؟"

            else:
                response = "أعتذر منك، لم أفهم السؤال بدقة. هل تسأل عن 'المدن المتأخرة'، 'حالة السائقين'، أم 'نقص المخازن'؟"

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- الواجهة الرئيسية ---
st.markdown("<h1 style='text-align: center;'>🏛️ مركز الإدارة والتحليل </h1>", unsafe_allow_html=True)

# المؤشرات (KPIs)
c1, c2, c3, c4 = st.columns(4)
c1.metric("إجمالي الشحنات", len(st.session_state.df_orders))
c2.metric("في الطريق 🚚", len(st.session_state.df_orders[st.session_state.df_orders['الحالة'] == 'في الطريق 🚚']))
c3.metric("تأخيرات 🔴", len(st.session_state.df_orders[st.session_state.df_orders['الحالة'] == 'متأخر 🔴']))
c4.metric("المخزون", f"{st.session_state.df_inv['الرصيد'].sum():,}")

st.markdown("---")
tab1, tab2, tab3 = st.tabs(["📋 تفاصيل الأسطول", "📦 حالة المخازن", "📊 تقارير بيانية"])

with tab1:
    st.dataframe(st.session_state.df_orders, use_container_width=True)
with tab2:
    st.dataframe(st.session_state.df_inv, use_container_width=True)
with tab3:
    st.plotly_chart(px.bar(st.session_state.df_inv, x='المنتج', y='الرصيد', color='المستودع', barmode='group'), use_container_width=True)