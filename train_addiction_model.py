"""
train_addiction_model.py
Dataset  : ./datasets/mobile_addiction_data.csv
Model    : DecisionTreeClassifier
Output   : ./models/addiction_model.pkl
"""

import joblib

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

from preprocess import (
    load,
    basic_clean,
    encode_labels,
    normalize,
    save_clean
)

# ── CONFIGURABLE ──────────────────────────────────────────────
DATASET_PATH = "./datasets/mobile_addiction_data.csv"
MODEL_OUT    = "./models/addiction_model.pkl"

TEST_SIZE    = 0.2
RANDOM_STATE = 42
# ──────────────────────────────────────────────────────────────


def train():

    print("[Addiction Model] Loading data ...")

    df = load("mobile_addiction_data.csv")

    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")

    df = basic_clean(df)

    # Correct target column
    target = "Self_Reported_Addiction_Level"

    print(f"  Target column -> '{target}'")

    # Encode non-target categorical columns
    df, _ = encode_labels(df, exclude=[target])

    # Encode target column separately
    le_target = LabelEncoder()

    df[target] = le_target.fit_transform(
        df[target].astype(str)
    )

    # Normalize features
    df = normalize(df, exclude=[target])

    # Save cleaned dataset
    save_clean(df, "mobile_addiction_clean.csv")

    # Split features & target
    X = df.drop(columns=[target])

    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE
    )

    # Train model
    clf = DecisionTreeClassifier(
        random_state=RANDOM_STATE,
        max_depth=10
    )

    clf.fit(X_train, y_train)

    # Accuracy
    train_acc = accuracy_score(
        y_train,
        clf.predict(X_train)
    )

    test_acc = accuracy_score(
        y_test,
        clf.predict(X_test)
    )

    print(f"  Train accuracy : {train_acc:.4f}")
    print(f"  Test accuracy  : {test_acc:.4f}")

    # Save model
