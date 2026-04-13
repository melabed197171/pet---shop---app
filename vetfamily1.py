# إضافة زر "انضم لصفحة الفيسبوك" في أماكن متعددة

أضف هذه الأكواد في الأماكن المحددة:

## 1. إضافة زر في الهيدر (أسفل العنوان)

ابحث عن قسم الهيدر (بعد السطر 280 تقريباً) وأضف هذا:

```python
# بعد علامة الإغلاق للهيدر </div>
# أضف هذا الكود:

st.markdown(f"""
<div style="text-align:center;margin:15px 0;">
    <a href="{FACEBOOK_URL}" target="_blank"
       style="display:inline-block;
              background:#1877f2;color:white;
              padding:12px 30px;border-radius:30px;
              font-size:1.1rem;font-weight:900;
              text-decoration:none;box-shadow:0 4px 15px rgba(24,119,242,0.4);">
        👍 انضم لصفحتنا على الفيسبوك
    </a>
</div>
""", unsafe_allow_html=True)
```

---

## 2. إضافة زر في المتجر (أعلى قائمة المنتجات)

ابحث عن `with tab_shop:` وأضف هذا بعده مباشرة:

```python
with tab_shop:
    # إضافة زر الفيسبوك هنا
    st.markdown(f"""
    <div style="text-align:center;margin:15px 0;">
        <a href="{FACEBOOK_URL}" target="_blank"
           style="display:inline-block;
                  background:linear-gradient(135deg,#1877f2,#42a5f5);
                  color:white;padding:14px 35px;border-radius:30px;
                  font-size:1.1rem;font-weight:900;text-decoration:none;
                  box-shadow:0 4px 20px rgba(24,119,242,0.4);">
            👍 تابعنا على الفيسبوك للحصول على العروض الحصرية
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.write("## 🛒 متجر المستلزمات البيطرية")
    # ... باقي الكود
```

---

## 3. زر في الفوتر (للمدير والصفحة عنا)

ابحث عن نهاية الملف (الأسطر الأخيرة) وأضف هذا قبل الفوتر:

```python
# قبل الفوتر مباشرة
st.markdown(f"""
<div style="text-align:center;padding:20px;margin:30px 0;
            background:linear-gradient(135deg,#1877f2,#42a5f5);
            border-radius:20px;">
    <h3 style="color:white;margin:0;">👍 انضموا لعائلة VetFamily على الفيسبوك</h3>
    <p style="color:white;margin:10px 0 0;font-size:1rem;">
        تابعوا أحدث العروض والنصائح البيطرية أولاً بأول
    </p>
    <a href="{FACEBOOK_URL}" target="_blank"
       style="display:inline-block;
              background:white;color:#1877f2;
              padding:12px 40px;border-radius:30px;
              font-size:1.2rem;font-weight:900;
              text-decoration:none;margin-top:15px;">
        انضم الآن للصفحة 👈
    </a>
</div>
""", unsafe_allow_html=True)
```

---

## 4. تعديل رابط الفيسبوك في الثوابت

تأكد من تحديث الرابط في الأعلى:

```python
FACEBOOK_URL = "https://www.facebook.com/share/17LZbHtWzW/"
```

---

الآن لديك زر انضم للفيسبوك في:
1. **الهيدر** - أعلى الصفحة
2. **المتجر** - فوق المنتجات
3. **الصفحة عنا** - في الفوتر
4. **صفحة المدير** - زر في القائمة
