# rule_engine/classifier.py
import json
import re
from pathlib import Path


# تحميل القاموس من lexicon.json الموجود في نفس المجلد
LEXICON_PATH = Path(__file__).with_name("lexicon.json")

with open(LEXICON_PATH, "r", encoding="utf-8") as f:
    LEXICON = json.load(f)


def _normalize(text: str) -> str:
    """تبسيط النص العربي لإزالة بعض الاختلافات في الكتابة."""
    if not text:
        return ""

    t = text.strip()

    # توحيد الألف
    t = re.sub("[إأآا]", "ا", t)
    # توحيد الياء والألف المقصورة
    t = re.sub("[يى]", "ي", t)
    # إزالة التشكيل
    t = re.sub("[ًٌٍَُِّْـ]", "", t)

    return t


def score(text: str) -> dict:
    """
    يستقبل نص البلاغ ويرجع:
    - normalized: النص بعد التطبيع
    - scores: عدد التطابقات لكل جهة
    - matches: الكلمات التي طابقت لكل جهة
    - target_agency: الجهة المقترحة
    """

    t = _normalize(text)

    scores = {
        "trade": 0,
        "balady": 0,
        "transport": 0
    }

    matches = {
        "trade": [],
        "balady": [],
        "transport": []
    }

    # دالة مساعدة لحساب التطابقات
    def count_hits(words, key):
        for kw in words:
            kw_norm = _normalize(kw)
            if kw_norm and kw_norm in t:
                scores[key] += 1
                matches[key].append(kw)

    count_hits(LEXICON.get("trade", []), "trade")
    count_hits(LEXICON.get("balady", []), "balady")
    count_hits(LEXICON.get("transport", []), "transport")

    # اختيار الجهة
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
        "target_agency": target_agency
    }
