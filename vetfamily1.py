import streamlit as st

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="VetFamily Alexandria", layout="wide")

# 2. تنسيق الواجهة (CSS) لتحسين الشكل
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
    .promo-card {
        border: 2px solid #28a745;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        background-color: #f9fff9;
    }
    .product-card {
        border: 1px solid #e6e6e6;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# 3. رأس الصفحة (الهيدر الأزرق)
st.markdown("""
<div class='main-header'>
    <h1>🐾 VetFamily Alexandria 🐾</h1>
    <p>مركز الرعاية البيطرية المتكاملة - الإسكندرية</p>
</div>
""", unsafe_allow_html=True)

# 4. أزرار التنقل السريع
col_nav1, col_nav2, col_nav3 = st.columns(3)
with col_nav1: st.button("أعجبني ❤️", use_container_width=True)
with col_nav2: st.button("تبني الآن 🏠", use_container_width=True)
with col_nav3: st.button("المدير 👔", use_container_width=True)

st.write("---")

# 5. متجر المستلزمات والطلب عبر الواتساب
st.markdown("<h2 style='text-align: right;'>🛒 متجر المستلزمات البيطرية</h2>", unsafe_allow_html=True)
st.success("✅ اطلب أي منتج عبر الواتساب مباشرة!")

# 6. قسم عروض اليوم الحصرية
st.markdown("<h3 style='text-align: right; color: #d32f2f;'>🔥 عروض اليوم الحصرية</h3>", unsafe_allow_html=True)
c_offer1, c_offer2 = st.columns(2)

with c_offer1:
    st.markdown("""
    <div class='promo_card'>
        <h4>📦 رويال كانين قطط 2 كجم</h4>
        <p style='color: gray; text-decoration: line-through;'>السعر: 550 ج.م</p>
        <p style='color: #28a745; font-size: 1.2em;'><b>السعر الحالي: 450 ج.م</b></p>
    </div>
    """, unsafe_allow_html=True)
    st.link_button("📱 اطلب عبر الواتساب", "https://wa.me/201022395878", use_container_width=True)

with c_offer2:
    st.markdown("""
    <div class='promo_card'>
        <h4>🐱 رمل قطط كربون 5 لتر</h4>
        <p style='color: gray; text-decoration: line-through;'>السعر: 220 ج.م</p>
        <p style='color: #28a745; font-size: 1.2em;'><b>السعر الحالي: 180 ج.م</b></p>
    </div>
    """, unsafe_allow_html=True)
    st.link_button("📱 اطلب عبر الواتساب", "https://wa.me/201022395878", use_container_width=True)

st.write("---")

# 7. قسم طعام القطط الجاف
st.markdown("<h3 style='text-align: right;'>📦 طعام القطط الجاف</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

# قائمة المنتجات
items = [
    {"name": "بريميوم كات - 1 كجم", "price": "70 ج.م", "desc": "نظام محلي عالي الجودة"},
    {"name": "رويال كيتن - 1.5 كجم", "price": "400 ج.م", "desc": "للقطط الصغيرة حتى 12 شهر"},
    {"name": "رويال بالغ - 2 كجم", "price": "450 ج.م", "desc": "طعام متوازن للقطط البالغة"}
]

cols = [col1, col2, col3]
for i, item in enumerate(items):
    with cols[i]:
        st.markdown(f"""
        <div class='product-card'>
            <h4>{item['name']}</h4>
            <p style='font-size: 0.9em; color: #555;'>{item['desc']}</p>
            <p style='color: #28a745; font-weight: bold;'>{item['price']}</p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button(f"اطلب {item['name']}", "https://wa.me/201022395878", use_container_width=True)

st.write("---")
st.markdown("<p style='text-align: center; color: gray;'>VetFamily Alexandria 2026 ©</p>", unsafe_allow_html=True)
