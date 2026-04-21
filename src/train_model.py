print("Training script started...")

import os
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, VotingClassifier

from xgboost import XGBClassifier


# ---------------------------------------------------
# 1. Load Processed Dataset
# ---------------------------------------------------
DATA_PATH = "data/processed/esales_clean.csv"

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

df = pd.read_csv(DATA_PATH)

print("Dataset loaded")
print("Shape:", df.shape)


# ---------------------------------------------------
# 2. Feature / Target Split
# ---------------------------------------------------
target = "delivery_delay"

if target not in df.columns:
    raise ValueError("Target column 'delivery_delay' not found")

X = df.drop(target, axis=1)
y = df[target]

print("Number of features:", X.shape[1])


# ---------------------------------------------------
# 3. Class Distribution
# ---------------------------------------------------
print("\nClass Distribution:")
print(y.value_counts(normalize=True))


# ---------------------------------------------------
# 4. Train Test Split
# ---------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

print("Train size:", X_train.shape)
print("Test size:", X_test.shape)


# ---------------------------------------------------
# 5. Random Forest Model
# ---------------------------------------------------
print("\nTraining Random Forest...")

rf_model = RandomForestClassifier(
    n_estimators=400,
    max_depth=None,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train, y_train)

rf_probs = rf_model.predict_proba(X_test)[:, 1]

rf_auc = roc_auc_score(y_test, rf_probs)

print("Random Forest ROC-AUC:", rf_auc)


# ---------------------------------------------------
# 6. XGBoost Model
# ---------------------------------------------------
print("\nTraining XGBoost...")

scale = (y_train == 0).sum() / (y_train == 1).sum()

xgb_model = XGBClassifier(
    n_estimators=500,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=scale,
    eval_metric="auc",
    random_state=42,
    n_jobs=-1
)

xgb_model.fit(X_train, y_train)

xgb_probs = xgb_model.predict_proba(X_test)[:, 1]

xgb_auc = roc_auc_score(y_test, xgb_probs)

print("XGBoost ROC-AUC:", xgb_auc)


# ---------------------------------------------------
# 7. Ensemble Model (Soft Voting)
# ---------------------------------------------------
print("\nTraining Ensemble Model...")

voting_model = VotingClassifier(
    estimators=[
        ("rf", rf_model),
        ("xgb", xgb_model)
    ],
    voting="soft",
    weights=[2, 1]
)

voting_model.fit(X_train, y_train)

voting_probs = voting_model.predict_proba(X_test)[:, 1]

ensemble_auc = roc_auc_score(y_test, voting_probs)

print("Ensemble ROC-AUC:", ensemble_auc)


# ---------------------------------------------------
# 8. Threshold Evaluation
# ---------------------------------------------------
print("\nThreshold Evaluation")

thresholds = [0.5, 0.4, 0.3, 0.25, 0.2]

for t in thresholds:

    print(f"\nThreshold: {t}")

    y_pred = (voting_probs >= t).astype(int)

    print(classification_report(y_test, y_pred))


# ---------------------------------------------------
# 9. Confusion Matrix (Best Threshold)
# ---------------------------------------------------
best_threshold = 0.25

y_pred_best = (voting_probs >= best_threshold).astype(int)

cm = confusion_matrix(y_test, y_pred_best)

print("\nConfusion Matrix (threshold 0.25):")
print(cm)


# ---------------------------------------------------
# 10. Feature Importance (Random Forest)
# ---------------------------------------------------
print("\nTop Feature Importance")

feature_importance = pd.Series(
    rf_model.feature_importances_,
    index=X.columns
).sort_values(ascending=False)

print(feature_importance.head(10))

# Plot
feature_importance.head(10).plot(kind="barh")
plt.title("Top Feature Importance")
plt.show()


# ---------------------------------------------------
# 11. Save Model
# ---------------------------------------------------
os.makedirs("models", exist_ok=True)

MODEL_PATH = "models/delivery_delay_model.pkl"

joblib.dump(voting_model, MODEL_PATH)

print(f"\nModel saved to {MODEL_PATH}")

print("\nTraining completed successfully!")