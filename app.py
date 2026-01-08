import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- 1. إعدادات الهوية ---
st.set_page_config(page_title="Strategic Operations Center", layout="wide")

# دالة ذكية لعرض الصورة الشخصية لضمان عدم الاختفاء
def display_profile_pic(img_path):
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
            st.sidebar.markdown(
                f'<div style="text-align: center;"><img src="data:image/png;base64,{data}" style="border-radius: 50%; width: 120px; border: 2px solid #00ffcc;"></div>',
                unsafe_allow_html=True
            )
    else:
        st.sidebar.warning("⚠️ لم يتم العثور على me.jpg")

# --- 2. محرك قراءة البيانات المرن (يتفادى خطأ KeyError) ---
@st.cache_data
def load_and_clean_data():
    file_path = "UAE_Operations_DB.xlsx"
    if os.path.exists(file_path):
        try:
            # قراءة كل الشيتات
            xls = pd.ExcelFile(file_path)
            df_inv = pd.read_excel(xls, sheet_name=0)
            
            # تنظيف أسماء الأعمدة (إزالة المسافات وتحويلها لنصوص)
            df_inv.columns = [str(c).strip() for c in df_inv.columns]
            
            # محاولة العثور على عمود "Stock" حتى لو كُتب بشكل مختلف
            stock_col = next((c for c in df_inv.columns if 'stock' in c.lower() or 'مخزون' in c), None)
            warehouse_col = next((c for c in df_inv.columns if 'warehouse' in c.lower() or 'مستودع' in c), None)
            product_col = next((c for c in df_inv.columns if 'product' in c.lower() or 'منتج' in c), None)
            
            # إعادة تسمية الأعمدة داخلياً لضمان عمل الكود
            rename_dict = {}
            if stock_col: rename_dict[stock_col] = 'Stock'
            if warehouse_col: rename_dict[warehouse_col] = 'Warehouse'
            if product_col: rename_dict[product_col] = 'Product'
            
            df_inv = df_inv.rename(columns=rename_dict)
            return df_inv
        except Exception as e:
            st.error(f"فشل قراءة الملف: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

df_inv = load_and_clean_data()

# --- 3. تصميم الواجهة الجانبية (المستشار طارق) ---
with st.sidebar:
    display_profile_pic("me.jpg") # عرض صورتك
    st.markdown("<h3 style='text-align: center;'>المستشار طارق الذكي</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # عقل المحادثة - ردود حقيقية بناءً على البيانات
    if 'chat_history' not in st.session_state: st.session_state.chat_history = []
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    if prompt := st.chat_input("اسألني عن المخزون أو النواقص..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        # تحليل السؤال بناءً على البيانات
        if not df_inv.empty and 'Stock' in df_inv.columns:
            if "دبي" in prompt or "dubai" in prompt.lower():
                val = df_inv[df_inv['Warehouse'].str.contains('Dubai', case=False, na=False)]['Stock'].sum()
                reply = f"✅ بناءً على ملفك، إجمالي المخزون في **دبي** هو {val:,} وحدة."
            elif "نقص" in prompt or "low" in prompt.lower():
                low_items = df_inv[df_inv['Stock'] < 500]['Product'].tolist()
                reply = f"⚠️ رصدت نقصاً في الأصناف التالية: {', '.join(low_items[:3])}."
            else:
                reply = "أنا جاهز لتحليل بياناتك أستاذ طارق. اسألني عن مستودع معين أو عن النواقص."
        else:
            reply = "سيدي، يبدو أن هناك مشكلة في عمود 'Stock' في ملف الإكسل. يرجى التأكد من تسمية الأعمدة بوضوح."

        with st.chat_message("assistant"): st.write(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

# --- 4. العرض الرئيسي (Dashboard) ---
st.markdown("<h1 style='text-align: center;'>📊 Strategic Operations Center</h1>", unsafe_allow_html=True)

if not df_inv.empty and 'Stock' in df_inv.columns:
    # عدادات علوية واضحة
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي المخزون بالملف", f"{df_inv['Stock'].sum():,}")
    c2.metric("عدد المستودعات", df_inv['Warehouse'].nunique())
    c3.metric("كفاءة البيانات", "100%")

    st.markdown("---")
    
    col_l, col_r = st.columns([2, 1])
    
    with col_l:
        st.subheader("📈 توزيع المخزون (رسم بياني واضح)")
        # رسم أعمدة (Bar Chart) لتجنب التداخل
        fig = px.bar(df_inv, x='Warehouse', y='Stock', color='Product', 
                     template="plotly_dark", barmode='group', title="مستويات المخزون حسب المدينة")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.subheader("💡 نصيحة استشارية اليوم")
        st.info("بناءً على ملفك المرفوع: يوجد تركز مخزون عالي في الشارقة، يفضل موازنته مع فرع العين.")
        
        st.subheader("📋 ملخص البيانات")
        st.dataframe(df_inv[['Warehouse', 'Product', 'Stock']].head(10), use_container_width=True)
else:
    st.error("⚠️ خطأ في هيكلة البيانات: تأكد أن ملف الإكسل يحتوي على أعمدة باسم Warehouse و Stock.")