import joblib
import re
from pathlib import Path

def normalize_ar(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^0-9\u0600-\u06FF\s]+", " ", text)
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    text = text.replace("ى", "ي").replace("ة", "ه").replace("ؤ", "و").replace("ئ", "ي")
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ===== Paths =====
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "best_model.pkl"
VECT_PATH  = BASE_DIR / "models" / "tfidf_vectorizer.pkl"

print("MODEL_PATH:", MODEL_PATH)
print("VECT_PATH:", VECT_PATH)

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECT_PATH)

AGENCY_LABELS = {
    "trade": "وزارة التجارة",
    "balady": "وزارة الشؤون البلدية والقروية والإسكان",
    "transport": "الهيئة العامة للنقل",
}

def predict_agency(text: str):
    clean = normalize_ar(text)
    X_vec = vectorizer.transform([clean])
    label = model.predict(X_vec)[0]
    agency_name = AGENCY_LABELS.get(label, "جهة غير معروفة")
    return agency_name, label
