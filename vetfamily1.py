import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pytz

# 1. إعدادات الصفحة والتصميم (CSS) لضمان ظهور الموقع بشكل احترافي
st.set_page_config(page_title="VetFamily Alexandria", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .main-header {
        background-color: #1e3c72;
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }
    .product-card {
        border: 1px solid #e6e6e6;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        background-color: white;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .price-tag { color: #28a745; font-weight: bold; font-size: 1.2em; }
</style>
""", unsafe_allow_html=True)

# 2. الربط بجدول البيانات (Google Sheets)
URL = "https://docs.google.com/spreadsheets/d/1kQ1junWnmyfwKPYj-Jm2QeCLlJ4dwmiMXkystV8dc7k/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

def save_order(name, phone, product):
    try:
        df = conn.read(spreadsheet=URL)
        new_row = pd.DataFrame([{
            "التاريخ": datetime.now(pytz.timezone('Africa/Cairo')).strftime("%Y-%m-%d %H:%M"),
            "اسم العميل": name,
            "المنتج": product,
            "الهاتف": phone
        }])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(spreadsheet=URL, data=updated_df)
        return True
    except:
        return False

# --- واجهة الموقع ---

# الهيدر الأزرق (كما في التصميم الأصلي 13953.jpg)
st.markdown("""
<div class='main-header'>
    <h1>🐾 VetFamily Alexandria 🐾</h1>
    <p>مركز الرعاية البيطرية المتكاملة - الإسكندرية</p>
</div>
""", unsafe_allow_html=True)

# قسم عروض اليوم الحصرية
st.markdown("### 🔥 عروض اليوم الحصرية")
col_off1, col_off2 = st.columns(2)

with col_off1:
    st.info("📦 رويال كانين قطط 2 كجم - 450 ج.م")
    with st.expander("اضغط هنا لطلب العرض"):
        name_off1 = st.text_input("الاسم", key="off1")
        phone_off1 = st.text_input("الموبايل", key="p_off1")
        if st.button("تأكيد طلب رويال"):
            if name_off1 and phone_off1:
                if save_order(name_off1, phone_off1, "عرض رويال 2ك"): st.success("تم تسجيل طلبك!")

with col_off2:
    st.info("🐱 رمل قطط كربون 5 لتر - 180 ج.م")
    with st.expander("اضغط هنا لطلب العرض"):
        name_off2 = st.text_input("الاسم", key="off2")
        phone_off2 = st.text_input("الموبايل", key="p_off2")
        if st.button("تأكيد طلب الرمل"):
            if name_off2 and phone_off2:
                if save_order(name_off2, phone_off2, "عرض رمل كربون"): st.success("تم تسجيل طلبك!")

st.write("---")

# قسم طعام القطط الجاف (باقي الصفحة 13953.jpg)
st.markdown("### 📦 طعام القطط الجاف")
c1, c2, c3 = st.columns(3)

products = [
    {"name": "بريميوم كات - 1 كجم", "price": "70 ج.م", "id": "p1"},
    {"name": "رويال كيتن - 1.5 كجم", "price": "400 ج.م", "id": "p2"},
    {"name": "رويال بالغ - 2 كجم", "price": "450 ج.م", "id": "p3"}
]

cols = [c1, c2, c3]
for i, p in enumerate(products):
    with cols[i]:
        st.markdown(f"<div class='product-card'><h4>{p['name']}</h4><p class='price-tag'>{p['price']}</p></div>", unsafe_allow_html=True)
        with st.expander(f"حجز {p['name']}"):
            user_name = st.text_input("الاسم", key=f"u_{p['id']}")
            user_phone = st.text_input("الموبايل", key=f"ph_{p['id']}")
            if st.button(f"تأكيد حجز {p['id']}", key=f"btn_{p['id']}"):
                if user_name and user_phone:
                    if save_order(user_name, user_phone, p['name']): st.success("تم الحجز!")

st.write("---")
st.markdown("<p style='text-align: center; color: gray;'>VetFamily Alexandria 2026 ©</p>", unsafe_allow_html=True)
