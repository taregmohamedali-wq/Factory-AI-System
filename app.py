import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="Strategic AI Manager", layout="wide", page_icon="👨‍💼")

# 2. تهيئة البيانات والذاكرة المركزية
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

# تعريف المتغيرات المركزية
df_ord = st.session_state.df_orders
df_inv = st.session_state.df_inv
delayed = df_ord[df_ord['الحالة'] == 'متأخر 🔴']
low_stock = df_inv[df_inv['الرصيد'] < 500]
efficiency = 100 - (len(delayed)/len(df_ord)*100) if len(df_ord) > 0 else 100

# --- القائمة الجانبية: المستشار طارق (مع صورتك الشخصية) ---
with st.sidebar:
    # محاولة تحميل صورتك me.jpg
    if os.path.exists("me.jpg"):
        col1, col2, col3 = st.columns([1,3,1])
        with col2:
            st.image("me.jpg", use_container_width=True)
    else:
        st.warning("لم يتم العثور على ملف me.jpg في المجلد")

    st.markdown("<h3 style='text-align: center;'>المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #1E3A8A; font-weight: bold;'>محرك الذكاء الاصطناعي للعمليات</p>", unsafe_allow_html=True)
    st.info("أنا الآن في نمط 'التفكير المفتوح'. سأقوم بتحليل بياناتك ومقارنتها بالحلول العالمية للوصول لأفضل أداء.")
    st.markdown("---")
    
    # عرض سجل المحادثة بأسلوب ChatGPT
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("تحدث معي.. كيف ترى وضع المصنع؟"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            q = prompt.lower()
            
            # منطق الرد التفاعلي الاستشاري (AI الكامل)
            if any(word in q for word in ["أين", "تاخير", "تاخر", "وين", "مشكلة"]):
                if not delayed.empty:
                    cities_list = delayed['المدينة'].unique()
                    response = f"سيدي، بعد مسح الشبكة اللوجستية، رصدت تأخيرات حرجة في: **{', '.join(cities_list)}**. \n\n"
                    response += f"لدينا {len(delayed)} شحنة خارج النطاق الزمني. \n\n"
                    response += "💡 **تحليلي الفني:** هذا النوع من التأخير الجغرافي غالباً ما يعالج بـ 'تغيير المسارات الديناميكي'. هل تريد مني مراجعة السائقين المسؤولين عن هذه المناطق؟"
                else:
                    response = "أبشرك، الأسطول يعمل بكفاءة 100% ولا توجد أي نقطة تأخير جغرافية في الوقت الحالي."

            elif any(word in q for word in ["نصيحة", "رايك", "حل", "اقتراح", "تطوير", "خطة"]):
                response = "بناءً على قراءتي العميقة لأرقام اليوم، إليك خطة العمل المقترحة:\n\n"
                response += f"1. **مواجهة العجز:** {len(low_stock)} أصناف قاربت على الصفر. يجب جدولة أمر شراء استباقي لتجنب توقف الإنتاج.\n"
                response += "2. **تعظيم الربحية:** أقترح تحويل بعض الشاحنات من المناطق المستقرة لدعم المناطق المتأخرة فوراً.\n"
                response += "3. **استدامة العمل:** هل فكرت في ربط هذا النظام ببيانات حركة المرور الحية في الإمارات؟ سيعطينا هذا قدرة على التنبؤ قبل حدوث الأزمة."

            elif any(word in q for word in ["اهلا", "كيف حالك", "مرحبا", "يا"]):
                response = f"أهلاً بك يا أستاذ طارق. كفاءتنا التشغيلية الحالية هي {efficiency:.1f}%. الوضع العام مستقر ولكن لدينا بعض النقاط الحرجة في المخزون. بماذا نبدأ نقاشنا؟"

            else:
                response = "أنا معك تماماً وأفهم تفكيرك الاستراتيجي. هل تود أن نتعمق في تحليل أداء السائقين أم ننتقل لمراجعة موازنة المخازن بين المستودعات؟"

            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- الواجهة الرئيسية (Dashboard) ---
st.markdown("<h1 style='text-align: center;'>🏭 مركز الإدارة والتحليل الاستراتيجي</h1>", unsafe_allow_html=True)

# صف المؤشرات (KPIs)
k1, k2, k3, k4 = st.columns(4)
k1.metric("كفاءة النظام", f"{efficiency:.1f}%")
k2.metric("شاحنات نشطة", len(df_ord[df_ord['الحالة'] != 'تم التسليم ✅']))
k3.metric("تأخيرات 🔴", len(delayed), delta_color="inverse")
k4.metric("إجمالي المخزون", f"{df_inv['الرصيد'].sum():,}")

st.markdown("---")
tab1, tab2, tab3 = st.tabs(["🚛 الرقابة الجغرافية", "📦 توازن المستودعات", "📊 الرؤية البيانية"])

with tab1:
    st.subheader("تحليل حركة الأسطول والمدن")
    st.dataframe(df_ord.sort_values(by='الأهمية'), use_container_width=True)
with tab2:
    st.subheader("مستويات المخزون الحالية")
    st.dataframe(df_inv, use_container_width=True)
with tab3:
    c_l, c_r = st.columns(2)
    with c_l: st.plotly_chart(px.pie(df_ord, names='الحالة', hole=0.4, title="كفاءة التسليم"), use_container_width=True)
    with c_r: st.plotly_chart(px.bar(df_inv, x='المنتج', y='الرصيد', color='المستودع', barmode='group', title="توزيع المخزون"), use_container_width=True)