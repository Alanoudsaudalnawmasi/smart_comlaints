# rule_engine/classifier.py
import json
import re
from pathlib import Path

# تحميل القاموس من lexicon.json الموجود في نفس المجلد
LEXICON_PATH = Path(__file__).with_name("lexicon.json")

with open(LEXICON_PATH, "r", encoding="utf-8") as f:
    LEXICON = json.load(f)


def normalize_ar(text: str) -> str:
    """Normalize Arabic text so matching becomes more robust."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    # إزالة أي شيء غير أرقام/حروف عربية/مسافات
    text = re.sub(r"[^0-9\u0600-\u06FF\s]+", " ", text)
    # توحيد بعض الحروف
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    text = text.replace("ى", "ي").replace("ؤ", "و").replace("ئ", "ي")
    # أهم نقطة: تحويل ة إلى ه عشان ما نتعلق بفرق الكتابة
    text = text.replace("ة", "ه")
    # إزالة المسافات الزائدة
    text = re.sub(r"\s+", " ", text).strip()
    return text


def score(text: str) -> dict:
    """
    يستقبل نص البلاغ ويرجع:
    - normalized: النص بعد التطبيع
    - scores: عدد التطابقات لكل جهة
    - matches: الكلمات التي طابقت لكل جهة
    - target_agency: الجهة المقترحة
    """

    # نطبّع نص البلاغ
    t = normalize_ar(text)

    scores = {
        "trade": 0,
        "balady": 0,
        "transport": 0,
    }

    matches = {
        "trade": [],
        "balady": [],
        "transport": [],
    }

    # دالة مساعدة لحساب التطابقات
    def count_hits(words, key):
        for kw in words:
            kw_norm = normalize_ar(kw)
            if kw_norm and kw_norm in t:
                scores[key] += 1
                matches[key].append(kw)

    count_hits(LEXICON.get("trade", []), "trade")
    count_hits(LEXICON.get("balady", []), "balady")
    count_hits(LEXICON.get("transport", []), "transport")

    # اختيار الجهة بناءً على أعلى سكور
    max_score = max(scores.values())

    if max_score == 0:
        target_agency = "يحتاج مراجعة بشرية"
    else:
        best_keys = [k for k, v in scores.items() if v == max_score]

        if len(best_keys) > 1:
            target_agency = "يحتاج مراجعة، البلاغ يبدو أنه يخص أكثر من جهة"
        else:
            k = best_keys[0]
            if k == "trade":
                target_agency = "وزارة التجارة"
            elif k == "balady":
                target_agency = "وزارة الشؤون البلدية والقروية والإسكان"
            elif k == "transport":
                target_agency = "الهيئة العامة للنقل"
            else:
                target_agency = "يحتاج مراجعة بشرية"

    return {
        "normalized": t,
        "scores": scores,
        "matches": matches,
        "target_agency": target_agency,
    }

