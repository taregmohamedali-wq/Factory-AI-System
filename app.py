import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
import os

# --- 1. إعدادات الهوية والتصميم (Dark Professional Theme) ---
st.set_page_config(page_title="Strategic Operations Hub", layout="wide", page_icon="👨‍💼")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_avatar = get_base64("me.jpg")

# --- 2. محرك البيانات الحية ---
if 'db' not in st.session_state:
    st.session_state.df_inv = pd.DataFrame([
        {'Warehouse': w, 'Product': p, 'Stock': np.random.randint(50, 4000)}
        for w in ['Dubai Central', 'Abu Dhabi Main', 'Sharjah Hub']
        for p in ['Cola 330ml', 'Cola 1.5L', 'Water 500ml', 'Flour 5kg', 'Pasta']
    ])
    st.session_state.df_ord = pd.DataFrame([
        {'Order': f'ORD-{100+i}', 'Status': np.random.choice(['Delivered ✅', 'Delayed 🔴', 'In Transit 🚚']),
         'City': np.random.choice(['Dubai', 'Abu Dhabi', 'Sharjah', 'Al Ain']),
         'Driver': np.random.choice(['Saeed', 'Ahmed', 'Jasim', 'Khaled', 'Mohamed']),
         'Time': np.random.randint(50, 500)} for i in range(60)
    ])
    st.session_state.chat_history = []
    st.session_state.context = "general" # ذاكرة السياق

# --- 3. محرك "الذكاء الاستشاري" (يعمل بمنطق الحوار البشري) ---
def brain_engine(user_input):
    q = user_input.lower()
    inv = st.session_state.df_inv
    ord = st.session_state.df_ord
    
    # تحليلات خلفية لاتخاذ القرار
    delays = ord[ord['Status'] == 'Delayed 🔴']
    low_stock = inv[inv['Stock'] < 600]
    
    # منطق الفهم المترابط (Contextual Reasoning)
    
    # 1. إذا سأل عن التأخير أو المشاكل
    if any(word in q for word in ['تاخير', 'مشكلة', 'متاخر', 'delay', 'late']):
        st.session_state.context = "delays"
        return (f"أهلاً أستاذ طارق. بتحليل الأسطول حالياً، رصدت **{len(delays)} شحنة متأخرة**. "
                f"أكبر تجمع للتأخير موجود في **{delays['City'].value_counts().idxmax()}**. "
                f"أنصحك بالتركيز على السائق **{delays.iloc[0]['Driver']}** لأنه يحمل الشحنة الأكثر قدماً.")

    # 2. إذا سأل عن النقص أو المخازن
    elif any(word in q for word in ['نقص', 'بضاعة', 'مخزون', 'خلص', 'stock']):
        st.session_state.context = "inventory"
        if not low_stock.empty:
            item = low_stock.sort_values('Stock').iloc[0]
            return (f"سيدي، لدينا عجز حرج في **{item['Product']}** بمستودع **{item['Warehouse']}** (الرصيد: {item['Stock']}). "
                    f"هذا النقص قد يوقف عمليات التوزيع غداً. هل تريد مني جدولة أمر توريد عاجل؟")
        return "المخزون ممتاز في جميع الفروع حالياً، ولا توجد مؤشرات خطر."

    # 3. إذا سأل عن الطرق أو المسارات (محاكاة الإنترنت)
    elif any(word in q for word in ['طريق', 'زحمة', 'شارع', 'route', 'traffic']):
        return ("بناءً على التحديثات اللوجستية في الإمارات: \n"
                "* **المسار الأفضل:** شارع محمد بن زايد (E311) سالك الآن. \n"
                "* **تنبيه:** تجنب منطقة القوز في دبي لوجود كثافة مرورية عالية. \n"
                "* **نصيحة:** وجه السائقين لاتخاذ المخرج 45 لتوفير 15 دقيقة من زمن التوصيل.")

    # 4. الرد على المتابعة (مثل: كمل، طيب، ماذا أيضاً)
    elif any(word in q for word in ['كمل', 'طيب', 'نعم', 'ايه كمان', 'more']):
        if st.session_state.context == "delays":
            return "بالإضافة للتأخيرات، لاحظت أن معدل استهلاك الوقود يرتفع في شاحنات أبوظبي، قد نحتاج لمراجعة صيانة المحركات."
        return "بالتأكيد، يمكننا أيضاً تحليل أداء السائقين بشكل فردي أو مراجعة خطة التوزيع للأسبوع القادم. بماذا ترغب؟"

    # 5. رد ذكي لأي سؤال غير مفهوم (مستشار ذكي)
    else:
        return ("أنا معك يا أستاذ طارق. سأقوم الآن بالبحث في بيانات المخازن وحالة الطرق.. "
                "هل تود أن أعطيك تقريراً عن (النواقص الحالية) أم (أسرع مسارات الشاحنات)؟")

# --- 4. تصميم الواجهة الجانبية (الشات الاستشاري) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="width:100px;border-radius:50%;border:3px solid #00FFCC;object-fit:cover;"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center'>المستشار طارق AI</h3>", unsafe_allow_html=True)
    st.markdown("---")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar=user_avatar if msg["role"] == "assistant" else None):
            st.markdown(msg["content"])

    if prompt := st.chat_input("تحدث معي كشريك استراتيجي..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        answer = brain_engine(prompt)
        with st.chat_message("assistant", avatar=user_avatar):
            st.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

# --- 5. الواجهة الرئيسية (The Strategic Dashboard) ---
st.markdown("<h1 style='text-align: center;'>📊 Strategic Operations Hub</h1>", unsafe_allow_html=True)

# المؤشرات العليا
c1, c2, c3, c4 = st.columns(4)
c1.metric("إجمالي المخزون", f"{st.session_state.df_inv['Stock'].sum():,}")
c2.metric("شحنات متأخرة", len(st.session_state.df_ord[st.session_state.df_ord['Status'] == 'Delayed 🔴']), delta="-2", delta_color="inverse")
c3.metric("نسبة النجاح", f"{(len(st.session_state.df_ord[st.session_state.df_ord['Status'] == 'Delivered ✅'])/60)*100:.1f}%")
c4.metric("السائق المثالي", "Saeed")

st.markdown("---")
# الرسوم البيانية المتطورة (مثل صورك تماماً)
l_col, r_col = st.columns([2, 1])

with l_col:
    st.subheader("📈 تحليل تدفق المنتجات وزمن التسليم")
    fig = px.area(st.session_state.df_ord.sort_values('City'), x='City', y='Time', color='Driver', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with r_col:
    st.subheader("💡 نصيحة استشارية")
    st.warning("بناءً على معايير (Supply Chain Excellence)، نقترح نقل جزء من مخزون دبي لدعم فرع العين اليوم.")
    
    st.subheader("🌍 مراقبة المواقع (Live)")
    st.map(pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]}))

st.subheader("📋 تفاصيل الحالة التشغيلية")
st.dataframe(st.session_state.df_inv, use_container_width=True)