import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. بناء الهوية البصرية (طارق الرقمي) ---
st.set_page_config(page_title="Strategic Operations AI", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

# جلب صورتك الشخصية (تأكد أن الملف me.jpg موجود بجانب الكود)
user_avatar = get_base64_img("me.jpg")

# --- 2. محرك الربط بملف الإكسل المرفوع (xlsx) ---
@st.cache_data
def load_and_sync_data():
    file_path = "UAE_Operations_DB.xlsx"
    if os.path.exists(file_path):
        try:
            # قراءة الشيتات مباشرة من ملف الإكسل
            df_inv = pd.read_excel(file_path, sheet_name='Inventory')
            df_orders = pd.read_excel(file_path, sheet_name='Order_History')
            return df_inv, df_orders
        except Exception as e:
            st.error(f"حدث خطأ في قراءة ملف الإكسل: {e}")
            return pd.DataFrame(), pd.DataFrame()
    return pd.DataFrame(), pd.DataFrame()

df_inv, df_orders = load_and_sync_data()

# --- 3. عقل المستشار (التفكير والتحليل بمنطق الذكاء الاصطناعي) ---
def strategic_ai_thought(query):
    if df_inv.empty or df_orders.empty:
        return "أستاذ طارق، أنا هنا وجاهز، لكنني لا أستطيع الوصول لشيتات الإكسل. يرجى التأكد من اسم الملف."

    q = query.lower()
    
    # استخراج الحقائق اللحظية للتحليل
    delayed = df_orders[df_orders['Status'].str.contains('متأخر', na=False)]
    critical_stock = df_inv[df_inv['Stock_Level'] < 600]
    
    # منطق "الفهم والتحليل المفتوح"
    if any(word in q for word in ['وضع', 'تحليل', 'ماذا هناك', 'نصيحة', 'تقرير']):
        top_city_issue = delayed['City'].value_counts().idxmax() if not delayed.empty else "لا يوجد"
        
        response = f"### 🛡️ التقرير الاستراتيجي لليوم - أستاذ طارق\n\n"
        response += f"سيدي، بعد تحليل {len(df_orders)} عملية جارية، وجدت أن **{len(delayed)} شحنة** تواجه تأخيراً، وأغلبها يتركز في مسارات **{top_city_issue}**. "
        
        if not critical_stock.empty:
            item = critical_stock.iloc[0]
            response += f"أما المخزون، فهناك خطر حقيقي في **{item['Warehouse']}** لنفاذ صنف **({item['Product']})** حيث الرصيد الحالي {item['Stock_Level']} وحدة فقط. \n\n"
        
        response += "💡 **رؤيتي للموقف:** الأداء العام يحتاج تدخلاً في توزيع المخزون. أنصح بتحويل جزء من فائض مستودع دبي لدعم الشارقة فوراً، وتنبيه السائقين في المناطق المتأخرة لتفادي الازدحام."
        return response

    return "معك يا أستاذ طارق، أفكر معك في حلول للعمليات. هل تريد تحليل (كفاءة السائقين) أم (نواقص المستودعات)؟"

# --- 4. واجهة المحادثة التفاعلية (Sidebar) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:110px; border:3px solid #00ffcc; box-shadow: 0px 4px 15px rgba(0,255,204,0.3);"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>AI المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'history' not in st.session_state: st.session_state.history = []
    for m in st.session_state.history:
        with st.chat_message(m["role"], avatar=user_avatar if m["role"]=="assistant" else None):
            st.write(m["content"])

    if prompt := st.chat_input("تحدث معي.. كيف ترى وضع اليوم؟"):
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        response = strategic_ai_thought(prompt)
        with st.chat_message("assistant", avatar=user_avatar): st.write(response)
        st.session_state.history.append({"role": "assistant", "content": response})

# --- 5. الداشبورد الاحترافي (الخريطة والرسوم والبيانات) ---
st.markdown("<h1 style='text-align:center;'>📊 Strategic Operations Hub</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    # المنطقة 1: التحليل الذكي التلقائي (الذي يظهر في الأعلى)
    st.info(strategic_ai_thought("تحليل عام"))
    
    st.markdown("---")
    
    # المنطقة 2: العدادات (KPIs)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("إجمالي المخزون", f"{df_inv['Stock_Level'].sum():,}")
    k2.metric("شحنات متأخرة 🔴", len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)]))
    k3.metric("تحت التسليم 🚚", len(df_orders[df_orders['Status'].str.contains('طريق', na=False)]))
    k4.metric("تغطية المستودعات", df_inv['Warehouse'].nunique())

    st.markdown("---")
    
    # المنطقة 3: الرسوم البيانية والخريطة
    col_chart, col_map = st.columns([2, 1])
    
    with col_chart:
        st.subheader("📈 مستويات المخزون (منتج / موقع)")
        fig = px.bar(df_inv, x='Warehouse', y='Stock_Level', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
        
    with col_map:
        st.subheader("📍 التوزيع الجغرافي للمراكز")
        # خريطة مواقع العمليات الرئيسية
        map_df = pd.DataFrame({'lat': [25.2, 24.4, 25.3], 'lon': [55.3, 54.4, 55.4]})
        st.map(map_df)

    st.subheader("📋 سجل العمليات الحي (Order History)")
    st.dataframe(df_orders, use_container_width=True)
else:
    st.error("⚠️ الملف غير موجود أو تالف. تأكد من وجود UAE_Operations_DB.xlsx في نفس المجلد.")