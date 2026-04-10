import streamlit as st
from PIL import Image
from datetime import datetime, timedelta
import pytz
import io
import csv
import hashlib

# إعداد الصفحة
st.set_page_config(page_title="pet care", layout="wide", page_icon="🐾")

# تحديد منطقة القاهرة الزمنية
CAIRO_TZ = pytz.timezone('Africa/Cairo')

def get_cairo_time():
    return datetime.now(CAIRO_TZ)

# CSS الكامل
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');

    * {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }

    [data-testid="stAppViewContainer"] {
        direction: rtl !important;
        text-align: right !important;
        background: linear-gradient(135deg, #a1ebdb 0%, #ffdca2 100%);
        background-attachment: fixed;
    }

    .block-container {
        padding: 3rem 2.5rem;
        max-width: 1200px;
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-top: 30px;
        margin-bottom: 30px;
    }

    .stImage img {
        border-radius: 50%; 
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); 
        border: 4px solid #ffffff;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #1a365d !important;
        font-weight: 800 !important;
        text-align: right !important;
        direction: rtl !important;
    }

    div.stButton > button {
        width: 100%;
        height: 55px;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border-radius: 14px;
        background: linear-gradient(45deg, #10b981, #059669);
        color: white !important;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(5, 150, 105, 0.2);
    }
    
    input, textarea, select {
        direction: rtl !important;
        text-align: right !important;
    }
    
    .price-tag {
        font-size: 24px;
        color: #2e7d32;
        font-weight: bold;
    }
    
    .notification-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }

    .subscription-card {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        border-right: 6px solid #10b981;
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }
    
    .thank-you-message {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    .adoption-form {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        border-right: 6px solid #ff9800;
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }
    
    .adoption-section {
        background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);
        padding: 30px;
        border-radius: 20px;
        margin: 30px 0;
        border: 3px solid #e91e63;
        box-shadow: 0 10px 30px rgba(233, 30, 99, 0.2);
    }
    
    /* ✅ تصميم عروض اليوم */
    .offers-header {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 20px;
        border-radius: 20px 20px 0 0;
        text-align: center;
        margin-bottom: 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255, 107, 107, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0); }
    }
    
    .offer-card {
        background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px;
        border: 2px solid #ff6b6b;
        box-shadow: 0 8px 20px rgba(255, 107, 107, 0.2);
        transition: transform 0.3s ease;
        text-align: center;
    }
    
    .offer-card:hover {
        transform: scale(1.03);
    }
    
    .old-price {
        color: #999;
        text-decoration: line-through;
        font-size: 18px;
    }
    
    .new-price {
        color: #e74c3c;
        font-size: 28px;
        font-weight: bold;
    }
    
    .discount-badge {
        background: #e74c3c;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 5px;
    }
    
    .timer-box {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: #fff;
        padding: 10px 20px;
        border-radius: 10px;
        display: inline-block;
        margin: 10px 0;
    }
    
    .offers-container {
        background: linear-gradient(135deg, #fff5f5 0%, #ffe0e0 100%);
        border-radius: 0 0 20px 20px;
        padding: 20px;
        border: 2px solid #ff6b6b;
        border-top: none;
        margin-top: 0;
    }
</style>
""", unsafe_allow_html=True)

# دالة تشفير
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hash_password("admin123")

def check_login(username, password):
    return username == ADMIN_USERNAME and hash_password(password) == ADMIN_PASSWORD_HASH

if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

if 'show_adoption_form' not in st.session_state:
    st.session_state.show_adoption_form = False

if 'adoption_requests' not in st.session_state:
    st.session_state.adoption_requests = []

# ✅ إضافة عروض اليوم
if 'daily_offers' not in st.session_state:
    st.session_state.daily_offers = [
        {
            "id": 1,
            "name": "باقة الفحص الشامل",
            "description": "فحص طبي كامل + تحاليل + استشارة",
            "old_price": 800,
            "new_price": 499,
            "discount": 38,
            "icon": "🩺",
            "limited": True,
            "quantity": 10
        },
        {
            "id": 2,
            "name": "طعام بريميوم شهر كامل",
            "description": "طعام صحي عالي الجودة لمدة شهر",
            "old_price": 600,
            "new_price": 399,
            "discount": 33,
            "icon": "🍖",
            "limited": True,
            "quantity": 15
        },
        {
            "id": 3,
            "name": "جهاز تتبع GPS",
            "description": "جهاز تتبع ذكي + تركيب مجاني",
            "old_price": 2000,
            "new_price": 1499,
            "discount": 25,
            "icon": "📍",
            "limited": True,
            "quantity": 5
        },
        {
            "id": 4,
            "name": "باقة التطعيمات الأساسية",
            "description": "جميع التطعيمات الضرورية",
            "old_price": 500,
            "new_price": 299,
            "discount": 40,
            "icon": "💉",
            "limited": False,
            "quantity": 50
        }
    ]

if 'offer_orders' not in st.session_state:
    st.session_state.offer_orders = []

# تهيئة البيانات
if 'packages' not in st.session_state:
    st.session_state.packages = {
        "الباقة الماسية": {
            "price": 5000,
            "description": "رعاية شاملة + جهاز تتبع + نظام غذائي",
            "icon": "💎",
            "features": [
                "زيارات منزلية غير محدودة",
                "جهاز تتبع GPS متطور",
                "نظام غذائي مخصص",
                "استشارات على مدار الساعة",
                "تطعيمات شاملة"
            ]
        },
        "الباقة الذهبية": {
            "price": 2500,
            "description": "4 استشارات شهرياً + اللقاحات الأساسية",
            "icon": "✨",
            "features": [
                "4 استشارات شهرياً",
                "اللقاحات الأساسية",
                "فحص دوري شهري",
                "خصم 20% على الخدمات الإضافية"
            ]
        },
        "الباقة الاقتصادية": {
            "price": 1000,
            "description": "استشارة شهرية + جدول تطعيمات",
            "icon": "🛡️",
            "features": [
                "استشارة شهرية واحدة",
                "جدول تطعيمات سنوي",
                "خصم 10% على الخدمات الإضافية"
            ]
        }
    }

if 'subscriptions' not in st.session_state:
    st.session_state.subscriptions = []

if 'package_notifications' not in st.session_state:
    st.session_state.package_notifications = []

if 'shopping_cart' not in st.session_state:
    st.session_state.shopping_cart = []

# ✅ دالة حفظ طلب العرض
def save_offer_order(offer, customer_info):
    try:
        cairo_time = get_cairo_time()
        order = {
            "id": len(st.session_state.offer_orders) + 1,
            "offer_name": offer["name"],
            "offer_price": offer["new_price"],
            "original_price": offer["old_price"],
            "discount": offer["discount"],
            "customer_name": customer_info["name"],
            "customer_phone": customer_info["phone"],
            "date": cairo_time.strftime("%Y-%m-%d"),
            "time": cairo_time.strftime("%H:%M:%S"),
            "status": "جديد"
        }
        
        st.session_state.offer_orders.append(order)
        
        notification = {
            "message": f"طلب عرض جديد: {offer['name']}",
            "timestamp": cairo_time.strftime("%H:%M:%S"),
            "date": cairo_time.strftime("%Y-%m-%d"),
            "details": order,
            "type": "offer"
        }
        st.session_state.package_notifications.insert(0, notification)
        
        return True
    except Exception as e:
        st.error(f"خطأ: {e}")
        return False

# دالة حفظ طلب التبني
def save_adoption_request(adoption_info):
    try:
        cairo_time = get_cairo_time()
        request = {
            "id": len(st.session_state.adoption_requests) + 1,
            "customer_name": str(adoption_info["name"]),
            "customer_phone": str(adoption_info["phone"]),
            "customer_address": str(adoption_info.get("address", "")),
            "pet_type": str(adoption_info["pet_type"]),
            "pet_age": str(adoption_info.get("pet_age", "")),
            "notes": str(adoption_info.get("notes", "")),
            "date": cairo_time.strftime("%Y-%m-%d"),
            "time": cairo_time.strftime("%H:%M:%S"),
            "status": "جديد - في انتظار التواصل"
        }
        
        st.session_state.adoption_requests.append(request)
        
        notification = {
            "message": f"طلب تبني جديد من {adoption_info['name']}",
            "timestamp": cairo_time.strftime("%H:%M:%S"),
            "date": cairo_time.strftime("%Y-%m-%d"),
            "details": request,
            "type": "adoption"
        }
        st.session_state.package_notifications.insert(0, notification)
        
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ طلب التبني: {e}")
        return False

# دالة حفظ الاشتراك
def save_subscription(package_name, package_price, customer_info):
    try:
        cairo_time = get_cairo_time()
        subscription = {
            "id": len(st.session_state.subscriptions) + 1,
            "package_name": str(package_name),
            "price": int(package_price),
            "date": cairo_time.strftime("%Y-%m-%d"),
            "time": cairo_time.strftime("%H:%M:%S"),
            "customer_name": str(customer_info["name"]),
            "customer_phone": str(customer_info["phone"]),
            "status": "جديد - في انتظار التواصل"
        }
        
        st.session_state.subscriptions.append(subscription)
        
        notification = {
            "message": f"اشتراك جديد في {package_name}",
            "timestamp": cairo_time.strftime("%H:%M:%S"),
            "date": cairo_time.strftime("%Y-%m-%d"),
            "details": subscription,
            "type": "subscription"
        }
        st.session_state.package_notifications.insert(0, notification)
        
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ الاشتراك: {e}")
        return False

# ============================================
# الهيدر
# ============================================
col_text, col_img = st.columns([5, 1]) 

with col_text:
    st.markdown("<h1>pet care🐾</h1>", unsafe_allow_html=True)

with col_img:
    try:
        image = Image.open('cat.png')
        st.image(image, width=300) 
    except:
        pass

st.markdown("---")

# أزرار أعجبني وتبني الآن
col1, col2 = st.columns(2)
with col1:
    if st.button("أعجبني ❤️"):
        st.balloons()
        st.success("شكراً على حبك للأليف 🐱")

with col2:
    if st.button("تبني الآن 🏠"):
        st.session_state.show_adoption_form = True
        st.info("⬇️ انزل لأسفل الصفحة لملء نموذج التبني")

st.write("# مركز الرعاية المتكاملة البيطرية 🐾")
st.write("## تحت اشراف نخبة من الأطباء والمهندسين")

# ============================================
# ✅ قسم عروض اليوم - بعد العنوان مباشرة
# ============================================
st.markdown("---")

# حساب الوقت المتبقي للعرض (نهاية اليوم)
cairo_now = get_cairo_time()
end_of_day = cairo_now.replace(hour=23, minute=59, second=59)
time_remaining = end_of_day - cairo_now
hours_remaining = int(time_remaining.total_seconds() // 3600)
minutes_remaining = int((time_remaining.total_seconds() % 3600) // 60)

# هيدر العروض
st.markdown(f"""
<div class='offers-header'>
    <h2 style='color: white; margin: 0;'>🔥 عروض اليوم الحصرية 🔥</h2>
    <p style='margin: 10px 0 0 0; font-size: 18px;'>⏰ ينتهي العرض خلال: {hours_remaining} ساعة و {minutes_remaining} دقيقة</p>
    <p style='margin: 5px 0 0 0;'>📅 {cairo_now.strftime('%Y-%m-%d')}</p>
</div>
""", unsafe_allow_html=True)

# عرض البطاقات
st.markdown("<div class='offers-container'>", unsafe_allow_html=True)

# عرض العروض في صفوف
cols = st.columns(4)

for idx, offer in enumerate(st.session_state.daily_offers):
    with cols[idx % 4]:
        st.markdown(f"""
        <div class='offer-card'>
            <h1 style='font-size: 50px; margin: 0;'>{offer['icon']}</h1>
            <h4 style='color: #333; margin: 10px 0;'>{offer['name']}</h4>
            <p style='color: #666; font-size: 14px;'>{offer['description']}</p>
            <span class='discount-badge'>خصم {offer['discount']}%</span>
            <p class='old-price'>{offer['old_price']} ج.م</p>
            <p class='new-price'>{offer['new_price']} ج.م</p>
            <p style='color: #e74c3c; font-size: 12px;'>{'⚡ كمية محدودة: ' + str(offer['quantity']) + ' فقط' if offer['limited'] else '✅ متاح'}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# نموذج طلب العرض
st.markdown("### 🛒 اطلب عرضك الآن")

col_offer, col_name, col_phone = st.columns([2, 2, 2])

with col_offer:
    offer_names = [f"{o['icon']} {o['name']} - {o['new_price']} ج.م (خصم {o['discount']}%)" for o in st.session_state.daily_offers]
    selected_offer_name = st.selectbox("اختر العرض:", offer_names, key="selected_offer")

with col_name:
    offer_customer_name = st.text_input("الاسم:", placeholder="أدخل اسمك", key="offer_name")

with col_phone:
    offer_customer_phone = st.text_input("رقم الواتساب:", placeholder="01xxxxxxxxx", key="offer_phone")

if st.button("🎁 احجز العرض الآن", key="book_offer", use_container_width=True):
    if offer_customer_name.strip() and offer_customer_phone.strip():
        # الحصول على العرض المختار
        selected_idx = offer_names.index(selected_offer_name)
        selected_offer = st.session_state.daily_offers[selected_idx]
        
        customer_info = {
            "name": offer_customer_name.strip(),
            "phone": offer_customer_phone.strip()
        }
        
        if save_offer_order(selected_offer, customer_info):
            st.markdown(f"""
            <div class='thank-you-message'>
                🎉 تم حجز العرض بنجاح! 🎉<br>
                {selected_offer['icon']} {selected_offer['name']}<br>
                💰 السعر: {selected_offer['new_price']} ج.م بدلاً من {selected_offer['old_price']} ج.م<br>
                📞 سيتم التواصل معك قريباً
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
            st.rerun()
    else:
        st.error("⚠️ برجاء إدخال الاسم ورقم الهاتف")

st.markdown("---")

# ============================================
# التبويبات
# ============================================
if st.session_state.is_logged_in:
    tabs = st.tabs([
        "الباقات المتاحة 💳",
        "الاستشارات واللقاحات",
        "المتجر والمستلزمات 🛒",
        "التكنولوجيا والأجهزة",
        "لوحة التحكم 📊",
        "إدارة الباقات ⚙️",
        "طلبات التبني 🏠",
        "طلبات العروض 🎁"  # ✅ تبويب جديد
    ])
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = tabs
else:
    tabs = st.tabs([
        "الباقات المتاحة 💳",
        "الاستشارات واللقاحات",
        "المتجر والمستلزمات 🛒",
        "التكنولوجيا والأجهزة"
    ])
    tab1, tab2, tab3, tab4 = tabs

# تبويب الباقات
with tab1:
    st.write("## اختر باقتك المفضلة 💳")
    
    for idx, (package_name, package_data) in enumerate(st.session_state.packages.items()):
        st.markdown("---")
        
        st.write(f"## {package_name} {package_data['icon']}")
        st.write(f"**{package_data['description']}**")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("### التفاصيل:")
            for feature in package_data['features']:
                st.write(f"✓ {feature}")
        
        with col2:
            st.markdown(f"<p class='price-tag'>{package_data['price']} ج.م / سنة</p>", unsafe_allow_html=True)
        
        st.write("### بيانات التفعيل 📝")
        
        col_name, col_phone = st.columns(2)
        
        with col_name:
            customer_name = st.text_input(
                "الاسم الكامل",
                key=f"name_{package_name}_{idx}",
                placeholder="أدخل اسمك الكامل",
                label_visibility="collapsed"
            )
            st.caption("الاسم الكامل")
        
        with col_phone:
            customer_phone = st.text_input(
                "رقم الواتساب",
                key=f"phone_{package_name}_{idx}",
                placeholder="01xxxxxxxxx",
                label_visibility="collapsed"
            )
            st.caption("رقم الواتساب")
        
        if st.button(f"تفعيل {package_name} ✅", key=f"btn_{package_name}_{idx}"):
            if customer_name.strip() and customer_phone.strip():
                customer_info = {
                    "name": customer_name.strip(),
                    "phone": customer_phone.strip()
                }
                
                if save_subscription(package_name, package_data['price'], customer_info):
                    st.markdown("""
                    <div class='thank-you-message'>
                        ✅ شكراً لك! 🎉<br>
                        سيتم تنفيذ الطلب والتواصل للتوصيل 📞
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.balloons()
                    st.rerun()
            else:
                st.error("برجاء إدخال الاسم ورقم الهاتف ⚠️")

# تبويب الاستشارات
with tab2:
    st.write("## الخدمات الطبية والوقائية 🩺")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### الأدوية واللقاحات")
        st.info("نوفر أحدث اللقاحات الدورية والبروتوكولات العلاجية المعتمدة")
    with col2:
        st.write("### إرشادات طبية")
        st.write("- جدول التطعيمات السنوي")
        st.write("- الإسعافات الأولية للحيوانات الأليفة")

# تبويب المتجر
with tab3:
    st.write("## متجر المستلزمات 🛒")

# تبويب التكنولوجيا
with tab4:
    st.write("## الحلول التقنية ⚙️")

# لوحة التحكم - للمدير فقط
if st.session_state.is_logged_in:
    with tab5:
        st.write("## لوحة التحكم 📊")
        
        cairo_now = get_cairo_time()
        st.info(f"الوقت الحالي: {cairo_now.strftime('%Y-%m-%d %H:%M:%S')} 🕐")
        
        if st.button("تسجيل الخروج 🔓"):
            st.session_state.is_logged_in = False
            st.rerun()
        
        # الإحصائيات
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("الاشتراكات 📦", len(st.session_state.subscriptions))
        with col2:
            total_revenue = sum(sub["price"] for sub in st.session_state.subscriptions)
            st.metric("الإيرادات 💰", f"{total_revenue:,} ج.م")
        with col3:
            st.metric("طلبات التبني 🏠", len(st.session_state.adoption_requests))
        with col4:
            st.metric("طلبات العروض 🎁", len(st.session_state.offer_orders))
        with col5:
            st.metric("الإشعارات 🔔", len(st.session_state.package_notifications))
        
        st.markdown("---")
        st.write("### الإشعارات الفورية 🔔")
        
        if st.session_state.package_notifications:
            for notif in st.session_state.package_notifications[:10]:  # آخر 10 إشعارات
                notif_type = notif.get('type', 'subscription')
                
                if notif_type == 'offer':
                    st.markdown(f"""
                    <div class='notification-box' style='background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);'>
                        <h4>🎁 {notif['message']}</h4>
                        <p>📅 {notif['date']} | ⏰ {notif['timestamp']}</p>
                        <p>👤 {notif['details']['customer_name']} | 📞 {notif['details']['customer_phone']}</p>
                        <p>💰 {notif['details']['offer_price']} ج.م</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif notif_type == 'adoption':
                    st.markdown(f"""
                    <div class='notification-box' style='background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);'>
                        <h4>🏠 {notif['message']}</h4>
                        <p>📅 {notif['date']} | ⏰ {notif['timestamp']}</p>
                        <p>👤 {notif['details']['customer_name']} | 📞 {notif['details']['customer_phone']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='notification-box'>
                        <h4>🔔 {notif['message']}</h4>
                        <p>📅 {notif['date']} | ⏰ {notif['timestamp']}</p>
                        <p>👤 {notif['details']['customer_name']} | 📞 {notif['details']['customer_phone']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("لا توجد إشعارات")

    with tab6:
        st.write("## إدارة الباقات ⚙️")

    with tab7:
        st.write("## طلبات التبني 🏠")
        
        if st.session_state.adoption_requests:
            for req in reversed(st.session_state.adoption_requests):
                st.markdown(f"""
                <div class='adoption-form'>
                    <h4>طلب #{req['id']} - {req['customer_name']}</h4>
                </div>
                """, unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"📞 {req['customer_phone']}")
                    st.write(f"🐾 {req['pet_type']}")
                with col2:
                    st.write(f"📅 {req['date']}")
                    st.write(f"⏰ {req['time']}")
                st.markdown("---")
        else:
            st.warning("لا توجد طلبات تبني")

    # ✅ تبويب طلبات العروض الجديد
    with tab8:
        st.write("## طلبات العروض 🎁")
        
        total_offer_revenue = sum(order["offer_price"] for order in st.session_state.offer_orders)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("عدد الطلبات", len(st.session_state.offer_orders))
        with col2:
            st.metric("إجمالي المبيعات", f"{total_offer_revenue:,} ج.م")
        
        st.markdown("---")
        
        if st.session_state.offer_orders:
            for order in reversed(st.session_state.offer_orders):
                st.markdown(f"""
                <div class='offer-card' style='text-align: right;'>
                    <h4>🎁 طلب #{order['id']} - {order['offer_name']}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"👤 **الاسم:** {order['customer_name']}")
                    st.write(f"📞 **الهاتف:** {order['customer_phone']}")
                with col2:
                    st.write(f"💰 **السعر:** {order['offer_price']} ج.م")
                    st.write(f"📉 **الخصم:** {order['discount']}%")
                with col3:
                    st.write(f"📅 **التاريخ:** {order['date']}")
                    st.write(f"⏰ **الوقت:** {order['time']}")
                
                status_options = ["جديد", "تم التواصل", "تم التوصيل", "ملغي"]
                current_status = order.get('status', 'جديد')
                
                col_s, col_b = st.columns([4, 1])
                with col_s:
                    new_status = st.selectbox("الحالة:", status_options,
                        index=status_options.index(current_status) if current_status in status_options else 0,
                        key=f"offer_status_{order['id']}")
                with col_b:
                    if st.button("حفظ", key=f"offer_save_{order['id']}"):
                        for o in st.session_state.offer_orders:
                            if o['id'] == order['id']:
                                o['status'] = new_status
                        st.success("✅")
                        st.rerun()
                
                st.markdown("---")
        else:
            st.warning("لا توجد طلبات عروض")

# ============================================
# قسم التبني في آخر الصفحة
# ============================================
st.markdown("---")
st.markdown("---")

if st.session_state.show_adoption_form:
    st.markdown("""
    <div class='adoption-section'>
        <h2 style='color: #c2185b; text-align: center;'>🏠 نموذج طلب التبني 🐾</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("adoption_form"):
        st.write("### 👤 بياناتك الشخصية")
        
        col_name, col_phone = st.columns(2)
        with col_name:
            adopt_name = st.text_input("الاسم الكامل *", placeholder="أدخل اسمك", key="adopt_name")
        with col_phone:
            adopt_phone = st.text_input("رقم الواتساب *", placeholder="01xxxxxxxxx", key="adopt_phone")
        
        adopt_address = st.text_input("العنوان", placeholder="أدخل عنوانك", key="adopt_address")
        
        st.write("### 🐾 بيانات الحيوان")
        
        col_pet, col_age = st.columns(2)
        with col_pet:
            pet_type = st.selectbox("نوع الحيوان *", 
                ["قطة 🐱", "كلب 🐕", "طائر 🐦", "أرنب 🐰", "سلحفاة 🐢", "أخرى"], key="pet_type")
        with col_age:
            pet_age = st.selectbox("العمر المفضل",
                ["صغير (أقل من سنة)", "متوسط (1-3 سنوات)", "كبير (أكثر من 3 سنوات)", "لا يهم"], key="pet_age")
        
        adopt_notes = st.text_area("ملاحظات", placeholder="أي متطلبات خاصة؟", key="adopt_notes")
        
        col_submit, col_cancel = st.columns(2)
        with col_submit:
            submitted = st.form_submit_button("إرسال الطلب 🐾✅", use_container_width=True)
        with col_cancel:
            cancelled = st.form_submit_button("إلغاء ❌", use_container_width=True)
        
        if submitted:
            if adopt_name.strip() and adopt_phone.strip():
                adoption_info = {
                    "name": adopt_name.strip(),
                    "phone": adopt_phone.strip(),
                    "address": adopt_address.strip(),
                    "pet_type": pet_type,
                    "pet_age": pet_age,
                    "notes": adopt_notes.strip()
                }
                
                if save_adoption_request(adoption_info):
                    st.markdown("""
                    <div class='thank-you-message'>
                        ✅ تم إرسال طلب التبني بنجاح! 🎉🐾<br>
                        سيتم التواصل معك قريباً 📞
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                    st.session_state.show_adoption_form = False
                    st.rerun()
            else:
                st.error("⚠️ برجاء إدخال الاسم ورقم الهاتف")
        
        if cancelled:
            st.session_state.show_adoption_form = False
            st.rerun()
else:
    st.markdown("""
    <div style='text-align: center; padding: 30px;'>
        <h3>🏠 هل تريد تبني حيوان أليف؟</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📝 املأ نموذج التبني 🐾", key="open_adoption_bottom", use_container_width=True):
        st.session_state.show_adoption_form = True
        st.rerun()

# ============================================
# الشريط الجانبي
# ============================================
st.sidebar.write("# فريق العمل 👨‍⚕️")
st.sidebar.markdown("""
* **الفريق الطبي:** استشارات وأدوية
* **سلامة الغذاء:** طعام صحي
* **الهندسة الطبية:** أجهزة تتبع
---
📞 **للدعم:** 00000
""")

st.sidebar.markdown("---")

if not st.session_state.is_logged_in:
    st.sidebar.write("### تسجيل دخول المدير 🔐")
    with st.sidebar.form("login_form"):
        username = st.text_input("اسم المستخدم", label_visibility="collapsed", placeholder="admin")
        password = st.text_input("كلمة المرور", type="password", label_visibility="collapsed", placeholder="admin123")
        
        if st.form_submit_button("دخول 🔓"):
            if check_login(username, password):
                st.session_state.is_logged_in = True
                st.success("تم الدخول ✅")
                st.rerun()
            else:
                st.error("خطأ ❌")
else:
    st.sidebar.success("مسجل دخول كمدير ✅")
    cairo_now = get_cairo_time()
    st.sidebar.info(f"🕐 {cairo_now.strftime('%H:%M')}")
    st.sidebar.metric("الاشتراكات", len(st.session_state.subscriptions))
    st.sidebar.metric("طلبات العروض 🎁", len(st.session_state.offer_orders))
    st.sidebar.metric("طلبات التبني 🏠", len(st.session_state.adoption_requests))