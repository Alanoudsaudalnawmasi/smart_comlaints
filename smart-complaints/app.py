import streamlit as st
import random
from rule_engine.classifier import score
import streamlit.components.v1 as components  # مهم

# ---------------- إعداد الصفحة ----------------
st.set_page_config(page_title="منصة تحسين البلاغات", layout="centered")

PAGE_CSS = """
<style>
html, body, [class*="css"] {
    direction: rtl;
    font-family: "Segoe UI", Tahoma, Arial, sans-serif;
}
label, textarea, input, select {
    font-size: 16px !important;
}
</style>
"""
st.markdown(PAGE_CSS, unsafe_allow_html=True)

# ---------------- العنوان ----------------
st.markdown(
    "<h2 style='text-align:center; color:#0d5c2c;'>منصة تحسين البلاغات</h2>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:#444;'>نموذج تجريبي لتسجيل البلاغات وتوجيهها تلقائياً إلى الجهة المختصة.</p>",
    unsafe_allow_html=True
)
st.write("---")

# ---------------- حقول الإدخال ----------------
name = st.text_input("الاسم", placeholder="اكتب اسمك هنا")
phone = st.text_input("رقم الجوال", placeholder="05xxxxxxxx")

region = st.selectbox(
    "المنطقة",
    [
        "",
        "الرياض", "مكة المكرمة", "المدينة المنورة", "الشرقية",
        "القصيم", "حائل", "عسير", "تبوك", "الجوف", "الباحة",
        "جازان", "نجران"
    ]
)

complaint_text = st.text_area("نص البلاغ", height=160)

submitted = st.button("رفع البلاغ")

# ---------------- معالجة البلاغ ----------------
if submitted:
    if not complaint_text.strip():
        st.warning("فضلاً اكتب نص البلاغ قبل رفعه.")
    else:
        # تشغيل محرك القواعد لتحديد الجهة
        result = score(complaint_text)
        agency = result.get("target_agency", "غير محددة")

        # رقم عشوائي للبلاغ
        ticket_id = random.randint(100000, 999999)

        # تجهيز الاسم للعرض
        display_name = name.strip() if name.strip() else "عميلنا"

        # -------- رسالة النجاح كـ HTML --------
        success_html = f"""
        <div style="
            background-color:#ffffff;
            padding:25px;
            border-radius:15px;
            border:1px solid #dddddd;
            margin-top:25px;
            text-align:center;
            direction:rtl;
        ">
            <h3 style="color:#0d5c2c; margin-bottom:10px;">
                سعيدين بخدمتك يا {display_name}
            </h3>

            <p style="font-size:18px; margin:8px 0;">
                تم توجيه بلاغك إلى:
                <span style="color:#b8860b; font-weight:bold;">
                    {agency}
                </span>
            </p>

            <p style="font-size:20px; margin-top:12px;">
                رقم البلاغ:
                <span style="color:#d4a017; font-weight:bold; font-size:28px;">
                    {ticket_id}
                </span>
            </p>
        </div>
        """

        # عرض HTML مباشرة كمكون
        components.html(success_html, height=230)



