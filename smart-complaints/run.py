# -*- coding: utf-8 -*-
import sys
from rule_engine.classifier import score

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("اكتبي نص البلاغ بعد اسم الملف. مثال:\npython run.py \"في حفرة كبيرة والإنارة طافية\"")
        sys.exit(0)

    text = " ".join(sys.argv[1:])
    result = score(text)
    print("\nنــتــيــجــة الــتــصــنــيــف")
    print("---------------------------")
    print("النص:", text)
    print("الجهة:", result["target_agency"])
    print("الدرجات:", result["scores"])
    print("مطابقات التجارة:", ", ".join(result["matches"]["وزارة التجارة"]) or "لا يوجد")
    print("مطابقات الأمانة:", ", ".join(result["matches"]["الأمانة"]) or "لا يوجد")
    print("مطابقات النقل:", ", ".join(result["matches"]["هيئة النقل"]) or "لا يوجد")

