import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "village_data.csv"

MODEL_PATH = BASE_DIR / "ml" / "disease_risk_model.pkl"


# =========================================================
# START
# =========================================================

print()
print("=" * 60)
print("JEEVAN-ALERT AI MODEL TRAINING")
print("=" * 60)


# =========================================================
# LOAD DATASET
# =========================================================

print()
print("Loading dataset...")

data = pd.read_csv(DATA_PATH)

data.columns = data.columns.str.strip()

print("Dataset loaded successfully!")

print()
print("Number of villages:", len(data))


# =========================================================
# WATER QUALITY ENCODING
# =========================================================

water_quality_map = {
    "Good": 0,
    "Medium": 1,
    "Poor": 2
}

data["water_quality_encoded"] = (
    data["water_quality"]
    .map(water_quality_map)
    .fillna(1)
)


# =========================================================
# FLOOD STATUS ENCODING
# =========================================================

flood_map = {
    "No": 0,
    "Yes": 1
}

data["flood_status_encoded"] = (
    data["flood_status"]
    .map(flood_map)
    .fillna(0)
)


# =========================================================
# NORMALIZED RISK FACTORS
# =========================================================

rainfall_max = max(
    data["rainfall"].max(),
    1
)

data["rainfall_risk"] = (
    data["rainfall"] / rainfall_max
)


cases_max = max(
    data["previous_cases"].max(),
    1
)

data["cases_risk"] = (
    data["previous_cases"] / cases_max
)


data["sanitation_risk"] = (
    1 - (data["sanitation_score"] / 100)
)


# =========================================================
# CALCULATE DEMO RISK SCORE
# =========================================================

data["risk_score"] = (

    data["water_quality_encoded"] * 30

    +

    data["cases_risk"] * 25

    +

    data["rainfall_risk"] * 20

    +

    data["sanitation_risk"] * 15

    +

    data["flood_status_encoded"] * 10

)


# =========================================================
# CREATE RISK LABEL
# =========================================================

def get_risk_level(score):

    if score >= 55:
        return "High"

    elif score >= 30:
        return "Medium"

    else:
        return "Low"


data["risk_level"] = data["risk_score"].apply(
    get_risk_level
)


# =========================================================
# RISK DISTRIBUTION
# =========================================================

print()
print("=" * 60)
print("GENERATED RISK LEVELS")
print("=" * 60)

print()

print(
    data[
        [
            "village",
            "risk_score",
            "risk_level"
        ]
    ].to_string(index=False)
)


print()
print("Risk distribution:")

print(
    data["risk_level"].value_counts()
)


# =========================================================
# FEATURES
# =========================================================

features = [

    "population",

    "rainfall",

    "temperature",

    "humidity",

    "water_quality_encoded",

    "previous_cases",

    "sanitation_score",

    "flood_status_encoded"

]


X = data[features]

y = data["risk_level"]


# =========================================================
# TRAIN / TEST SPLIT
# =========================================================

print()
print("Splitting dataset...")

# IMPORTANT:
# Medium class me sirf 1 sample hai.
# Isliye stratify=y use nahi karenge.

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.30,

    random_state=42

)


print(
    "Training samples:",
    len(X_train)
)

print(
    "Testing samples:",
    len(X_test)
)


# =========================================================
# RANDOM FOREST
# =========================================================

print()
print("Training Random Forest model...")

model = RandomForestClassifier(

    n_estimators=200,

    max_depth=8,

    random_state=42,

    class_weight="balanced"

)


model.fit(
    X_train,
    y_train
)


print(
    "Model trained successfully!"
)


# =========================================================
# PREDICTION
# =========================================================

y_pred = model.predict(
    X_test
)


# =========================================================
# MODEL PERFORMANCE
# =========================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)


precision = precision_score(

    y_test,

    y_pred,

    average="weighted",

    zero_division=0

)


recall = recall_score(

    y_test,

    y_pred,

    average="weighted",

    zero_division=0

)


f1 = f1_score(

    y_test,

    y_pred,

    average="weighted",

    zero_division=0

)


# =========================================================
# CONFUSION MATRIX
# =========================================================

labels = [
    "Low",
    "Medium",
    "High"
]


cm = confusion_matrix(

    y_test,

    y_pred,

    labels=labels

)


# =========================================================
# PRINT PERFORMANCE
# =========================================================

print()
print("=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print()

print(
    f"Accuracy  : {accuracy * 100:.2f}%"
)

print(
    f"Precision : {precision * 100:.2f}%"
)

print(
    f"Recall    : {recall * 100:.2f}%"
)

print(
    f"F1 Score  : {f1 * 100:.2f}%"
)


print()
print("Confusion Matrix:")

print(cm)


print()
print("Classification Report:")

print(
    classification_report(

        y_test,

        y_pred,

        labels=labels,

        zero_division=0

    )
)


# =========================================================
# FEATURE IMPORTANCE
# =========================================================

print()
print("=" * 60)
print("FEATURE IMPORTANCE")
print("=" * 60)

importance = pd.DataFrame({

    "Feature": features,

    "Importance": model.feature_importances_

})


importance = importance.sort_values(

    by="Importance",

    ascending=False

)


print()

print(
    importance.to_string(index=False)
)


# =========================================================
# SAVE COMPLETE MODEL PACKAGE
# =========================================================

model_package = {

    "model": model,

    "water_encoder": None,

    "flood_encoder": None,

    "water_quality_map": water_quality_map,

    "flood_map": flood_map,

    "features": features,

    "metrics": {

        "accuracy": accuracy,

        "precision": precision,

        "recall": recall,

        "f1_score": f1

    },

    "confusion_matrix": cm,

    "labels": labels,

    "feature_importance": importance.to_dict(
        orient="records"
    )

}


joblib.dump(

    model_package,

    MODEL_PATH

)


# =========================================================
# FINISH
# =========================================================

print()
print("=" * 60)
print("MODEL SAVED SUCCESSFULLY!")
print("=" * 60)

print()

print("Model location:")

print(MODEL_PATH)

print()

print(
    "JEEVAN-ALERT AI training completed successfully!"
)

print()