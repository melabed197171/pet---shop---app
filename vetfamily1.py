import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pytz

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="VetFamily Alexandria", layout="wide")

# 2. رابط الجدول (تأكد من ضبط الصلاحية لـ Editor)
URL = "https://docs.google.com/spreadsheets/d/1kQ1junWnmyfwKPYj-Jm2QeCLlJ4dwmiMXkystV8dc7k/edit?usp=sharing"

# 3. الربط بجوجل شيت
conn = st.connection("gsheets", type=GSheetsConnection)

def save_data(name, phone, product):
    try:
        existing_data = conn.read(spreadsheet=URL)
        new_row = pd.DataFrame([{
            "التاريخ": datetime.now(pytz.timezone('Africa/Cairo')).strftime("%Y-%m-%d %H:%M"),
            "اسم العميل": name,
            "المنتج": product,
            "رقم الهاتف": phone
        }])
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        conn.update(spreadsheet=URL, data=updated_df)
        return True
    except Exception as e:
        st.error(f"خطأ تقني: {e}")
        return False

# 4. واجهة الموقع
st.title("VetFamily Alexandria")
st.write("مركز الرعاية المتكاملة للحيوانات الاليفة")

st.write("---")
st.subheader("العروض والمنتجات المتاحة")

col1, col2 = st.columns(2)

with col1:
    st.info("رويال كانين قطط 2 كجم - 450 جنيه")
    with st.expander("اضغط هنا لطلب المنتج"):
        n1 = st.text_input("الاسم بالكامل", key="client_n1")
        p1 = st.text_input("رقم الهاتف", key="client_p1")
        if st.button("تاكيد ارسال الطلب", key="submit1"):
            if n1 and p1:
                if save_data(n1, p1, "رويال كانين قطط"):
                    st.success("تم تسجيل طلبك بنجاح")
            else:
                st.warning("برجاء ادخال البيانات المطلوبة")

with col2:
    st.info("رمل قطط كربون 5 لتر - 180 جنيه")
    with st.expander("اضغط هنا لطلب المنتج"):
        n2 = st.text_input("الاسم بالكامل", key="client_n2")
        p2 = st.text_input("رقم الهاتف", key="client_p2")
        if st.button("تاكيد ارسال الطلب", key="submit2"):
            if n2 and p2:
                if save_data(n2, p2, "رمل كربون"):
                    st.success("تم تسجيل طلبك بنجاح")
            else:
                st.warning("برجاء ادخال البيانات المطلوبة")

st.markdown("---")
st.caption("VetFamily Alexandria 2026")
