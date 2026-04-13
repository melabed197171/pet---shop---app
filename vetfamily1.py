import streamlit as st
from datetime import datetime, timedelta
import pytz
import hashlib
import urllib.parse

st.set_page_config(
    page_title="VetFamily Alexandria - مركز الرعاية البيطرية",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    [data-testid="stSidebar"]        { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    .block-container {
        max-width: 100% !important;
        padding: 1rem 1.5rem !important;
        direction: rtl !important;
    }
    * { box-sizing: border-box; }
    body, .stMarkdown, [data-testid="stAppViewContainer"] {
        direction: rtl !important;
        text-align: right !important;
    }

    /* ===== هيدر ===== */
    .main-header {
        background: linear-gradient(135deg,#1e3c72,#2a5298);
        padding: 30px 20px; border-radius: 20px;
        color: white; text-align: center; margin-bottom: 20px;
    }
    .main-header h1 {
        font-size: clamp(1.8rem,5vw,3rem) !important;
        color: white !important; font-weight: 900 !important; margin: 0 !important;
    }
    .main-header p { color: rgba(255,255,255,0.9) !important; margin: 8px 0 0 !important; }

    /* ===== بطاقة المنتج ===== */
    .product-card {
        background: white; border-radius: 18px; padding: 20px;
        margin: 10px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0; text-align: center;
        transition: transform 0.2s ease;
    }
    .product-card:hover { transform: translateY(-3px); }
    .product-image  { font-size: 3.5rem !important; margin: 5px 0 !important; }
    .product-name   {
        font-size: 1.5rem !important; font-weight: 900 !important;
        color: #1e3c72 !important; margin: 10px 0 8px !important; line-height: 1.3 !important;
    }
    .product-description {
        font-size: 0.9rem !important; color: #718096 !important;
        font-weight: 500 !important; margin: 6px 0 !important;
    }
    .product-price {
        font-size: 1.5rem !important; font-weight: 900 !important;
        color: #28a745 !important; margin: 10px 0 !important;
    }
    .product-badge {
        display: inline-block; padding: 3px 12px; border-radius: 20px;
        font-size: 0.75rem; font-weight: 700; margin: 2px; color: white;
    }
    .badge-new     { background: linear-gradient(135deg,#11998e,#38ef7d); }
    .badge-sale    { background: linear-gradient(135deg,#ff416c,#ff4b2b); }
    .badge-popular { background: linear-gradient(135deg,#667eea,#764ba2); }
    .stock-badge {
        padding: 5px 10px; border-radius: 8px; font-size: 0.8rem;
        font-weight: 700; margin-top: 8px; display: inline-block;
    }
    .in-stock  { background:#d4edda; color:#155724; }
    .low-stock { background:#fff3cd; color:#856404; }
    .out-stock { background:#f8d7da; color:#721c24; }

    /* ===== رسالة الإضافة تحت الزر مباشرة ===== */
    .add-confirm-inline {
        background: linear-gradient(135deg,#f0fff4,#e8f5e9);
        border: 2px solid #28a745;
        border-radius: 14px;
        padding: 14px 16px;
        margin-top: 10px;
        text-align: center;
        animation: popIn 0.3s ease;
    }
    @keyframes popIn {
        0%   { opacity:0; transform:scale(0.95) translateY(-5px); }
        100% { opacity:1; transform:scale(1)    translateY(0);     }
    }
    .add-confirm-icon    { font-size: 2rem !important; margin-bottom: 4px !important; }
    .add-confirm-title   {
        font-size: 1.1rem !important; font-weight: 900 !important;
        color: #155724 !important; margin: 4px 0 !important;
    }
    .add-confirm-product {
        font-size: 0.95rem !important; font-weight: 700 !important;
        color: #1e3c72 !important; background: #c8e6c9;
        padding: 4px 12px; border-radius: 8px;
        display: inline-block; margin: 6px 0 !important;
    }
    .add-confirm-stats {
        font-size: 0.9rem !important; font-weight: 700 !important;
        color: #374151 !important; margin: 6px 0 !important;
    }
    .add-confirm-hint {
        font-size: 0.82rem !important; font-weight: 600 !important;
        color: #6b7280 !important; margin-top: 6px !important;
    }

    /* ===== فاصل ===== */
    .divider {
        height: 3px;
        background: linear-gradient(90deg,#667eea,#764ba2);
        margin: 25px 0; border-radius: 10px;
    }

    /* ===== لوحة السلة والدفع ===== */
    .cart-panel {
        background: white; border-radius: 20px;
        box-shadow: 0 8px 40px rgba(0,0,0,0.12);
        border-top: 6px solid #1e3c72;
        overflow: hidden; margin: 20px 0;
    }
    .cart-panel-header {
        background: linear-gradient(135deg,#1e3c72,#2a5298);
        padding: 18px 25px; color: white;
        font-size: 1.3rem !important; font-weight: 900 !important;
        text-align: center !important;
    }

    /* ===== عنصر السلة ===== */
    .cart-item {
        background: #f8f9fa; border-radius: 12px;
        padding: 12px 15px; margin: 8px 0;
        border-right: 4px solid #667eea; direction: rtl;
    }
    .cart-item-name  { font-size:1rem !important; font-weight:700 !important; color:#2d3748 !important; }
    .cart-item-price { font-size:1rem !important; font-weight:900 !important; color:#28a745 !important; }

    /* ===== ملخص السعر ===== */
    .price-summary {
        background: linear-gradient(135deg,#1e3c72,#2a5298);
        border-radius: 15px; padding: 18px; color: white; margin: 15px 0;
    }
    .price-row {
        display: flex; justify-content: space-between;
        padding: 6px 0; font-size: 1rem !important; font-weight: 700 !important;
        border-bottom: 1px solid rgba(255,255,255,0.15);
    }
    .price-total {
        display: flex; justify-content: space-between;
        padding: 10px 0 0; font-size: 1.3rem !important;
        font-weight: 900 !important; color: #ffd700 !important;
    }

    /* ===== بطاقات الدفع ===== */
    .pay-section-title {
        font-size: 1.2rem !important; font-weight: 900 !important;
        color: #1e3c72 !important; text-align: center !important;
        padding: 12px; background: #f0f4ff; border-radius: 10px;
        margin: 15px 0 !important;
    }
    .pay-card { border-radius: 15px; padding: 18px; margin: 10px 0; direction: rtl; border-right: 6px solid; }
    .pay-card-cod      { background:#fffbeb; border-color:#f59e0b; }
    .pay-card-instapay { background:#ecfdf5; border-color:#10b981; }
    .pay-card-vodafone { background:#fff1f2; border-color:#e53935; }
    .pay-method-title  { font-size:1.1rem !important; font-weight:900 !important; margin-bottom:8px !important; }
    .pay-method-detail { font-size:0.95rem !important; font-weight:600 !important; color:#374151 !important; line-height:1.9 !important; }
    .pay-number {
        font-size: 1.3rem !important; font-weight: 900 !important;
        letter-spacing: 2px !important; direction: ltr !important;
        display: inline-block !important; color: #1e3c72 !important;
        background: white; padding: 4px 12px; border-radius: 8px;
        margin: 4px 0 !important; border: 2px dashed #94a3b8;
    }

    /* ===== عروض ===== */
    .offers-title {
        font-size: 1.8rem !important; font-weight: 900 !important;
        color: #ff4b4b !important; text-align: center !important;
        padding: 15px; background: #fff5f5; border-radius: 15px;
        border: 2px dashed #ff4b4b; margin: 15px 0 !important;
    }
    .item-box {
        background: white; border-radius: 15px; padding: 20px;
        margin-bottom: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.07); direction: rtl;
    }
    .item-title { font-size:1.6rem !important; font-weight:900 !important; color:#1e3c72 !important; margin-bottom:8px !important; }
    .item-desc  { font-size:0.95rem !important; font-weight:500 !important; color:#718096 !important; margin-bottom:10px !important; }
    .item-price { font-size:1.4rem !important; font-weight:900 !important; }

    /* ===== نموذج ===== */
    .form-section {
        background: #f8faff; border-radius: 15px;
        padding: 20px; margin: 15px 0; border: 1px solid #e2e8f0;
    }

    /* ===== رسالة نجاح ===== */
    .success-message {
        background: linear-gradient(135deg,#38ef7d,#11998e);
        padding: 20px; border-radius: 15px; text-align: center;
        color: white; font-size: 1.1rem; font-weight: 700; margin: 15px 0;
    }

    /* ===== موبايل ===== */
    @media (max-width: 768px) {
        .block-container { padding: 0.5rem !important; }
        .product-name    { font-size: 1.2rem !important; }
        .pay-number      { font-size: 1rem !important; letter-spacing:1px !important; }
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# الثوابت
# =============================================
WHATSAPP_NUMBER = "201022395878"
FACEBOOK_URL    = "https://www.facebook.com/share/p/1Dgba12hfT/"
DELIVERY_FEE    = 50
INSTAPAY_NUMBER = "01022395878"
VODAFONE_NUMBER = "01022395878"
INSTAPAY_NAME   = "VetFamily Alexandria"

CAIRO_TZ = pytz.timezone('Africa/Cairo')
def get_cairo_time(): return datetime.now(CAIRO_TZ)

# =============================================
# Session State
# =============================================
def hash_password(p): return hashlib.sha256(p.encode()).hexdigest()
ADMIN_USERNAME      = "melabed"
ADMIN_PASSWORD_HASH = hash_password("Ma3902242$")
def check_login(u, p): return u == ADMIN_USERNAME and hash_password(p) == ADMIN_PASSWORD_HASH

defaults = {
    'is_logged_in':       False,
    'show_adoption_form': False,
    'shopping_cart':      [],
    'adoption_requests':  [],
    'product_orders':     [],
    'subscriptions':      [],
    'notifications':      [],
    'show_cart_panel':    False,
    'show_login':         False,
    # ← المفتاح الجديد: يحفظ ID المنتج الذي أُضيف للسلة مؤخراً
    'just_added_id':      None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =============================================
# بيانات المنتجات
# =============================================
if 'products' not in st.session_state:
    st.session_state.products = {
        "طعام_القطط_الجاف": [
            {"id":1,"name":"رويال كانين - قطط بالغة 2 كجم",
             "description":"طعام متوازن للقطط البالغة من 1-7 سنوات",
             "price":450,"cost":320,"icon":"🐱","category":"طعام القطط الجاف","stock":25,
             "unit":"كيس 2 كجم","brand":"Royal Canin","country":"فرنسا",
             "features":["بروتين 32%","دهون 15%","فيتامينات متكاملة","أوميجا 3 و 6"],
             "badges":["popular","premium"]},
            {"id":2,"name":"رويال كانين كيتن - قطط صغيرة 1.5 كجم",
             "description":"تركيبة للقطط الصغيرة من شهرين إلى 12 شهر",
             "price":400,"cost":280,"icon":"🐈","category":"طعام القطط الجاف","stock":18,
             "unit":"كيس 1.5 كجم","brand":"Royal Canin","country":"فرنسا",
             "features":["سهل الهضم","دعم المناعة","تقوية العظام"],
             "badges":["new","recommended"]},
            {"id":3,"name":"بريميوم كات - قطط 1 كجم",
             "description":"طعام محلي عالي الجودة بسعر اقتصادي",
             "price":70,"cost":45,"icon":"🐱","category":"طعام القطط الجاف","stock":40,
             "unit":"كيس 1 كجم","brand":"Premium Cat","country":"مصر",
             "features":["جودة جيدة","سعر مناسب","بروتين 28%"],
             "badges":["sale"]},
        ],
        "طعام_القطط_الرطب": [
            {"id":5,"name":"ويسكاس - تونة في جيلي 85 جم",
             "description":"وجبة رطبة لذيذة من التونة الطبيعية",
             "price":25,"cost":15,"icon":"🐟","category":"طعام القطط الرطب","stock":100,
             "unit":"علبة 85 جم","brand":"Whiskas","country":"تايلاند",
             "features":["تونة طبيعية","غني بالبروتين","رطوبة عالية"],
             "badges":["popular"]},
            {"id":6,"name":"شيبا - دجاج مشوي 85 جم",
             "description":"وجبة فاخرة من الدجاج المشوي",
             "price":30,"cost":20,"icon":"🍗","category":"طعام القطط الرطب","stock":80,
             "unit":"علبة 85 جم","brand":"Sheba","country":"تايلاند",
             "features":["دجاج مشوي","طعم لذيذ","قطع كبيرة"],
             "badges":["premium"]},
        ],
        "طعام_الكلاب_الجاف": [
            {"id":8,"name":"رويال كانين - كلاب كبيرة 3 كجم",
             "description":"تركيبة للكلاب الكبيرة فوق 25 كجم",
             "price":550,"cost":380,"icon":"🐕","category":"طعام الكلاب الجاف","stock":20,
             "unit":"كيس 3 كجم","brand":"Royal Canin","country":"فرنسا",
             "features":["دعم المفاصل","بروتين 30%","طاقة عالية"],
             "badges":["popular","premium"]},
            {"id":9,"name":"بيديجري - كلاب بالغة 2.5 كجم",
             "description":"طعام متوازن للكلاب البالغة",
             "price":320,"cost":220,"icon":"🐕","category":"طعام الكلاب الجاف","stock":30,
             "unit":"كيس 2.5 كجم","brand":"Pedigree","country":"تايلاند",
             "features":["فيتامينات متكاملة","دجاج حقيقي","سهل الهضم"],
             "badges":["sale"]},
        ],
        "الرمل_والنظافة": [
            {"id":11,"name":"كات ساند - رمل متكتل 5 كجم",
             "description":"رمل بنتونايت متكتل برائحة اللافندر",
             "price":90,"cost":55,"icon":"🏖️","category":"الرمل والنظافة","stock":50,
             "unit":"كيس 5 كجم","brand":"Cat Sand","country":"مصر",
             "features":["سريع التكتل","امتصاص فائق","معطر"],
             "badges":["popular","sale"]},
            {"id":13,"name":"صندوق رمل قطط مع غطاء",
             "description":"صندوق بلاستيك عالي الجودة مع مجرفة",
             "price":150,"cost":90,"icon":"🚽","category":"الرمل والنظافة","stock":15,
             "unit":"قطعة","brand":"Pet Home","country":"الصين",
             "features":["سهل التنظيف","مع مجرفة","غطاء مانع للروائح"],
             "badges":["new"]},
        ],
        "الصحة_والأد��ية": [
            {"id":14,"name":"شامبو بيتكين الطبي 500 مل",
             "description":"شامبو طبي مضاد للحساسية والبراغيث",
             "price":130,"cost":70,"icon":"🧴","category":"الصحة والأدوية","stock":30,
             "unit":"زجاجة 500 مل","brand":"Petkin","country":"مصر",
             "features":["مضاد حساسية","مضاد براغيث","آمن تماماً"],
             "badges":["vet-recommended"]},
            {"id":15,"name":"فرونت لاين - قطرات ضد البراغيث",
             "description":"أقوى علاج للبراغيث والقراد",
             "price":150,"cost":85,"icon":"💧","category":"الصحة والأدوية","stock":20,
             "unit":"أمبول واحد","brand":"Frontline","country":"فرنسا",
             "features":["حماية شهرية","فعال 100%","سهل الاستخدام"],
             "badges":["premium","vet-recommended"]},
            {"id":18,"name":"قطرة عين فيتامين A",
             "description":"قطرة مطهرة لالتهابات العين",
             "price":85,"cost":45,"icon":"👁️","category":"الصحة والأدوية","stock":18,
             "unit":"زجاجة 15 مل","brand":"Pet Vision","country":"مصر",
             "features":["مطهرة","آمنة","سريعة المفعول"],
             "badges":["vet-recommended"]},
        ],
        "الإكسسوارات": [
            {"id":19,"name":"طوق جلد طبيعي مع جرس",
             "description":"طوق جلد أصلي قابل للتعديل",
             "price":80,"cost":35,"icon":"🎀","category":"الإكسسوارات","stock":35,
             "unit":"قطعة","brand":"Pet Style","country":"تركيا",
             "features":["جلد طبيعي","قابل للتعديل","جرس معدني"],
             "badges":["popular"]},
            {"id":20,"name":"سلسلة مشي نايلون قوية",
             "description":"سلسلة للكلاب المتوسطة والكبيرة",
             "price":90,"cost":40,"icon":"🦮","category":"الإكسسوارات","stock":25,
             "unit":"قطعة 1.5 متر","brand":"Strong Lead","country":"الصين",
             "features":["نايلون قوي","مقبض مريح","طول 1.5 م"],
             "badges":["sale"]},
            {"id":21,"name":"حقيبة نقل فاخرة",
             "description":"حقيبة آمنة للسفر والعيادات",
             "price":350,"cost":200,"icon":"🎒","category":"الإكسسوارات","stock":10,
             "unit":"مقاس متوسط","brand":"Travel Pet","country":"الصين",
             "features":["تهوية ممتازة","خفيفة الوزن","قابلة للطي"],
             "badges":["premium"]},
        ],
        "الألعاب": [
            {"id":23,"name":"فأر إلكتروني تفاعلي",
             "description":"يتحرك تلقائياً لتسلية القطط",
             "price":120,"cost":60,"icon":"🐭","category":"الألعاب","stock":20,
             "unit":"قطعة","brand":"Smart Toy","country":"الصين",
             "features":["حركة تلقائية","آمنة","بطاريات قابلة للشحن"],
             "badges":["new","popular"]},
            {"id":24,"name":"كرة مطاطية بجرس",
             "description":"كرة ملونة بجرس داخلي",
             "price":25,"cost":12,"icon":"⚽","category":"الألعاب","stock":50,
             "unit":"قطعة","brand":"Play Ball","country":"مصر",
             "features":["مطاط آمن","جرس داخلي","ألوان زاهية"],
             "badges":["sale"]},
        ],
        "العناية_والتجميل": [
            {"id":30,"name":"فرشاة تمشيط احترافية",
             "description":"فرشاة مزدوجة لفك التشابك",
             "price":50,"cost":22,"icon":"🪮","category":"العناية والتجميل","stock":20,
             "unit":"قطعة","brand":"Grooming Pro","country":"الصين",
             "features":["أسنان ناعمة","مقبض مريح","للفراء الطويل والقصير"],
             "badges":["recommended"]},
            {"id":31,"name":"مقص أظافر احترافي",
             "description":"مقص آمن بحماية من القص الزائد",
             "price":75,"cost":35,"icon":"✂️","category":"العناية والتجميل","stock":15,
             "unit":"قطعة","brand":"Nail Clipper","country":"ألمانيا",
             "features":["شفرة حادة","واقي أمان","مقبض مطاطي"],
             "badges":["premium"]},
            {"id":32,"name":"مناديل تنظيف معطرة",
             "description":"مناديل مبللة للتنظيف السريع",
             "price":45,"cost":22,"icon":"🧻","category":"العناية والتجميل","stock":35,
             "unit":"علبة 80 منديل","brand":"Fresh Wipes","country":"مصر",
             "features":["آمنة 100%","معطرة","مضادة للبكتيريا"],
             "badges":["popular"]},
        ],
        "الفيتامينات_والمكملات": [
            {"id":34,"name":"مالتي فيتامين للقطط",
             "description":"فيتامينات متعددة لصحة أفضل",
             "price":160,"cost":90,"icon":"💊","category":"الفيتامينات والمكملات","stock":15,
             "unit":"علبة 60 قرص","brand":"Pet Vitamin","country":"أمريكا",
             "features":["فيتامينات متكاملة","تقوية المناعة","طعم سمك"],
             "badges":["vet-recommended"]},
        ],
    }

if 'packages' not in st.session_state:
    st.session_state.packages = {
        "الباقة البرونزية": {
            "price":200,"duration":"شهرياً","description":"باقة أساسية للرعاية الشهرية",
            "icon":"🥉","color":"#CD7F32",
            "features":["استشارتان هاتفيتان","استشارة واتساب","خصم 10% على الأدوية"]},
        "الباقة الفضية": {
            "price":400,"duration":"شهرياً","description":"رعاية متقدمة مع فحوصات دورية",
            "icon":"🥈","color":"#C0C0C0",
            "features":["4 استشارات","فحص شامل مجاني","خصم 20% على المنتجات"]},
        "الباقة الذهبية": {
            "price":700,"duration":"شهرياً","description":"رعاية VIP شاملة",
            "icon":"🥇","color":"#FFD700",
            "features":["استشارات غير محدودة","زيارة منزلية","خصم 30% على المنتجات"]},
        "الباقة الماسية": {
            "price":1200,"duration":"شهرياً","description":"الأشمل - رعاية ملكية",
            "icon":"💎","color":"#B9F2FF",
            "features":["كل مميزات الذهبية","زيارتان منزليتان","خصم 40% على كل شيء"]},
    }

# =============================================
# دوال السلة
# =============================================
def add_to_cart(product):
    for item in st.session_state.shopping_cart:
        if item['id'] == product['id']:
            if item['quantity'] < product['stock']:
                item['quantity'] += 1; return True
            return False
    c = product.copy(); c['quantity'] = 1
    st.session_state.shopping_cart.append(c); return True

def remove_from_cart(pid):
    st.session_state.shopping_cart = [i for i in st.session_state.shopping_cart if i['id'] != pid]

def update_cart_qty(pid, qty):
    for item in st.session_state.shopping_cart:
        if item['id'] == pid:
            if qty <= 0: remove_from_cart(pid)
            else: item['quantity'] = qty
            break

def get_cart_total():
    return sum(i['price']*i['quantity'] for i in st.session_state.shopping_cart)

def get_cart_count():
    return sum(i['quantity'] for i in st.session_state.shopping_cart)

def get_grand_total():
    return get_cart_total() + DELIVERY_FEE if st.session_state.shopping_cart else 0

def build_wa_msg():
    lines = ["مرحباً VetFamily 🐾، أود طلب:\n"]
    for i in st.session_state.shopping_cart:
        lines.append(f"• {i['name']} × {i['quantity']} = {i['price']*i['quantity']} ج.م")
    lines += [f"\n🛒 المنتجات: {get_cart_total():,} ج.م",
              f"🚗 التوصيل: {DELIVERY_FEE} ج.م",
              f"💰 الإجمالي: {get_grand_total():,} ج.م",
              "برجاء التواصل لتأكيد الطلب 🙏"]
    return urllib.parse.quote("\n".join(lines))

def save_order(cart_items, info):
    try:
        ct = get_cairo_time()
        order = {
            "id": len(st.session_state.product_orders)+1,
            "items": [{"name":i['name'],"quantity":i['quantity'],
                       "price":i['price'],"total":i['price']*i['quantity']} for i in cart_items],
            "total_price":    get_cart_total(),
            "delivery_fee":   DELIVERY_FEE,
            "grand_total":    get_grand_total(),
            "payment_method": info.get("payment",""),
            "customer_name":  info["name"],
            "customer_phone": info["phone"],
            "customer_address": info.get("address",""),
            "notes": info.get("notes",""),
            "date": ct.strftime("%Y-%m-%d"),
            "time": ct.strftime("%H:%M:%S"),
            "status": "جديد"
        }
        st.session_state.product_orders.append(order)
        st.session_state.notifications.insert(0,{
            "type":"product_order",
            "message":f"طلب جديد من {info['name']}",
            "details":f"{get_grand_total():,} ج.م | {info.get('payment','')}",
            "timestamp":ct.strftime("%H:%M:%S"),
            "date":ct.strftime("%Y-%m-%d"),
        })
        st.session_state.shopping_cart = []
        st.session_state.just_added_id = None
        return True
    except Exception as e:
        st.error(f"خطأ: {e}"); return False

def save_subscription(pname, pdata, info):
    try:
        ct = get_cairo_time()
        st.session_state.subscriptions.append({
            "id":len(st.session_state.subscriptions)+1,
            "package_name":pname,"price":pdata['price'],"duration":pdata['duration'],
            "customer_name":info["name"],"customer_phone":info["phone"],
            "customer_address":info.get("address",""),
            "date":ct.strftime("%Y-%m-%d"),"time":ct.strftime("%H:%M:%S"),
            "status":"جديد","start_date":ct.strftime("%Y-%m-%d"),
            "end_date":(ct+timedelta(days=30)).strftime("%Y-%m-%d")
        })
        return True
    except Exception as e:
        st.error(f"خطأ: {e}"); return False

def save_adoption(info):
    try:
        ct = get_cairo_time()
        st.session_state.adoption_requests.append({
            "id":len(st.session_state.adoption_requests)+1,
            "customer_name":info["name"],"customer_phone":info["phone"],
            "customer_address":info.get("address",""),"pet_type":info["pet_type"],
            "pet_age":info.get("pet_age",""),"experience":info.get("experience",""),
            "home_type":info.get("home_type",""),"notes":info.get("notes",""),
            "date":ct.strftime("%Y-%m-%d"),"time":ct.strftime("%H:%M:%S"),"status":"جديد"
        })
        return True
    except Exception as e:
        st.error(f"خطأ: {e}"); return False

def get_badge_html(badges):
    m = {"new":("جديد","badge-new"),"sale":("عرض","badge-sale"),
         "popular":("الأكثر مبيعاً","badge-popular"),"premium":("بريميوم","badge-popular"),
         "recommended":("موصى به","badge-new"),"vet-recommended":("موصى طبياً","badge-sale")}
    return "".join(f'<span class="product-badge {c}">{t}</span>'
                   for b in badges if b in m for t,c in [m[b]])

# =============================================
# بطاقة المنتج - مع رسالة الإضافة تحت الزر
# =============================================
def display_product_card(product):
    pid = product['id']

    if product['stock'] > 10:
        sc, st_txt = "in-stock",  f"✅ متوفر ({product['stock']})"
    elif product['stock'] > 0:
        sc, st_txt = "low-stock", f"⚠️ محدود ({product['stock']})"
    else:
        sc, st_txt = "out-stock", "❌ نفذ"

    # ---- بطاقة المنتج ----
    st.markdown(f"""
    <div class='product-card'>
        <div class='product-image'>{product['icon']}</div>
        <div class='product-name'>{product['name']}</div>
        <div>{get_badge_html(product.get('badges',[]))}</div>
        <div class='product-description'>{product['description']}</div>
        <div class='product-price'>{product['price']} ج.م</div>
        <div style='font-size:0.8rem;color:#718096;font-weight:500;'>
            📦 {product['unit']} | 🏷️ {product['brand']}
        </div>
        <div class='stock-badge {sc}'>{st_txt}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📋 التفاصيل والمميزات"):
        for f in product['features']: st.write(f"✓ {f}")
        st.write(f"**🌍 بلد المنشأ:** {product['country']}")

    # ---- زر الإضافة ----
    ca, cb = st.columns([3, 1])
    with ca:
        if product['stock'] > 0:
            btn_label = "✅ تمت الإضافة!" if st.session_state.just_added_id == pid else "🛒 أضف للسلة"
            btn_type  = "secondary" if st.session_state.just_added_id == pid else "primary"

            if st.button(btn_label, key=f"add_{pid}",
                         use_container_width=True, type=btn_type):
                if add_to_cart(product):
                    st.session_state.just_added_id  = pid
                    st.session_state.show_cart_panel = False
                    st.rerun()
                else:
                    st.warning("⚠️ الكمية المتاحة محدودة")
        else:
            st.button("نفذ من المخزون ❌", disabled=True, use_container_width=True)

    with cb:
        if st.session_state.is_logged_in:
            profit = product['price'] - product['cost']
            st.caption(f"💰 {product['cost']} ج")
            st.caption(f"📈 +{profit/product['cost']*100:.0f}%")

    # ---- رسالة التأكيد تحت الزر مباشرة ----
    if st.session_state.just_added_id == pid:
        cart_count = get_cart_count()
        cart_total = get_cart_total()

        # بناء رابط واتساب لهذا المنتج
        wa_msg = urllib.parse.quote(
            f"مرحباً VetFamily 🐾\nأود طلب: {product['name']}\n"
            f"السعر: {product['price']} ج.م\nبرجاء التواصل 🙏"
        )
        wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={wa_msg}"

        st.markdown(f"""
        <div class="add-confirm-inline">
            <div class="add-confirm-icon">🎉</div>
            <div class="add-confirm-title">تمت الإضافة للسلة!</div>
            <div class="add-confirm-product">{product['icon']} {product['name']}</div>
            <div class="add-confirm-stats">
                💰 {product['price']} ج.م &nbsp;|&nbsp;
                🛒 السلة: {cart_count} منتج &nbsp;|&nbsp;
                💵 الإجمالي: {cart_total:,} ج.م
            </div>
            <div class="add-confirm-hint">
                👇 اختر ما تريد فعله الآن
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ثلاثة أزرار اختيار
        r1, r2, r3 = st.columns(3)

        with r1:
            if st.button("🛍️ استكمال التسوق",
                         key=f"cont_{pid}", use_container_width=True):
                st.session_state.just_added_id = None
                st.rerun()

        with r2:
            if st.button("💳 عرض السلة والدفع",
                         key=f"pay_{pid}", use_container_width=True, type="primary"):
                st.session_state.just_added_id  = None
                st.session_state.show_cart_panel = True
                st.rerun()

        with r3:
            st.link_button(
                "📱 طلب عبر واتساب",
                wa_link,
                use_container_width=True
            )

# =============================================
# لوحة السلة والدفع
# =============================================
def render_cart_and_payment():
    subtotal    = get_cart_total()
    grand_total = get_grand_total()

    st.markdown('<div class="cart-panel">', unsafe_allow_html=True)
    st.markdown('<div class="cart-panel-header">🛒 سلة التسوق وتفاصيل الدفع</div>',
                unsafe_allow_html=True)

    # ---- عناصر السلة ----
    st.markdown("#### 📦 منتجاتك")
    for item in st.session_state.shopping_cart:
        ic1, ic2, ic3 = st.columns([4, 2, 1])
        with ic1:
            st.markdown(f"""
            <div class="cart-item">
                <div class="cart-item-name">{item['icon']} {item['name']}</div>
                <div class="cart-item-price">
                    {item['price']} × {item['quantity']} =
                    {item['price']*item['quantity']} ج.م
                </div>
            </div>
            """, unsafe_allow_html=True)
        with ic2:
            nq = st.number_input("", min_value=1, max_value=item['stock'],
                                 value=item['quantity'], key=f"cq_{item['id']}",
                                 label_visibility="collapsed")
            if nq != item['quantity']:
                update_cart_qty(item['id'], nq); st.rerun()
        with ic3:
            if st.button("🗑️", key=f"del_{item['id']}", use_container_width=True):
                remove_from_cart(item['id']); st.rerun()

    # ---- ملخص السعر ----
    st.markdown(f"""
    <div class="price-summary">
        <div class="price-row">
            <span>🛒 إجمالي المنتجات</span><span>{subtotal:,} ج.م</span>
        </div>
        <div class="price-row">
            <span>🚗 رسوم التوصيل</span><span>{DELIVERY_FEE} ج.م</span>
        </div>
        <div class="price-total">
            <span>💰 الإجمالي الكلي</span><span>{grand_total:,} ج.م</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- طرق الدفع ----
    st.markdown('<div class="pay-section-title">🏦 طرق الدفع المتاحة</div>',
                unsafe_allow_html=True)

    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        st.markdown("""
        <div class="pay-card pay-card-cod">
            <div class="pay-method-title" style="color:#92400e;">💵 كاش عند الاستلام</div>
            <div class="pay-method-detail">
                ✅ ادفع عند وصول طلبك<br>
                ✅ لا رسوم إضافية<br>
                ✅ متاح في الإسكندرية كلها
            </div>
        </div>""", unsafe_allow_html=True)
    with pc2:
        st.markdown(f"""
        <div class="pay-card pay-card-instapay">
            <div class="pay-method-title" style="color:#065f46;">📲 إنستاباي</div>
            <div class="pay-method-detail">
                رقم الحساب:<br>
                <span class="pay-number">{INSTAPAY_NUMBER}</span><br>
                الاسم: <strong>{INSTAPAY_NAME}</strong><br>
                ✅ أرسل الإيصال على الواتساب
            </div>
        </div>""", unsafe_allow_html=True)
    with pc3:
        st.markdown(f"""
        <div class="pay-card pay-card-vodafone">
            <div class="pay-method-title" style="color:#991b1b;">📱 فودافون كاش</div>
            <div class="pay-method-detail">
                رقم المحفظة:<br>
                <span class="pay-number">{VODAFONE_NUMBER}</span><br>
                ✅ أرسل الإيصال على الواتساب<br>
                ✅ يُفعَّل الطلب فور التأكيد
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ---- نموذج بيانات العميل ----
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 📝 أكمل بياناتك لتأكيد الطلب")

    fc1, fc2 = st.columns(2)
    with fc1:
        cname    = st.text_input("الاسم الكامل *",  key="cp_name")
        caddress = st.text_input("عنوان التوصيل *", key="cp_addr")
    with fc2:
        cphone   = st.text_input("رقم الواتساب *",  key="cp_phone")
        cpayment = st.selectbox("طريقة الدفع *",
                                ["💵 كاش عند الاستلام","📲 إنستاباي","📱 فودافون كاش"],
                                key="cp_pay")
    cnotes = st.text_area("ملاحظات (اختياري)", key="cp_notes", height=70)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- أزرار التأكيد ----
    ba, bb, bc = st.columns(3)
    with ba:
        if st.button("✅ تأكيد الطلب", use_container_width=True,
                     type="primary", key="confirm_main"):
            if cname and cphone and caddress:
                if save_order(st.session_state.shopping_cart.copy(),
                              {"name":cname,"phone":cphone,"address":caddress,
                               "notes":cnotes,"payment":cpayment}):
                    st.session_state.show_cart_panel = False
                    st.markdown("""<div class='success-message'>
                        🎉 تم إرسال طلبك بنجاح!<br>
                        📞 سيتم التواصل معك للتأكيد والتوصيل<br>
                        🙏 شكراً لثقتك في VetFamily
                    </div>""", unsafe_allow_html=True)
                    st.balloons(); st.rerun()
            else:
                st.error("⚠️ برجاء إدخال الاسم والهاتف والعنوان")
    with bb:
        st.link_button("📱 طلب عبر واتساب",
                       f"https://wa.me/{WHATSAPP_NUMBER}?text={build_wa_msg()}",
                       use_container_width=True)
    with bc:
        if st.button("❌ إغلاق السلة", use_container_width=True, key="close_cart"):
            st.session_state.show_cart_panel = False; st.rerun()

    if st.button("🗑️ تفريغ السلة بالكامل", use_container_width=True, key="clear_cart"):
        st.session_state.shopping_cart   = []
        st.session_state.show_cart_panel = False; st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

def render_item(name, price, desc, is_medical=False):
    ac  = "#d9534f" if is_medical else "#28a745"
    msg = urllib.parse.quote(f"مرحباً VetFamily، أود طلب: {name}")
    st.markdown(f'''
    <div class="item-box" style="border-right:8px solid {ac};">
        <div class="item-title">{name}</div>
        <div class="item-desc">{desc}</div>
        <div class="item-price" style="color:{ac};">السعر: {price}</div>
    </div>''', unsafe_allow_html=True)
    st.link_button("طلب عبر واتساب 💬",
                   f"https://wa.me/{WHATSAPP_NUMBER}?text={msg}")

# =============================================
# ===== الصفحة الرئيسية =====
# =============================================
st.markdown("""
<div class='main-header'>
    <h1>🐾 VetFamily Alexandria 🐾</h1>
    <p>مركز الرعاية البيطرية المتكاملة - الإسكندرية</p>
    <p style='font-size:0.95rem;'>
        🩺 أطباء متخصصون &nbsp;|&nbsp; 🍖 منتجات أصلية
        &nbsp;|&nbsp; 🚗 توصيل +50 ج.م
    </p>
</div>
""", unsafe_allow_html=True)

# ===== شريط الأزرار =====
t1, t2, t3, t4 = st.columns(4)
with t1:
    if st.button("❤️ أعجبني", use_container_width=True):
        st.balloons(); st.success("شكراً! 🙏")
with t2:
    cnt = get_cart_count()
    lbl = f"🛒 السلة ({cnt}) | {get_cart_total():,} ج.م" if cnt > 0 else "🛒 السلة فارغة"
    if st.button(lbl, use_container_width=True,
                 type="primary" if cnt > 0 else "secondary"):
        if cnt > 0:
            st.session_state.show_cart_panel = not st.session_state.show_cart_panel
            st.session_state.just_added_id   = None
            st.rerun()
        else:
            st.info("🛒 أضف منتجات أولاً")
with t3:
    if st.button("🏠 تبني الآن", use_container_width=True):
        st.session_state.show_adoption_form = True
with t4:
    if st.button("🔐 المدير", use_container_width=True):
        st.session_state.show_login = not st.session_state.show_login
        st.rerun()

# ===== دخول المدير =====
if st.session_state.show_login and not st.session_state.is_logged_in:
    with st.expander("🔐 دخول لوحة التحكم", expanded=True):
        lc1, lc2, lc3 = st.columns([2,2,1])
        with lc1: lu = st.text_input("اسم المستخدم", key="lu")
        with lc2: lp = st.text_input("كلمة المرور", type="password", key="lp")
        with lc3:
            st.write("")
            if st.button("دخول 🔓", use_container_width=True):
                if check_login(lu, lp):
                    st.session_state.is_logged_in = True
                    st.session_state.show_login   = False
                    st.success("✅ تم الدخول"); st.rerun()
                else:
                    st.error("❌ خطأ في البيانات")

if st.session_state.is_logged_in:
    im1,im2,im3,im4 = st.columns(4)
    with im1: st.metric("📦 الطلبات",    len(st.session_state.product_orders))
    with im2: st.metric("💳 الاشتراكات", len(st.session_state.subscriptions))
    with im3: st.metric("🏠 التبني",     len(st.session_state.adoption_requests))
    with im4:
        if st.button("🔓 خروج", use_container_width=True):
            st.session_state.is_logged_in = False; st.rerun()

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ===== لوحة السلة والدفع =====
if st.session_state.show_cart_panel and st.session_state.shopping_cart:
    render_cart_and_payment()
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# =============================================
# التبويبات
# =============================================
if st.session_state.is_logged_in:
    tabs = st.tabs(["🏪 المتجر","💎 الباقات","🩺 الاستشارات",
                    "📊 لوحة التحكم","📦 الطلبات","💳 الاشتراكات","🏠 التبني"])
    tab_shop,tab_pkg,tab_con,tab_dash,tab_ord,tab_sub,tab_ado = tabs
else:
    tabs = st.tabs(["🏪 المتجر","💎 الباقات","🩺 الاستشارات","ℹ️ من نحن"])
    tab_shop,tab_pkg,tab_con,tab_about = tabs

# ===== المتجر =====
with tab_shop:
    st.write("## 🛒 متجر المستلزمات البيطرية")
    st.markdown('<div class="offers-title">🔥 عروض اليوم الحصرية</div>',
                unsafe_allow_html=True)

    daily_offers = [
        {"name":"📦 رويال كانين قطط 2 كجم",
         "price":"550 ج.م بدلاً من 650","desc":"عرض خاص لدعم صحة أليفك."},
        {"name":"🐱 رمل قطط كربون 5 لتر",
         "price":"180 ج.م بدلاً من 220","desc":"أفضل حماية من الروائح."},
    ]
    oc = st.columns(len(daily_offers))
    for i, o in enumerate(daily_offers):
        with oc[i]: render_item(o['name'], o['price'], o['desc'])

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    sc1, sc2, sc3 = st.columns([2,2,1])
    with sc1: srch = st.text_input("🔍 ابحث:", placeholder="اسم المنتج أو الماركة...")
    with sc2: scat = st.selectbox("📂 الفئة:", ["الكل"]+list(st.session_state.products.keys()))
    with sc3: ssrt = st.selectbox("ترتيب:", ["الأحدث","السعر: الأقل","السعر: الأعلى"])

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    for ck, prods in st.session_state.products.items():
        if scat != "الكل" and ck != scat: continue
        st.markdown(f"### 📦 {prods[0]['category']}")
        fp = [p for p in prods if not srch or
              srch.lower() in p['name'].lower() or
              srch.lower() in p['brand'].lower()]
        if not fp: continue
        if ssrt == "السعر: الأقل":   fp = sorted(fp, key=lambda x: x['price'])
        elif ssrt == "السعر: الأعلى": fp = sorted(fp, key=lambda x: x['price'], reverse=True)
        cols = st.columns(3)
        for idx, prod in enumerate(fp):
            with cols[idx%3]: display_product_card(prod)
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ===== الباقات =====
with tab_pkg:
    st.write("## 💎 الباقات الطبية")
    for pn, pd in st.session_state.packages.items():
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,{pd['color']}22,{pd['color']}44);
                    padding:25px;border-radius:18px;margin:15px 0;
                    border:3px solid {pd['color']};'>
            <h2 style='text-align:center;font-weight:900;'>{pd['icon']} {pn}</h2>
            <p style='text-align:center;'>{pd['description']}</p>
            <h1 style='text-align:center;color:{pd['color']};font-weight:900;'>
                {pd['price']} ج.م / {pd['duration']}
            </h1>
        </div>""", unsafe_allow_html=True)
        pc1, pc2 = st.columns([2,1])
        with pc1:
            for f in pd['features']: st.write(f"✅ {f}")
        with pc2:
            with st.form(f"pkg_{pn}"):
                n = st.text_input("الاسم:",   key=f"sn_{pn}")
                p = st.text_input("الهاتف:", key=f"sp_{pn}")
                a = st.text_input("العنوان:", key=f"sa_{pn}")
                if st.form_submit_button("🎯 اشترك الآن", use_container_width=True):
                    if n and p:
                        if save_subscription(pn, pd, {"name":n,"phone":p,"address":a}):
                            st.success(f"🎉 تم الاشتراك في {pn}!")
                            st.balloons(); st.rerun()
                    else: st.error("⚠️ أدخل الاسم والهاتف")
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ===== الاستشارات =====
with tab_con:
    st.write("## 🩺 الاستشارات البيطرية")
    cc1, cc2 = st.columns(2)
    with cc1:
        st.markdown("""<div style='background:linear-gradient(135deg,#667eea,#764ba2);
            padding:25px;border-radius:18px;color:white;'>
            <h3 style='color:white;'>👨‍⚕️ فريقنا الطبي</h3>
            <ul style='line-height:2;'><li>أطباء معتمدون</li>
            <li>خبرة واسعة</li><li>استشارات 24/7</li></ul></div>""",
            unsafe_allow_html=True)
    with cc2:
        st.markdown("""<div style='background:linear-gradient(135deg,#f093fb,#f5576c);
            padding:25px;border-radius:18px;color:white;'>
            <h3 style='color:white;'>📋 خدماتنا</h3>
            <ul style='line-height:2;'><li>الكشف والفحص</li>
            <li>التطعيمات</li><li>العمليات</li><li>التحاليل</li></ul></div>""",
            unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    svcs = [("📞","استشارة هاتفية","مجاني"),("🏥","استشارة بالعيادة","100 ج.م"),
            ("💉","كشف + تطعيم","150 ج.م"),("🏠","زيارة منزلية","250 ج.م"),
            ("🔬","فحص شامل","300 ج.م"),("⚕️","عملية صغرى","500 ج.م+")]
    sv_cols = st.columns(3)
    for idx,(ico,nm,pr) in enumerate(svcs):
        with sv_cols[idx%3]:
            st.markdown(f"""<div style='background:white;padding:18px;border-radius:14px;
                text-align:center;border:2px solid #667eea;margin:8px 0;'>
                <div style='font-size:2.5rem;'>{ico}</div>
                <h4 style='color:#2d3748;margin:8px 0;'>{nm}</h4>
                <h3 style='color:#667eea;margin:0;'>{pr}</h3></div>""",
                unsafe_allow_html=True)

# ===== لوحة التحكم =====
if st.session_state.is_logged_in:
    with tab_dash:
        st.write("## 📊 لوحة التحكم")
        st.info(f"🕐 {get_cairo_time().strftime('%Y-%m-%d %H:%M:%S')}")
        dm1,dm2,dm3,dm4 = st.columns(4)
        with dm1: st.metric("📦 الطلبات",   len(st.session_state.product_orders))
        with dm2: st.metric("💰 الإيرادات", f"{sum(o.get('grand_total',0) for o in st.session_state.product_orders):,} ج.م")
        with dm3: st.metric("💳 الاشتراكات",len(st.session_state.subscriptions))
        with dm4: st.metric("🏠 التبني",    len(st.session_state.adoption_requests))
        st.write("### 🔔 الإشعارات")
        for n in st.session_state.notifications[:10]:
            bg = {"product_order":"#667eea","subscription":"#f093fb",
                  "adoption":"#38ef7d"}.get(n['type'],"#764ba2")
            st.markdown(f"""<div style='background:linear-gradient(135deg,{bg},{bg}cc);
                padding:14px;border-radius:12px;color:white;margin:6px 0;'>
                <strong>{n['message']}</strong><br>
                <small>{n['details']} | {n['date']} {n['timestamp']}</small>
                </div>""", unsafe_allow_html=True)

    with tab_ord:
        st.write("## 📦 طلبات المنتجات")
        if st.session_state.product_orders:
            for order in reversed(st.session_state.product_orders):
                with st.expander(f"طلب #{order['id']} - {order['customer_name']} | {order.get('grand_total',0):,} ج.م"):
                    oc1,oc2,oc3 = st.columns(3)
                    with oc1:
                        st.write(f"**📞** {order['customer_phone']}")
                        st.write(f"**📍** {order['customer_address']}")
                    with oc2:
                        st.write(f"**📅** {order['date']} {order['time']}")
                        st.write(f"**💳** {order.get('payment_method','')}")
                    with oc3:
                        st.write(f"**🛒** {order['total_price']} ج.م")
                        st.write(f"**🚗** {order.get('delivery_fee',DELIVERY_FEE)} ج.م")
                        st.write(f"**💰** {order.get('grand_total',0)} ج.م")
                    for it in order['items']:
                        st.write(f"• {it['name']} × {it['quantity']} = {it['total']} ج.م")
                    opts = ["جديد","تم التواصل","قيد التجهيز",
                            "جاهز للتوصيل","تم التوصيل","ملغي"]
                    ns = st.selectbox("الحالة:", opts, key=f"so_{order['id']}")
                    if st.button("💾 حفظ الحالة", key=f"sv_{order['id']}"):
                        for o in st.session_state.product_orders:
                            if o['id'] == order['id']: o['status'] = ns
                        st.success("✅ تم الحفظ"); st.rerun()
        else: st.info("لا توجد طلبات بعد")

    with tab_sub:
        st.write("## 💳 الاشتراكات")
        if st.session_state.subscriptions:
            for s in reversed(st.session_state.subscriptions):
                with st.expander(f"{s['package_name']} - {s['customer_name']}"):
                    st.write(f"**📞** {s['customer_phone']} | **💰** {s['price']} ج.م/{s['duration']}")
                    st.write(f"**📅** {s['start_date']} ← {s['end_date']}")
        else: st.info("لا توجد اشتراكات")

    with tab_ado:
        st.write("## 🏠 طلبات التبني")
        if st.session_state.adoption_requests:
            for r in reversed(st.session_state.adoption_requests):
                with st.expander(f"#{r['id']} - {r['customer_name']} | {r['pet_type']}"):
                    st.write(f"**📞** {r['customer_phone']} | **🏡** {r.get('home_type','')}")
                    st.write(f"**📚** {r.get('experience','')} | **📅** {r['date']}")
                    if r.get('notes'): st.write(f"**📝** {r['notes']}")
        else: st.info("لا توجد طلبات تبني")

else:
    with tab_about:
        st.write("## ℹ️ عن VetFamily Alexandria")
        st.markdown("""<div style='background:linear-gradient(135deg,#667eea,#764ba2);
            padding:35px;border-radius:20px;color:white;text-align:center;'>
            <h2 style='color:white;'>🐾 عائلتك البيطرية في الإسكندرية</h2>
            <p style='font-size:1.1rem;'>مركز متكامل للرعاية البيطرية والمستلزمات</p>
            </div>""", unsafe_allow_html=True)
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        ab_cols = st.columns(3)
        for col,(ico,ttl,dsc) in zip(ab_cols,[
            ("👨‍⚕️","أطباء متخصصون","خبرة واسعة في جميع التخصصات"),
            ("🏆","منتجات أصلية","100% أصلية من أفضل العلامات العالمية"),
            ("🚗","توصيل سريع","لجميع مناطق الإسكندرية بـ 50 ج.م فقط")
        ]):
            with col:
                st.markdown(f"""<div style='text-align:center;padding:25px;background:white;
                    border-radius:15px;box-shadow:0 4px 15px rgba(0,0,0,0.08);'>
                    <div style='font-size:3.5rem;'>{ico}</div>
                    <h3 style='font-weight:900;'>{ttl}</h3><p>{dsc}</p></div>""",
                    unsafe_allow_html=True)
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        ac1, ac2 = st.columns(2)
        with ac1:
            st.markdown("- **📍** محرم بك - الإسكندرية\n- **📞** 01022395878")
        with ac2:
            st.markdown("- **🕐** يومياً 9 ص - 9 م\n- **💬** واتساب متاح")
        st.link_button("👍 تابعنا على فيسبوك", FACEBOOK_URL, use_container_width=True)

# ===== نموذج التبني =====
if st.session_state.show_adoption_form:
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("""<div style='background:linear-gradient(135deg,#38ef7d,#11998e);
        padding:20px;border-radius:18px;text-align:center;color:white;margin-bottom:15px;'>
        <h2 style='color:white;margin:0;'>🏠 نموذج طلب التبني 🐾</h2></div>""",
        unsafe_allow_html=True)
    with st.form("adoption_form"):
        af1, af2 = st.columns(2)
        with af1:
            an = st.text_input("الاسم الكامل *")
            ap = st.text_input("رقم الواتساب *")
        with af2:
            aa = st.text_input("العنوان *")
            ah = st.selectbox("نوع السكن:", ["شقة","فيلا","منزل مستقل","آخر"])
        af3, af4 = st.columns(2)
        with af3: pt = st.selectbox("نوع الحيوان:", ["قطة 🐱","كلب 🐕","طائر 🐦","أرنب 🐰","أخرى"])
        with af4: pa = st.selectbox("العمر المفضل:", ["صغير","متوسط","كبير","لا يهم"])
        ae  = st.radio("خبرة سابقة؟", ["نعم","لا","خبرة بسيطة"])
        ano = st.text_area("ملاحظات:")
        af5, af6 = st.columns(2)
        with af5: sub = st.form_submit_button("📝 إرسال الطلب", use_container_width=True, type="primary")
        with af6: can = st.form_submit_button("❌ إلغاء",        use_container_width=True)
        if sub:
            if an and ap and aa:
                if save_adoption({"name":an,"phone":ap,"address":aa,"home_type":ah,
                                  "pet_type":pt,"pet_age":pa,"experience":ae,"notes":ano}):
                    st.markdown("""<div class='success-message'>
                        🎉 تم إرسال طلب التبني! سيتم التواصل قريباً 💚
                    </div>""", unsafe_allow_html=True)
                    st.balloons()
                    st.session_state.show_adoption_form = False; st.rerun()
            else: st.error("⚠️ أدخل الاسم والهاتف والعنوان")
        if can:
            st.session_state.show_adoption_form = False; st.rerun()

# ===== الفوتر =====
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align:center;padding:25px;
            background:linear-gradient(135deg,#1e3c72,#2a5298);
            border-radius:18px;color:white;margin-top:20px;'>
    <h3 style='color:white;font-weight:900;'>🐾 VetFamily Alexandria 🐾</h3>
    <p style='margin:5px 0;'>مركز الرعاية البيطرية المتكاملة</p>
    <p style='font-size:0.85rem;margin-top:10px;color:rgba(255,255,255,0.8);'>
        📍 محرم بك - الإسكندرية &nbsp;|&nbsp;
        📞 01022395878 &nbsp;|&nbsp;
        🚗 توصيل 50 ج.م فقط<br>
        © 2024 VetFamily Alexandria
    </p>
</div>""", unsafe_allow_html=True)