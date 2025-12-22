import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
import base64

# --- 1. وظيفة تحويل الصورة لترميز يضمن ظهورها كـ Avatar ---
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    except Exception:
        return None

# 2. إعدادات الصفحة
st.set_page_config(page_title="Strategic AI Manager", layout="wide", page_icon="👨‍💼")

# 3. تهيئة البيانات المركزية (الذكاء المعتمد على البيانات)
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

# تعريف المتغيرات المركزية للتحليل
df_ord = st.session_state.df_orders
df_inv = st.session_state.df_inv
delayed = df_ord[df_ord['الحالة'] == 'متأخر 🔴']
low_stock = df_inv[df_inv['الرصيد'] < 500]
efficiency = 100 - (len(delayed)/len(df_ord)*100) if len(df_ord) > 0 else 100

# تحضير أيقونة "المستشار طارق" (Base64)
user_avatar = get_image_base64("me.jpg")

# --- 4. القائمة الجانبية: المستشار طارق (AI-Driven Logic) ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    
    if user_avatar:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center;">
                <img src="{user_avatar}" 
                     style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 3px solid #1E3A8A;">
            </div>
            """, unsafe_allow_html=True
        )
    
    st.markdown("<h3 style='text-align: center; margin-bottom: 0;'>المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #1E3A8A; font-weight: bold;'>محرك الذكاء الاصطناعي للعمليات</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # عرض الدردشة بأسلوب ChatGPT (ردود ذكية وتفصيلية)
    for msg in st.session_state.chat_history:
        current_avatar = user_avatar if msg["role"] == "assistant" else None
        with st.chat_message(msg["role"], avatar=current_avatar):
            st.markdown(msg["content"])

    if prompt := st.chat_input("ناقشني في وضع العمليات أو اطلب اقتراحات..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=user_avatar):
            q = prompt.lower()
            
            # محرك الردود الذكي المفتوح
            if any(word in q for word in ["تحليل", "وضع", "حال", "أين", "تاخير"]):
                cities = delayed['المدينة'].unique()
                response = f"### 📊 تقرير التحليل اللحظي\n\n"
                response += f"أهلاً بك يا أستاذ طارق. بناءً على قراءتي للبيانات الحالية، أرى أن كفاءة النظام تبلغ **{efficiency:.1f}%**.\n\n"
                if not delayed.empty:
                    response += f"⚠️ **تنبيه عاجل:** رصدت اختناقات في التوزيع بمدن: {', '.join(cities)}. \n"
                    response += f"هناك {len(delayed)} شحنة متأخرة حالياً، وبعضها يخص عملاء VIP.\n\n"
                    response += "**💡 التوصية:** أقترح تحويل مسار أقرب شاحنة نشطة لدعم هذه المناطق فوراً."
                else:
                    response += "✅ العمليات تسير بمثالية تامة ولا توجد أي عوائق لوجستية مسجلة."

            elif any(word in q for word in ["نصيحة", "حل", "تطوير", "خطة", "اقتراح"]):
                response = f"### 🚀 رؤية استراتيجية للتطوير\n\n"
                response += "بصفتي مساعدك الذكي، قمت بمقارنة أداء المصنع بأفضل الممارسات العالمية، وإليك خطة العمل:\n\n"
                response += f"1️⃣ **أمن المخزون:** لدينا {len(low_stock)} أصناف تحت حد الأمان. يجب المبادرة بطلب توريد لتجنب توقف خطوط الإنتاج.\n"
                response += "2️⃣ **كفاءة النقل:** دمج الرحلات المتقاربة في 'دبي والشارقة' سيوفر ما يقارب 12% من تكاليف التشغيل.\n"
                response += "3️⃣ **التحول الاستباقي:** أنصح ببدء استخدام نظام التنبؤ بالطلب (Demand Forecasting) لتقليل الهالك.\n\n"
                response += "**هل تريد مني تفصيل أي من هذه النقاط بشكل أكبر؟**"
            
            elif any(word in q for word in ["اهلا", "كيف حالك", "مرحبا"]):
                response = f"مرحباً بك يا سيدي! أنا في جاهزية تامة. قمت للتو بمراجعة كافة المستودعات والأسطول، والوضع العام مستقر بنسبة {efficiency:.1f}%. بماذا ترغب في البدء؟"
            
            else:
                response = "أفهم اهتمامك. بصفتي 'عقلك الثاني' في الإدارة، يمكنني تحليل أي جزء من العمليات، بدءاً من أداء السائقين وصولاً إلى توازن المخازن. ما هي الخطوة القادمة؟"

            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- 5. الواجهة الرئيسية (لوحة التحكم الاستراتيجية) ---
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏛️ مركز الإدارة والتحليل الاستراتيجي</h1>", unsafe_allow_html=True)

# صف المؤشرات (KPIs)
k1, k2, k3, k4 = st.columns(4)
k1.metric("كفاءة النظام", f"{efficiency:.1f}%")
k2.metric("شاحنات نشطة", len(df_ord[df_ord['الحالة'] != 'تم التسليم ✅']))
k3.metric("تأخيرات 🔴", len(delayed), delta_color="inverse")
k4.metric("إجمالي المخزون", f"{df_inv['الرصيد'].sum():,}")

st.markdown("---")
t1, t2, t3 = st.tabs(["🚛 الرقابة الجغرافية", "📦 حالة المستودعات", "📊 الرؤية البيانية"])

with t1:
    st.subheader("تحليل حركة الأسطول والمدن")
    st.dataframe(df_ord.sort_values(by='الأهمية'), use_container_width=True)
with t2:
    st.subheader("مستويات المخزون الحالية")
    st.dataframe(df_inv, use_container_width=True)
with t3:
    c_l, c_r = st.columns(2)
    with c_l: 
        st.plotly_chart(px.pie(df_ord, names='الحالة', hole=0.4, title="كفاءة التسليم"), use_container_width=True)
    with c_r: 
        st.plotly_chart(px.bar(df_inv, x='المنتج', y='الرصيد', color='المستودع', barmode='group', title="توزيع المخزون الاستراتيجي"), use_container_width=True)