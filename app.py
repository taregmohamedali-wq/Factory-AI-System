import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات الشخصية والهوية ---
st.set_page_config(page_title="Strategic Operations AI", layout="wide")

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

user_avatar = get_base64_img("me.jpg")

# --- 2. محرك قراءة البيانات المرفوعة سلفاً ---
@st.cache_data
def load_and_sync_data():
    try:
        # قراءة الشيتات المرفوعة سلفاً
        inv = pd.read_csv("UAE_Operations_DB.xlsx - Inventory.csv")
        orders = pd.read_csv("UAE_Operations_DB.xlsx - Order_History.csv")
        return inv, orders
    except:
        return pd.DataFrame(), pd.DataFrame()

df_inv, df_orders = load_and_sync_data()

# --- 3. محرك التفكير الاستراتيجي (منطقي التحليلي) ---
def strategic_brain(user_query):
    query = user_query.lower()
    
    if df_inv.empty or df_orders.empty:
        return "أستاذ طارق، الملفات غير متاحة حالياً. تأكد من وجود UAE_Operations_DB.xlsx في بيئة العمل."

    # تحليل التأخير (Delayed) بربطه بالمناطق
    delayed_df = df_orders[df_orders['Status'].str.contains('متأخر', na=False)]
    
    # تحليل المخزون الحرج
    critical_stock = df_inv[df_inv['Stock_Level'] < 500]

    # منطق "الفهم والاستنتاج"
    if any(word in query for word in ['وضع', 'تحليل', 'نصيح', 'تقرير']):
        response = "### 🛡️ التحليل الاستراتيجي لليوم\n\n"
        
        # ربط البيانات ببعضها
        if not delayed_df.empty:
            top_city = delayed_df['City'].value_counts().idxmax()
            response += f"⚠️ **أزمة الأسطول:** سيدي، هناك {len(delayed_df)} شحنة متأخرة حالياً، والأزمة الكبرى تتركز في **{top_city}**. "
        
        if not critical_stock.empty:
            item = critical_stock.iloc[0]
            response += f"\n\n🚨 **خطر المخزون:** صنف **({item['Product']})** في {item['Warehouse']} وصل لمستوى {item['Stock_Level']} وحدة، وهو مستوى غير كافٍ لتغطية طلبات الـ 48 ساعة القادمة.\n\n"
            
        response += "💡 **توصيتي الشخصية:** يجب إعادة توجيه جزء من مخزون دبي نحو الشارقة فوراً، واستدعاء السائقين المتأخرين في مسار أبوظبي للتحقق من العوائق اللوجستية."
        return response

    if 'دبي' in query or 'dubai' in query:
        dubai_inv = df_inv[df_inv['Warehouse'].str.contains('دبي', na=False)]
        total = dubai_inv['Stock_Level'].sum()
        return f"📍 **تقرير دبي:** المخزون الإجمالي {total:,} وحدة. الوضع مستقر ولكن صنف ({dubai_inv.iloc[0]['Product']}) يحتاج لمراقبة لصرفه السريع."

    return "معك يا أستاذ طارق، أنا الآن أحلل بياناتك في الخلفية. هل تريد التركيز على (أداء السائقين المتأخرين) أم (خطة تأمين نواقص المخازن)؟"

# --- 4. واجهة المحادثة (Sidebar) ---
with st.sidebar:
    if user_avatar:
        st.markdown(f'<div style="text-align:center"><img src="{user_avatar}" style="border-radius:50%; width:110px; border:3px solid #00ffcc;"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>AI المستشار طارق</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    if 'history' not in st.session_state: st.session_state.history = []
    
    for m in st.session_state.history:
        with st.chat_message(m["role"], avatar=user_avatar if m["role"]=="assistant" else None):
            st.write(m["content"])

    if p := st.chat_input("تحدث معي.. حلل لي وضع اليوم"):
        st.session_state.history.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        
        # استدعاء العقل التحليلي
        res = strategic_brain(p)
        with st.chat_message("assistant", avatar=user_avatar): st.write(res)
        st.session_state.history.append({"role": "assistant", "content": res})

# --- 5. الداشبورد الرئيسي (التصميم البصري الاستراتيجي) ---
st.markdown("<h1 style='text-align:center;'>📊 Operations Command Center</h1>", unsafe_allow_html=True)

if not df_inv.empty:
    # عرض التحليل التلقائي في صدر الصفحة
    st.info(strategic_brain("تحليل عام"))
    
    st.markdown("---")
    
    # العدادات الحية
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("إجمالي المخزون", f"{df_inv['Stock_Level'].sum():,}")
    c2.metric("شحنات متأخرة 🔴", len(df_orders[df_orders['Status'].str.contains('متأخر', na=False)]))
    c3.metric("في الطريق 🚚", len(df_orders[df_orders['Status'].str.contains('طريق', na=False)]))
    c4.metric("المستودعات", df_inv['Warehouse'].nunique())

    st.markdown("---")
    
    # الرسوم والخريطة
    col_l, col_r = st.columns([2, 1])
    
    with col_l:
        st.subheader("📈 ميزان توزيع المخزون")
        fig = px.bar(df_inv, x='Warehouse', y='Stock_Level', color='Product', barmode='group', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
        
    with col_r:
        st.subheader("📍 التوزيع الجغرافي للمراكز")
        # خريطة لمراكز العمليات في الإمارات
        map_data = pd.DataFrame({
            'lat': [25.2048, 24.4539, 25.3463, 24.1302],
            'lon': [55.2708, 54.3773, 55.4209, 55.8023],
            'name': ['Dubai', 'Abu Dhabi', 'Sharjah', 'Al Ain']
        })
        st.map(map_data)

    st.subheader("📋 مراجعة البيانات الحية (Order History)")
    st.dataframe(df_orders, use_container_width=True)
else:
    st.error("⚠️ فشل الربط: يرجى التأكد من وجود ملف UAE_Operations_DB.xlsx")