import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. إعدادات الصفحة
st.set_page_config(page_title="Strategic AI Manager", layout="wide")

# 2. تهيئة البيانات والذاكرة المركزية (Global State)
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

# --- تعريف المتغيرات المركزية (لحل مشكلة NameError تماماً) ---
df_ord = st.session_state.df_orders
df_inv = st.session_state.df_inv
delayed = df_ord[df_ord['الحالة'] == 'متأخر 🔴']
low_stock = df_inv[df_inv['الرصيد'] < 500]
efficiency = 100 - (len(delayed)/len(df_ord)*100) if len(df_ord) > 0 else 100

# --- القائمة الجانبية: المستشار الذكي (تفاعل كامل) ---
with st.sidebar:
    st.header("👨‍💼 المستشار الاستراتيجي AI")
    st.info("أنا الآن أحلل بياناتك وأقارنها بمعايير السوق العالمية.")
    st.markdown("---")
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("تحدث معي.. كيف نحسن العمل اليوم؟"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            q = prompt.lower()
            
            # منطق الرد المفتوح والتفاعلي
            if any(word in q for word in ["أين", "تاخير", "تاخر", "وين", "مشكلة"]):
                if not delayed.empty:
                    c_list = delayed['المدينة'].unique()
                    response = f"أستاذ طارق، لقد رصدت اختناقات في التوزيع حالياً في **{', '.join(c_list)}**. \n\n"
                    response += f"لدينا {len(delayed)} شحنات خارج الجدول الزمني. "
                    response += "عالمياً، يُنصح في هذه الحالات بتفعيل 'إدارة الاستثناءات'؛ أي التركيز فقط على شحنات VIP المتأخرة أولاً لتقليل الضرر الاستراتيجي."
                else:
                    response = "جميع المسارات خضراء اليوم! الأسطول يتحرك بكفاءة مثالية."

            elif any(word in q for word in ["نصيحة", "رايك", "حل", "اقتراح", "تطوير"]):
                response = "بناءً على ذكاء العمليات، إليك 3 مقترحات لتحسين المصنع: \n\n"
                response += f"1. **المخازن:** {len(low_stock)} أصناف في خطر. أنصح بطلب توريد استباقي (Proactive Ordering). \n"
                response += "2. **الأسطول:** دمج شحنات 'الشارقة' و'دبي' المتقاربة لتوفير 15% من وقود الشاحنات. \n"
                response += "3. **العملاء:** تحديث عملاء الـ VIP آلياً بحالة شحناتهم لرفع نسبة الرضا."

            elif any(word in q for word in ["اهلا", "كيف حالك", "مرحبا", "يا"]):
                response = f"أهلاً بك يا أستاذ طارق. أنا في جاهزية تامة. كفاءتنا الحالية {efficiency:.1f}%. هل نناقش خطة رفع هذه النسبة اليوم؟"

            else:
                response = "فهمت قصدك. أنا هنا لأناقش معك أي تفصيل إداري. هل نبدأ بتحليل أداء السائقين أم نراجع توازن المستودعات؟"

            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- الواجهة الرئيسية (لوحة التحكم الاستراتيجية) ---
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏛️ مركز الإدارة والتحليل الاستراتيجي</h1>", unsafe_allow_html=True)

# صف المؤشرات (KPIs) - تعمل الآن بأمان 100%
k1, k2, k3, k4 = st.columns(4)
k1.metric("كفاءة النظام", f"{efficiency:.1f}%")
k2.metric("شاحنات نشطة", len(df_ord[df_ord['الحالة'] != 'تم التسليم ✅']))
k3.metric("تأخيرات 🔴", len(delayed), delta_color="inverse")
k4.metric("إجمالي المخزون", f"{df_inv['الرصيد'].sum():,}")

st.markdown("---")
t1, t2, t3 = st.tabs(["🚛 الرقابة الجغرافية", "📦 حالة المستودعات", "📊 الرؤية البيانية"])

with t1:
    st.subheader("تفاصيل حركة الأسطول والمدن")
    st.dataframe(df_ord.sort_values(by='الأهمية'), use_container_width=True)
with t2:
    st.subheader("مستويات المخزون الحالية")
    st.dataframe(df_inv, use_container_width=True)
with t3:
    col_l, col_r = st.columns(2)
    with col_l: st.plotly_chart(px.pie(df_ord, names='الحالة', hole=0.4, title="كفاءة التسليم"), use_container_width=True)
    with col_r: st.plotly_chart(px.bar(df_inv, x='المنتج', y='الرصيد', color='المستودع', barmode='group', title="توزيع المخزون"), use_container_width=True)