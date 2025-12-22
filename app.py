import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
import base64

# --- 1. وظيفة تحويل الصورة لترميز يضمن ظهورها كأيقونة (Avatar) ---
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    except Exception:
        return None

# 2. إعدادات الصفحة
st.set_page_config(page_title="Strategic AI Manager", layout="wide", page_icon="👨‍💼")

# 3. تهيئة البيانات المركزية (تحدث مرة واحدة عند التشغيل)
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

# تعريف المتغيرات للتحليل العام
df_ord = st.session_state.df_orders
df_inv = st.session_state.df_inv
delayed = df_ord[df_ord['الحالة'] == 'متأخر 🔴']
low_stock = df_inv[df_inv['الرصيد'] < 500]
efficiency = 100 - (len(delayed)/len(df_ord)*100) if len(df_ord) > 0 else 100

# تحضير أيقونة "المستشار طارق"
user_avatar = get_image_base64("me.jpg")

# --- 4. القائمة الجانبية: المستشار طارق الذكي ---
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
            
            # محاكاة ذكاء ChatGPT في الردود
            if any(word in q for word in ["تحليل", "وضع", "حال", "أين", "تاخير"]):
                cities = delayed['المدينة'].unique()
                response = f"### 📊 تحليل حالة العمليات الحالية\n\n"
                response += f"أهلاً بك يا أستاذ طارق. بعد مراجعة الأرقام اللحظية، أرى أن كفاءة النظام تبلغ **{efficiency:.1f}%**. \n\n"
                if not delayed.empty:
                    response += f"⚠️ **مكمن الخطر:** رصدت تأخيرات في المدن التالية: {', '.join(cities)}. \n"
                    response += f"هناك {len(delayed)} طلبات متعثرة، مما قد يؤثر على سمعة الشركة إذا لم يتم التدخل.\n\n"
                    response += "**💡 اقتراحي الاستراتيجي:** تفعيل بروتوكول 'التحويل السريع' للشاحنات القريبة من مناطق التأخير لدعم الأسطول هناك فوراً."
                else:
                    response += "✅ جميع العمليات تسير وفق الجداول الزمنية. لا توجد معوقات جغرافية حالياً."

            elif any(word in q for word in ["نصيحة", "حل", "تطوير", "خطة", "اقتراح"]):
                response = f"### 🚀 رؤية استشارية لتطوير المصنع\n\n"
                response += "بناءً على المعايير العالمية لإدارة سلاسل الإمداد، أنصحك بالتركيز على ثلاثة محاور:\n\n"
                response += f"1️⃣ **إدارة المخزون:** لدينا {len(low_stock)} أصناف حرجة. الاستمرار في الإنتاج دون تأمين المواد الخام سيعرضنا للتوقف المفاجئ.\n"
                response += "2️⃣ **كفاءة السائقين:** تحليل المسارات يظهر إمكانية دمج رحلات المدن المتقاربة، مما سيوفر قرابة 12% من تكاليف الوقود.\n"
                response += "3️⃣ **التكنولوجيا:** نحتاج للانتقال إلى نظام 'التنبؤ الاستباقي' لنتوقع الأزمات قبل حدوثها بـ 24 ساعة.\n\n"
                response += "**هل ترغب في أن أضع لك جدولاً زمنياً لتنفيذ هذه النقاط؟**"

            elif any(word in q for word in ["اهلا", "كيف حالك", "مرحبا"]):
                response = f"مرحباً بك يا سيدي! أنا في كامل جاهزيتي. \n\n"
                response += f"لقد قمت للتو بمسح شامل للمستودعات والأسطول. الوضع العام **مستقر** بنسبة {efficiency:.1f}%، ولكن هناك تفاصيل في قسم الشحن تستحق نقاشنا. بماذا تحب أن نبدأ؟"
            
            else:
                response = "فهمت سياق حديثك. بصفتي مساعدك الذكي، أنا قادر على تحليل الجداول، التنبؤ بالنواقص، وتقديم حلول لوجستية مفصلة. \n\n"
                response += "**كيف يمكنني خدمتك في اتخاذ القرار القادم؟**"

            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- الواجهة الرئيسية (لوحة التحكم الاستراتيجية) ---
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏛️ مركز الإدارة والتحليل الاستراتيجي</h1>", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
k1.metric("كفاءة النظام", f"{efficiency:.1f}%")
k2.metric("شاحنات نشطة", len(df_ord[df_ord['الحالة'] != 'تم التسليم ✅']))
k3.metric("تأخيرات 🔴", len(delayed), delta_color="inverse")
k4.metric("إجمالي المخزون", f"{df_inv['الرصيد'].sum():,}")

st.markdown("---")
t1, t2, t3 = st.tabs(["🚛 الرقابة الجغرافية", "📦 حالة المستودعات", "📊 الرؤية البيانية"])

with t1:
    st.dataframe(df_ord.sort_values(by='الأهمية'), use_container_width=True)
with t2:
    st.dataframe(df_inv, use_container_width=True)
with t3:
    c_l, c_r = st.columns(2)
    with c_l: st.plotly_chart(px.pie(df_ord, names='الحالة', hole=0.4, title="كفاءة التسليم"), use_container_width=True)
    with c_r: st.plotly_chart(px.bar(df_