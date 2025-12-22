import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. إعدادات الصفحة
st.set_page_config(page_title="Strategic AI Manager", layout="wide")

# 2. بناء قاعدة البيانات المتكاملة
if 'db' not in st.session_state:
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
    st.session_state.db = True

# --- القائمة الجانبية: المحادثة المفتوحة ---
with st.sidebar:
    st.header("👨‍💼 طارق خبير العمليات ")
    st.info("أنا الآن أعمل بنمط 'التفكير المفتوح'. ناقشني في أي شيء يخص المصنع.")
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("تحدث معي بحرية..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            q = prompt.lower()
            df_ord = st.session_state.df_orders
            df_inv = st.session_state.df_inv
            
            # --- محرك الذكاء المفتوح (تحليل وليس مجرد رد) ---
            
            # رصد المدن (تحليل جغرافي)
            delayed_c = df_ord[df_ord['الحالة'] == 'متأخر 🔴']['المدينة'].unique()
            # رصد النواقص (تحليل مخزني)
            low_s = df_inv[df_inv['الرصيد'] < 300]['المنتج'].unique()
            # رصد السائقين (تحليل بشري)
            del_drivers = df_ord[df_ord['الحالة'] == 'متأخر 🔴']['السائق'].unique()

            # منطق الرد المفتوح:
            if any(word in q for word in ["مدن", "مكان", "فين", "وين"]):
                if len(delayed_c) > 0:
                    response = f"بناءً على مراقبتي للحركة، المدن التي تعاني من اختناق حالياً هي {', '.join(delayed_c)}. \n\n"
                    response += "💡 **رأيي الشخصي:** هذا التأخير قد يرجع لضغط الطلبات في هذه المناطق. هل نراجع خطة التوزيع هناك؟"
                else:
                    response = "جميع المدن مغطاة بالكامل ولا يوجد أي تأخير جغرافي حالياً."

            elif any(word in q for word in ["سائق", "سواق", "تأخير", "أداء"]):
                response = f"أرى أن لدينا {len(del_drivers)} سائقين يواجهون صعوبات اليوم. \n\n"
                response += f"الأبرز هم: {', '.join(del_drivers[:3])}. \n\n"
                response += "⚠️ **ملاحظة:** التأخير يتركز عند عملاء الـ VIP، وهذا قد يسبب مشكلة في العقود. أنصح بالتدخل."

            elif any(word in q for word in ["بضاعة", "نقص", "مخزن", "حل"]):
                response = f"هناك نقص في {len(low_s)} أصناف، وتحديداً {', '.join(low_s[:2])}. \n\n"
                response += "💡 **اقتراح:** بدل الشراء، دعنا ننقل الفائض من مستودع دبي إلى الشارقة، هذا سيوفر الوقت والتكلفة."

            elif any(word in q for word in ["أهلا", "مرحبا", "هلا", "كيف حالك"]):
                response = "أهلاً بك أستاذ طارق! أنا في كامل جاهزيتي. قمت للتو بمراجعة الأرقام، ولدي بعض الملاحظات على تأخيرات مدينة 'العين' ونقص 'Flour 5kg'. هل نناقشها؟"

            else:
                # الرد المفتوح "الاستشاري"
                response = "أفهم سياق حديثك. من منظور إدارة العمليات، أرى أن البيانات تشير لفرصة تحسين في توزيع الأسطول. هل تريد مني التعمق في أداء السائقين أم حالة المخازن؟"

            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- الواجهة الرئيسية (لوحة القيادة الاستراتيجية) ---
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏛️ مركز الإدارة والتحليل الاستراتيجي</h1>", unsafe_allow_html=True)

# صف الـ KPIs الجمالي
k1, k2, k3, k4 = st.columns(4)
k1.metric("كفاءة الأسطول", "92%", "3%+")
k2.metric("شاحنات نشطة", len(df_ord[df_ord['الحالة'] != 'تم التسليم ✅']))
k3.metric("تأخيرات حرجة", len(df_ord[df_ord['الحالة'] == 'متأخر 🔴']), delta_color="inverse")
k4.metric("تغطية المخزون", f"{len(df_inv[df_inv['الرصيد'] > 300])}/{len(df_inv)}")

st.markdown("---")
tab1, tab2, tab3 = st.tabs(["🚛 تحليل الأسطول", "📦 تحليل المستودعات", "📊 الرؤية البيانية"])

with tab1:
    st.dataframe(st.session_state.df_orders, use_container_width=True)
with tab2:
    st.dataframe(st.session_state.df_inv, use_container_width=True)
with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.pie(df_ord, names='الحالة', hole=0.4, title="تحليل حالة التسليم"), use_container_width=True)
    with c2:
        st.plotly_chart(px.bar(df_inv, x='المنتج', y='الرصيد', color='المستودع', title="مستويات الرصيد الجارية"), use_container_width=True)