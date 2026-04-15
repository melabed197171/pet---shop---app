import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pytz

# 1. إعداد الصفحة بشكل عريض وجذاب
st.set_page_config(page_title="VetFamily Alexandria", layout="wide")

# 2. الربط بجدول البيانات
URL = "https://docs.google.com/spreadsheets/d/1kQ1junWnmyfwKPYj-Jm2QeCLlJ4dwmiMXkystV8dc7k/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

def save_order(name, phone, product):
    try:
        # قراءة الشيت الحالي
        df = conn.read(spreadsheet=URL)
        # إضافة السطر الجديد بمطابقة دقيقة لعناوينك (التاريخ، اسم العميل، المنتج، الهاتف)
        new_row = pd.DataFrame([{
            "التاريخ": datetime.now(pytz.timezone('Africa/Cairo')).strftime("%Y-%m-%d %H:%M"),
            "اسم العميل": name,
            "المنتج": product,
            "الهاتف": phone
        }])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(spreadsheet=URL, data=updated_df)
        return True
    except Exception as e:
        st.error(f"فشل الحفظ: {e}")
        return False

# --- تنسيق الواجهة (CSS) ---
st.markdown("""
<style>
    .main-title { text-align: center; color: #1e3c72; font-family: 'Arial'; }
    .section-head { background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin: 20px 0; }
    .product-box { border: 1px solid #ddd; padding: 15px; border-radius: 10px; text-align: center; height: 100%; }
</style>
""", unsafe_allow_html=True)

# 3. رأس الصفحة (الهيدر)
st.markdown("<h1 class='main-title'>VetFamily Alexandria 🐾</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>الرعاية المتكاملة لحيوانك الأليف في الإسكندرية</p>", unsafe_allow_html=True)
st.write("---")

# 4. قسم عروض اليوم (التي تظهر في الجزء العلوي)
st.markdown("<div class='section-head'><h3>🔥 عروض اليوم الحصرية</h3></div>", unsafe_allow_html=True)
col_a, col_b = st.columns(2)

with col_a:
    st.info("رويال كانين بالغ - 2 كجم (450 ج.م)")
    with st.expander("📝 اطلب هذا العرض الآن"):
        n_a = st.text_input("الأسم", key="na")
        p_a = st.text_input("الموبايل", key="pa")
        if st.button("تأكيد حجز العرض 1"):
            if n_a and p_a:
                if save_order(n_a, p_a, "رويال بالغ - عرض"): st.success("تم الحفظ في الجدول!")

with col_b:
    st.info("رمل قطط كربون - 5 لتر (180 ج.م)")
    with st.expander("📝 اطلب هذا العرض الآن"):
        n_b = st.text_input("الأسم", key="nb")
        p_b = st.text_input("الموبايل", key="pb")
        if st.button("تأكيد حجز العرض 2"):
            if n_b and p_b:
                if save_order(n_b, p_b, "رمل كربون - عرض"): st.success("تم الحفظ في الجدول!")

# 5. قسم طعام القطط الجاف (باقي الصفحة)
st.markdown("<div class='section-head'><h3>🐱 طعام القطط الجاف</h3></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='product-box'><h4>بريميوم كات - 1 كجم</h4><p>70 ج.م</p></div>", unsafe_allow_html=True)
    with st.expander("حجز المنتج"):
        un1 = st.text_input("الأسم", key="u1")
        up1 = st.text_input("الموبايل", key="p1")
        if st.button("حجز بريميوم", key="b1"):
            if un1 and up1: save_order(un1, up1, "بريميوم كات")

with col2:
    st.markdown("<div class='product-box'><h4>رويال كيتن - 1.5 كجم</h4><p>400 ج.م</p></div>", unsafe_allow_html=True)
    with st.expander("حجز المنتج"):
        un2 = st.text_input("الأسم", key="u2")
        up2 = st.text_input("الموبايل", key="p2")
        if st.button("حجز كيتن", key="b2"):
            if un2 and up2: save_order(un2, up2, "رويال كيتن")

with col3:
    st.markdown("<div class='product-box'><h4>رويال كانين فيت - 2 كجم</h4><p>450 ج.م</p></div>", unsafe_allow_html=True)
    with st.expander("حجز المنتج"):
        un3 = st.text_input("الأسم", key="u3")
        up3 = st.text_input("الموبايل", key="p3")
        if st.button("حجز رويال فيت", key="b3"):
            if un3 and up3: save_order(un3, up3, "رويال فيت")

st.write("---")
st.caption("VetFamily Alexandria 2026 - جميع الحقوق محفوظة")
