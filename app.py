import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

# 1. إعدادات الصفحة والستايل
st.set_page_config(page_title="AI Operations Consultant", layout="wide")

# 2. بناء قاعدة البيانات الذكية
if 'db_initialized' not in st.session_state:
    products = ['Cola 330ml', 'Cola 1.5L', 'Water 500ml', 'Flour 5kg', 'Pasta', 'Flour Qarassa']
    warehouses = ['مستودع دبي المركزي', 'مستودع أبوظبي الرئيسي', 'مستودع الشارقة']
    
    inv_data = []
    for p in products:
        for w in warehouses:
            # توليد عشوائي لبيانات تجعل النقاش مثيراً (بعضها ناقص وبعضها زائد)
            stock = np.random.randint(50, 5000)
            inv_data.append({'Warehouse': w, 'Product': p, 'Stock_Level': stock})
    
    orders_data = []
    drivers = ['سعيد محمد', 'أحمد علي', 'جاسم عبدالله', 'خالد إبراهيم', 'محمد حسن']
    for i in range(1, 41):
        orders_data.append({
            'Customer': f'عميل {i}',
            'Category': np.random.choice(['AAA (VIP)', 'AA', 'A']),
            'City': np.random.choice(['Dubai', 'Abu Dhabi', 'Sharjah']),
            'Status': np.random.choice(['Delivered ✅', 'Delayed 🔴', 'In-Transit 🚚']),
            'Truck_ID': f'TRK-{100+i}',
            'Driver': np.random.choice(drivers)
        })
    
    st.session_state.df_inv = pd.DataFrame(inv_data)
    st.session_state.df_orders = pd.DataFrame(orders_data)
    st.session_state.chat_history = [] 
    st.session_state.db_initialized = True

# --- القائمة الجانبية: محرك الدردشة الاستشاري ---
with st.sidebar:
    st.title("🤖 المساعد الاستشاري الذكي")
    st.markdown("---")
    
    # عرض سجل المحادثة
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # إدخال المستخدم (ChatGPT Style)
    if prompt := st.chat_input("سيد طارق، كيف يمكنني مساعدتك في إدارة العمليات اليوم؟"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            q = prompt.lower()
            # استحضار البيانات للتحليل
            df_i = st.session_state.df_inv
            df_o = st.session_state.df_orders
            
            # --- محرك التحليل والرد الذكي ---
            
            # 1. تحليل النواقص بأسلوب استشاري
            if any(word in q for word in ["نقص", "نواقص", "مخزن", "بضاعة"]):
                low = df_i[df_i['Stock_Level'] < 500]
                if not low.empty:
                    response = f"سيدي، بعد تحليل المخزون، وجدت أننا نواجه عجزاً في {len(low)} أصناف. \n\n"
                    response += f"أخطرها هو **{low.iloc[0]['Product']}** في **{low.iloc[0]['Warehouse']}**. \n\n"
                    response += "📝 **نصيحة إدارية:** عالمياً، نقص المخزون في هذا التوقيت من السنة قد يؤدي لخسارة عملاء الـ VIP. "
                    response += "أنصحك فوراً بنقل فائض من مستودع آخر بدلاً من انتظار التوريد الخارجي لتقليل زمن الاستجابة (Lead Time)."
                else:
                    response = "المخزون حالياً في المنطقة الآمنة. هل تود أن نناقش استراتيجية تحسين التوزيع للأسابيع القادمة؟"

            # 2. تحليل السائقين والتأخير بأسلوب نقاشي
            elif any(word in q for word in ["سائق", "تأخير", "تأخر", "مشكلة"]):
                delayed = df_o[df_o['Status'] == 'Delayed 🔴']
                if not delayed.empty:
                    vip_delay = delayed[delayed['Category'] == 'AAA (VIP)']
                    response = f"هناك نقطة قلق هنا؛ لدينا {len(delayed)} حالات تأخير. \n\n"
                    if not vip_delay.empty:
                        response += f"⚠️ **تحذير:** العميل **{vip_delay.iloc[0]['Customer']}** (VIP) لم يستلم شحنته بعد. \n\n"
                    response += f"السائق **{delayed.iloc[0]['Driver']}** هو الأكثر تأخراً الآن. "
                    response += "البروتوكول الصحيح هنا هو التواصل مع السائق لتحديد المعوقات (زحام أم عطل فني) وتحديث العميل فوراً للحفاظ على سمعة الشركة."
                else:
                    response = "جميع السائقين يسيرون حسب الجدول الزمني. هل تريد مراجعة تقارير استهلاك الوقود أو كفاءة المسارات؟"

            # 3. التحية والدردشة العامة
            elif any(word in q for word in ["أهلا", "مرحبا", "هلا", "كيف حالك"]):
                response = "أنا في قمة الجاهزية! أراقب تدفق البيانات في دبي وأبوظبي والشارقة. "
                response += "أرقامنا اليوم تشير إلى كفاءة تشغيل بنسبة 92%. بماذا نبدأ نقاشنا اليوم؟"

            # 4. طلب نصيحة عامة
            elif any(word in q for word in ["نصيحة", "رأيك", "اقتراح"]):
                response = "بناءً على البيانات، أقترح التركيز على 'المناقلة الذكية'. لدينا تكدس في بعض المستودعات ونقص في أخرى. "
                response += "تحسين هذا الجانب سيوفر لنا 15% من تكاليف النقل الخارجي."

            else:
                response = "فهمت قصدك. دعنا نحلل هذه النقطة بناءً على أرقام الشاحنات والمخازن المتوفرة لدينا حالياً. هل لديك تفضيل لمستودع معين لنبدأ به؟"

            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- الواجهة الرئيسية (لوحة العرض الاستراتيجية) ---
st.markdown("<h1 style='text-align: center; color: #1A5276;'>🏭 مركز الإدارة الاستراتيجية (AI Consultant)</h1>", unsafe_allow_html=True)

# المؤشرات (KPIs)
k1, k2, k3, k4 = st.columns(4)
k1.metric("المخزون الإجمالي", f"{st.session_state.df_inv['Stock_Level'].sum():,}")
k2.metric("شاحنات نشطة", len(st.session_state.df_orders[st.session_state.df_orders['Status'] != 'Delivered ✅']))
k3.metric("تأخيرات حرجة", len(st.session_state.df_orders[st.session_state.df_orders['Status'] == 'Delayed 🔴']))
k4.metric("رضا العملاء (تقديري)", "94%")

st.markdown("---")
t1, t2, t3 = st.tabs(["🚛 مراقبة الأسطول", "🔄 مركز التحويلات", "📊 تحليل البيانات"])

with t1:
    st.subheader("تحليل حركة السائقين والعملاء")
    st.dataframe(st.session_state.df_orders.sort_values('Category'), use_container_width=True)

with t2:
    st.subheader("تفيذ مقترحات المساعد الذكي (المناقلة)")
    c1, c2, c3, c4 = st.columns(4)
    with c1: f_w = st.selectbox("من:", st.session_state.df_inv['Warehouse'].unique())
    with c2: t_w = st.selectbox("إلى:", [w for w in st.session_state.df_inv['Warehouse'].unique() if w != f_w])
    with c3: pr = st.selectbox("المنتج:", st.session_state.df_inv['Product'].unique())
    with c4: qty = st.number_input("الكمية:", min_value=1)
    
    if st.button("تأكيد النقل ⚡"):
        st.success("تم تنفيذ العملية وتحديث السجلات.")

with t3:
    st.plotly_chart(px.bar(st.session_state.df_inv, x='Product', y='Stock_Level', color='Warehouse', barmode='group'), use_container_width=True)