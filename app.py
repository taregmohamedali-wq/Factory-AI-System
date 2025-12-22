import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="المدير التنفيذي الذكي | AI Operations", layout="wide")

# 2. تهيئة البيانات والذاكرة الذكية (Session State)
if 'db_initialized' not in st.session_state:
    products = ['Cola 330ml', 'Cola 1.5L', 'Water 500ml', 'Flour 5kg', 'Pasta', 'Flour Qarassa']
    warehouses = ['مستودع دبي المركزي', 'مستودع أبوظبي الرئيسي', 'مستودع الشارقة']
    
    inv_data = []
    for p in products:
        for w in warehouses:
            # تعمدنا وضع مستويات منخفضة لبعض المواد لاختبار الذكاء
            stock = np.random.choice([np.random.randint(100, 400), np.random.randint(1000, 5000)])
            inv_data.append({'Warehouse': w, 'Product': p, 'Stock_Level': stock})
    
    orders_data = []
    drivers_list = ['سعيد محمد', 'أحمد علي', 'جاسم عبدالله', 'خالد إبراهيم', 'محمد حسن']
    for i in range(1, 41):
        orders_data.append({
            'Customer_ID': f'CUST-{i:03d}',
            'Category': np.random.choice(['AAA (أهمية قصوى)', 'AA (عالية)', 'A (عادي)']),
            'City': np.random.choice(['Dubai', 'Abu Dhabi', 'Sharjah']),
            'Status': np.random.choice(['Delivered ✅', 'Delayed 🔴', 'In-Transit 🚚']),
            'Truck_ID': f'TRK-{100+i}',
            'Driver': np.random.choice(drivers_list)
        })
    
    st.session_state.df_inv = pd.DataFrame(inv_data)
    st.session_state.df_orders = pd.DataFrame(orders_data)
    st.session_state.chat_history = [] 
    st.session_state.db_initialized = True

# --- القائمة الجانبية: موظف العمليات الذكي ---
with st.sidebar:
    st.title("👨‍💼 موظف العمليات الذكي")
    st.markdown("---")
    
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("تحدث معي، اسأل عن السائقين أو المخازن..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            q = prompt.lower()
            df_o = st.session_state.df_orders
            df_i = st.session_state.df_inv
            
            # --- منطق الرد المباشر والتحليلي ---
            
            # 1. تحليل نواقص المخازن (مباشر)
            if any(word in q for word in ["نقص", "نواقص", "مخزن", "مخازن", "بضاعة"]):
                low_stock = df_i[df_i['Stock_Level'] < 500]
                if not low_stock.empty:
                    response = "📝 **تقرير النواقص العاجل سيدي:**\n\n"
                    for _, item in low_stock.iterrows():
                        response += f"• **{item['Product']}** في **{item['Warehouse']}**: الرصيد الحالي ({item['Stock_Level']}) وحدة فقط. ⚠️\n"
                    response += "\n💡 **التوصية:** أقترح البدء بعملية تحويل من أقرب مستودع به وفرة لتغطية الطلبيات القادمة."
                else:
                    response = "✅ قمت بفحص جميع الرفوف في المستودعات، والمخزون حالياً فوق حد الأمان في كل الفروع."
            
            # 2. تحليل السائقين والأسطول (مباشر)
            elif any(word in q for word in ["سائق", "سواق", "driver", "شاحنة", "تأخير"]):
                delayed = df_o[df_o['Status'] == 'Delayed 🔴']
                response = f"📊 **تحليل الأسطول اللحظي:**\n\n"
                response += f"• إجمالي الشاحنات: {len(df_o)}\n"
                response += f"• شاحنات في الطريق: {len(df_o[df_o['Status'] == 'In-Transit 🚚'])}\n"
                if not delayed.empty:
                    response += f"• **تنبيه:** لدينا {len(delayed)} حالات تأخير.\n"
                    response += f"• السائق الأكثر تأخراً هو **{delayed.iloc[0]['Driver']}** (الشاحنة {delayed.iloc[0]['Truck_ID']}) في مدينة {delayed.iloc[0]['City']}."
                else:
                    response += "• الوضع ممتاز، لا توجد أي بلاغات تأخير حالياً."

            # 3. التحية
            elif any(word in q for word in ["أهلا", "مرحبا", "هلا", "كيف حالك"]):
                response = "أهلاً بك سيدي! أنا أراقب البيانات الآن وجاهز لتحليل أي جزء من العمليات تطلبه."

            else:
                response = "أنا معك. هل تريدني أن أسرد لك النواقص بالتفصيل أم نركز على السائقين المتأخرين؟"

            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- الواجهة الرئيسية (نفس التصميم الجميل) ---
st.markdown("<h1 style='text-align: center;'>🏛️ مركز إدارة العمليات والأسطول الذكي</h1>", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
k1.metric("إجمالي الشاحنات", len(st.session_state.df_orders))
k2.metric("في الطريق 🚚", len(st.session_state.df_orders[st.session_state.df_orders['Status'] == 'In-Transit 🚚']))
k3.metric("تأخيرات 🔴", len(st.session_state.df_orders[st.session_state.df_orders['Status'] == 'Delayed 🔴']))
k4.metric("رصيد المخازن", f"{st.session_state.df_inv['Stock_Level'].sum():,}")

st.markdown("---")
tab1, tab2, tab3 = st.tabs(["📋 الرقابة على السائقين", "🔄 مركز المناقلات الذكي", "📊 التحليل الاستراتيجي"])

with tab1:
    st.dataframe(st.session_state.df_orders[['Driver', 'Truck_ID', 'City', 'Status', 'Category']], use_container_width=True)

with tab2:
    st.subheader("إدارة التحويلات بين المستودعات")
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a: f_wh = st.selectbox("من مستودع:", st.session_state.df_inv['Warehouse'].unique())
    with col_b: t_wh = st.selectbox("إلى مستودع:", [w for w in st.session_state.df_inv['Warehouse'].unique() if w != f_wh])
    with col_c: prod = st.selectbox("المنتج:", st.session_state.df_inv['Product'].unique())
    with col_d:
        max_v = st.session_state.df_inv[(st.session_state.df_inv['Warehouse']==f_wh) & (st.session_state.df_inv['Product']==prod)]['Stock_Level'].values[0]
        qty = st.number_input("الكمية:", min_value=1, max_value=int(max_v) if max_v > 0 else 1)
    
    if st.button("تنفيذ التحويل الفوري ⚡"):
        st.session_state.df_inv.loc[(st.session_state.df_inv['Warehouse']==f_wh) & (st.session_state.df_inv['Product']==prod), 'Stock_Level'] -= qty
        st.session_state.df_inv.loc[(st.session_state.df_inv['Warehouse']==to_wh) & (st.session_state.df_inv['Product']==prod), 'Stock_Level'] += qty
        st.success("تم النقل بنجاح.")

with tab3:
    c_left, c_right = st.columns(2)
    with c_left: st.plotly_chart(px.bar(st.session_state.df_inv, x='Product', y='Stock_Level', color='Warehouse', barmode='group'), use_container_width=True)
    with c_right: st.plotly_chart(px.pie(st.session_state.df_orders, names='Status', hole=0.5), use_container_width=True)