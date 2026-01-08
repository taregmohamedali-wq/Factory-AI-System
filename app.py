import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
import os

# --- 1. إعدادات الهوية (صورتك me.jpg) ---
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    return None

st.set_page_config(page_title="Strategic AI Manager", layout="wide", page_icon="👨‍💼")
user_avatar = get_image_base64("me.jpg")

# --- 2. تهيئة البيانات (تثبيت البيانات لضمان منطقية الحوار) ---
if 'db_init' not in st.session_state:
    st.session_state.df_inv = pd.DataFrame([
        {'Warehouse': w, 'Product': p, 'Stock': np.random.randint(50, 4000)}
        for w in ['Dubai Central', 'Abu Dhabi Main', 'Sharjah Hub']
        for p in ['Cola 330ml', 'Cola 1.5L', 'Water 500ml', 'Flour 5kg', 'Pasta']
    ])
    st.session_state.df_orders = pd.DataFrame([
        {'Order': f'ORD-{i}', 'Status': np.random.choice(['Delivered ✅', 'Delayed 🔴', 'In Transit 🚚']),
         'Driver': np.random.choice(['Saeed', 'Ahmed', 'Jasim']), 'City': np.random.choice(['Dubai', 'Abu Dhabi', 'Sharjah'])}
        for i in range(1, 41)
    ])
    st.session_state.chat_history = []
    st.session_state.db_init = True

df_inv = st.session_state.df_inv
df_ord = st.session_state.df_orders

# --- 3. محرك الحوار البشري (Human-Like Reasoning) ---
def human_reasoning_ai(prompt):
    p = prompt.lower()
    # تحليل البيانات فورياً للرد
    low_items = df_inv[df_inv['Stock'] < 800]
    delays = df_ord[df_ord['Status'] == 'Delayed 🔴']
    
    # أ- أسئلة الوضع العام والتحليل العميق
    if any(word in p for word in ['شاييف', 'وضع', 'تقرير', 'كامل', 'عام', 'ايه الاخبار']):
        res = f"أهلاً أستاذ طارق، نظرة عامة على العمليات اليوم تقول أننا في وضع جيد إجمالاً، ولكن هناك نقطتين تحتاجا انتباهك: \n\n"
        res += f"1️⃣ **المخزون:** لدينا {len(low_items)} أصناف بدأت تقترب من حد الخطر، خصوصاً في مستودع الشارقة.\n"
        res += f"2️⃣ **التأخير:** هناك {len(delays)} شحنات متوقفة حالياً. \n\n"
        res += "💡 **رأيي الشخصي:** الأولوية اليوم لتحريك بضاعة من دبي لأبوظبي لتغطية العجز قبل نهاية الدوام."
        return res

    # ب- أسئلة النقص بمرونة
    elif any(word in p for word in ['ناقص', 'نقص', 'خلص', 'مخزون', 'بضاعة']):
        if not low_items.empty:
            item = low_items.iloc[0]
            return f"بصراحة يا فندم، أنا قلق بشأن **{item['Product']}**. الكمية المتوفرة {item['Stock']} فقط في {item['Warehouse']}. هل تريدني أن أجهز لك مسودة طلب توريد؟"
        return "المخازن كلها 'فل' والحمد لله، لا يوجد أي نقص يذكر حالياً."

    # ج- أسئلة السائقين والأداء
    elif any(word in p for word in ['سائق', 'سواق', 'افضل', 'احسن', 'شاطر']):
        top = df_ord[df_ord['Status'] == 'Delivered ✅']['Driver'].value_counts()
        return f"لو سألتني عن بطل اليوم، فهو بالتأكيد **{top.index[0]}**. لقد أكمل {top.values[0]} شحنات بنجاح. يستحق كلمة شكر!"

    # د- أسئلة الطريق والخرائط والذكاء الخارجي
    elif any(word in p for word in ['طريق', 'زحمة', 'شارع', 'اسرع', 'خريطة']):
        return "بناءً على التقارير اللوجستية، شارع الشيخ زايد يشهد كثافة حالياً. أنصح السائقين بأخذ شارع الخيل لتفادي التأخير. هذا سيوفر لنا حوالي 20 دقيقة لكل شحنة متجهة لأبوظبي."

    # هـ- ردود عامة ذكية
    else:
        return "معك يا أستاذ طارق.. هل تقصد الاستفسار عن وضع المخازن حالياً، أم تريدني أن أحلل لك أداء السائقين وتأخيرات المدن؟ أنا جاهز لأي تفصيل."

# --- 4. الواجهة (العودة للشكل القديم المعتمد) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="width:100px;border-radius:50%;border:3px solid #1E3A8A;"></div>', unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center'>المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # عرض الشات
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar=user_avatar if msg["role"] == "assistant" else None):
            st.markdown(msg["content"])

    if prompt := st.chat_input("تحدث معي كخبير عمليات..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        response = human_reasoning_ai(prompt)
        
        with st.chat_message("assistant", avatar=user_avatar):
            st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- 5. الداشبورد (Dashboard) ---
st.markdown("<h1 style='text-align: center;'>🏭 Strategic Operations Center</h1>", unsafe_allow_html=True)

# العدادات الرئيسية
c1, c2, c3 = st.columns(3)
c1.metric("إجمالي المخزون", f"{df_inv['Stock'].sum():,}")
c2.metric("شحنات متأخرة", len(df_ord[df_ord['Status'] == 'Delayed 🔴']))
c3.metric("كفاءة التوصيل", f"{(len(df_ord[df_ord['Status'] == 'Delivered ✅'])/len(df_ord))*100:.1f}%")

st.markdown("---")
# الرسوم البيانية والجداول
tab1, tab2 = st.tabs(["📦 حالة المستودعات", "🚚 مراقبة الأسطول"])
with tab1:
    fig = px.bar(df_inv, x='Product', y='Stock', color='Warehouse', barmode='group', title="توزيع المخزون")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_inv, use_container_width=True)

with tab2:
    st.dataframe(df_ord, use_container_width=True)