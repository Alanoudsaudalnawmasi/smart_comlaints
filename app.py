import streamlit as st
import random
import streamlit.components.v1 as components

from rule_engine.classifier import score as rule_score
from ml_model import predict_agency

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

# ---------------- منطق المعالجة عند الضغط على الزر ----------------
if submitted:
    if not complaint_text.strip():
        st.warning("فضلاً اكتب نص البلاغ قبل رفعه.")
    else:
        # --- Rule-Based Result ---
        rb_result = rule_score(complaint_text)
        rb_agency = rb_result.get("target_agency", "غير محددة")

        # --- ML Result ---
        ml_agency, ml_label = predict_agency(complaint_text)

        # --- القرار النهائي: نعتمد محرك القواعد ---
        final_agency = rb_agency

        # --- نص التوضيح ---
        if rb_agency == ml_agency:
            compare_note = f"""
            <p style="font-size:16px; margin-top:12px; color:#444;">
                <b>ملاحظة:</b>
                نتيجة محرك القواعد ونموذج الـ ML كانت متطابقة
                (<span style="color:#0d5c2c; font-weight:bold;">{rb_agency}</span>).
            </p>
            """
        else:
            compare_note = f"""
            <p style="font-size:16px; margin-top:12px; color:#444;">
                <b>ملاحظة:</b>
                محرك القواعد اقترح:
                <span style="color:#0d5c2c; font-weight:bold;">{rb_agency}</span><br>
                بينما نموذج الـ ML (المبني على بيانات تدريب محدودة) اقترح:
                <span style="color:#b8860b; font-weight:bold;">{ml_agency}</span><br>
                لذلك تم الاعتماد في القرار النهائي على
                <span style="font-weight:bold;">محرك القواعد</span>
                لأنه أكثر ثباتاً مع كمية البيانات الحالية.
            </p>
            """

        # رقم عشوائي للبلاغ
        ticket_id = random.randint(100000, 999999)

        # الاسم المعروض
        display_name = name.strip() if name.strip() else "عميلنا"

        # --- HTML Message ---
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
                    {final_agency}
                </span>
            </p>

            <p style="font-size:20px; margin-top:12px;">
                رقم البلاغ:
                <span style="color:#d4a017; font-weight:bold; font-size:28px;">
                    {ticket_id}
                </span>
            </p>

            {compare_note}
        </div>
        """

        components.html(success_html, height=360)





