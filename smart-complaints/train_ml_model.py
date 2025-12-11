# train_ml_model.py

# 1) Import libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
import joblib
import re
from pathlib import Path

# 2) Define base directory and dataset path
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "complaints_dataset.csv"

# 3) Load dataset
print("Loading dataset from:", DATA_PATH)
df = pd.read_csv(DATA_PATH)

print("Columns:", df.columns)

# 4) Normalize text function (Arabic)
def normalize_ar(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^0-9\u0600-\u06FF\s]+", " ", text)
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    text = text.replace("ى", "ي").replace("ة", "ه").replace("ؤ", "و").replace("ئ", "ي")
    text = re.sub(r"\s+", " ", text).strip()
    return text

# 5) Apply cleaning
df["clean_text"] = df["text"].apply(normalize_ar)

print("Unique labels:", df["label"].unique())
print("Label counts:")
print(df["label"].value_counts())

X = df["clean_text"]
y = df["label"]

# 6) Split train / test
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Train size:", len(X_train))
print("Test size:", len(X_test))

# 7) TF-IDF vectorizer (NLP part)
tfidf = TfidfVectorizer(
    ngram_range=(1, 2),
    max_features=5000
)

X_train_vec = tfidf.fit_transform(X_train)
X_test_vec = tfidf.transform(X_test)

# 8) Define models
models = {
    "svm": LinearSVC(),
    "logistic_regression": LogisticRegression(max_iter=1000),
    "naive_bayes": MultinomialNB()
}

best_model_name = None
best_acc = 0.0
best_model = None

# 9) Train and evaluate each model
for name, model in models.items():
    print("=" * 60)
    print(f"Training model: {name}")
    model.fit(X_train_vec, y_train)

    # Train accuracy
    y_train_pred = model.predict(X_train_vec)
    train_acc = accuracy_score(y_train, y_train_pred)

    # Test accuracy
    y_test_pred = model.predict(X_test_vec)
    test_acc = accuracy_score(y_test, y_test_pred)

    print(f"Train Accuracy: {train_acc:.3f}")
    print(f"Test  Accuracy: {test_acc:.3f}")
    print("Classification Report (Test):")
    print(classification_report(y_test, y_test_pred))

    if test_acc > best_acc:
        best_acc = test_acc
        best_model_name = name
        best_model = model

print("=" * 60)
print(f"Best model is: {best_model_name} with test accuracy {best_acc:.3f}")

# 10) Save best model and vectorizer
models_dir = BASE_DIR / "models"
models_dir.mkdir(exist_ok=True)

joblib.dump(best_model, models_dir / f"{best_model_name}.pkl")
joblib.dump(tfidf, models_dir / "tfidf_vectorizer.pkl")

print("Saved model to:", models_dir)
