import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pytz

# 1. إعدادات الصفحة
st.set_page_config(page_title="VetFamily Alexandria", layout="wide")

# 2. رابط الجدول
URL = "https://docs.google.com/spreadsheets/d/1kQ1junWnmyfwKPYj-Jm2QeCLlJ4dwmiMXkystV8dc7k/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# دالة حفظ البيانات
def save_order(name, phone, product):
    try:
        df = conn.read(spreadsheet=URL)
        new_row = pd.DataFrame([{
            "التاريخ": datetime.now(pytz.timezone('Africa/Cairo')).strftime("%Y-%m-%d %H:%M"),
            "اسم العميل": name,
            "المنتج": product,
            "رقم الهاتف": phone
        }])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(spreadsheet=URL, data=updated_df)
        return True
    except Exception as e:
        st.error(f"خطأ في الحفظ: {e}")
        return False

# 3. واجهة الموقع (نصوص فقط لضمان الاستقرار)
st.markdown("<h1 style='text-align: center; color: #1e3c72;'>VetFamily Alexandria</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>مركز الرعاية المتكاملة للحيوانات الأليفة</p>", unsafe_allow_html=True)
st.write("---")

# 4. عروض اليوم الحصرية
st.subheader("عروض اليوم الحصرية")
c1, c2 = st.columns(2)

with c1:
    st.info("رويال كانين قطط 2 كجم - 450 ج.م")
    with st.expander("اطلب الان"):
        n1 = st.text_input("الاسم", key="n_r2")
        p1 = st.text_input("الموبايل", key="p_r2")
        if st.button("تأكيد طلب رويال 2 كجم"):
            if n1 and p1:
                if save_order(n1, p1, "رويال كانين 2 كجم"): st.success("تم تسجيل طلبك")

with c2:
    st.info("رمل قطط كربون 5 لتر - 180 ج.م")
    with st.expander("اطلب الان"):
        n2 = st.text_input("الاسم", key="n_s5")
        p2 = st.text_input("الموبايل", key="p_s5")
        if st.button("تأكيد طلب الرمل"):
            if n2 and p2:
                if save_order(n2, p2, "رمل كربون"): st.success("تم تسجيل طلبك")

st.write("---")

# 5. طعام القطط الجاف
st.subheader("طعام القطط الجاف")
col1, col2, col3 = st.columns(3)

with col1:
    st.write("### بريميوم كات - 1 كجم")
    st.write("**السعر: 70 ج.م**")
    with st.expander("حجز المنتج"):
        un1 = st.text_input("الاسم", key="u_p1")
        up1 = st.text_input("الموبايل", key="ph_p1")
        if st.button("طلب بريميوم كات"):
            if un1 and up1:
                if save_order(un1, up1, "بريميوم كات"): st.success("تم الحجز")

with col2:
    st.write("### رويال كانين كيتن - 1.5 كجم")
    st.write("**السعر: 400 ج.م**")
    with st.expander("حجز المنتج"):
        un2 = st.text_input("الاسم", key="u_rk")
        up2 = st.text_input("الموبايل", key="ph_rk")
        if st.button("طلب رويال كيتن"):
            if un2 and up2:
                if save_order(un2, up2, "رويال كيتن"): st.success("تم الحجز")

with col3:
    st.write("### رويال كانين بالغ - 2 كجم")
    st.write("**السعر: 450 ج.م**")
    with st.expander("حجز المنتج"):
        un3 = st.text_input("الاسم", key="u_ra")
        up3 = st.text_input("الموبايل", key="ph_ra")
        if st.button("طلب رويال بالغ"):
            if un3 and up3:
                if save_order(un3, up3, "رويال بالغ"): st.success("تم الحجز")
