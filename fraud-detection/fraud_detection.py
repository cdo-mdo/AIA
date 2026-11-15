"""Detect credit card fraud using a PyOD AutoEncoder."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pyod.models.auto_encoder import AutoEncoder
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    average_precision_score,
    classification_report,
    confusion_matrix,
    precision_recall_curve,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


SEED = 42
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "creditcard.csv"
RESULTS_DIR = BASE_DIR / "results"


def main():
    """Load data, train the detector, and evaluate held-out transactions."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(DATA_PATH)

    if "Class" not in data.columns:
        raise ValueError("The dataset must contain a 'Class' column.")

    # Remove exact duplicate records before creating independent splits.
    data = data.drop_duplicates()

    if data.isna().any().any():
        raise ValueError("Handle missing values before training.")

    if set(data["Class"].unique()) != {0, 1}:
        raise ValueError("Expected Class labels 0 and 1.")

    # Never include the target label among the model's input features.
    X = data.drop(columns="Class")
    y = data["Class"].astype(int)

    # Reserve 20% for final testing.
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=SEED
    )

    # Overall proportions: 60% training, 20% validation, 20% testing.
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val,
        y_train_val,
        test_size=0.25,
        stratify=y_train_val,
        random_state=SEED,
    )

    # Learn normal transaction patterns using only normal training examples.
    X_train_normal = X_train.loc[y_train == 0]

    # Fit preprocessing only on training data to avoid data leakage.
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_normal).astype(np.float32)
    X_val_scaled = scaler.transform(X_val).astype(np.float32)
    X_test_scaled = scaler.transform(X_test).astype(np.float32)

    model = AutoEncoder(
        hidden_neuron_list=[16, 8],
        epoch_num=20,
        batch_size=256,
        lr=0.001,
        dropout_rate=0.1,
        preprocessing=False,  # Scaling has already been applied.
        contamination=0.01,
        random_state=SEED,
        device="cpu",
        verbose=1,
    )
    model.fit(X_train_scaled)

    # Higher scores indicate more unusual transactions.
    val_scores = model.decision_function(X_val_scaled)

    # Select the threshold using validation labels, never test labels.
    precision, recall, thresholds = precision_recall_curve(y_val, val_scores)
    f1_scores = (
        2 * precision[:-1] * recall[:-1]
        / np.maximum(precision[:-1] + recall[:-1], 1e-12)
    )
    threshold = float(thresholds[np.argmax(f1_scores)])

    test_scores = model.decision_function(X_test_scaled)
    predictions = (test_scores >= threshold).astype(int)

    report = classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=["Normal", "Fraud"],
        digits=4,
        zero_division=0,
    )

    summary = (
        f"Transactions after removing duplicates: {len(data):,}\n"
        f"Normal training transactions: {len(X_train_normal):,}\n"
        f"Validation transactions: {len(X_val):,}\n"
        f"Test transactions: {len(X_test):,}\n"
        f"Selected threshold: {threshold:.6f}\n"
        f"Test ROC-AUC: {roc_auc_score(y_test, test_scores):.4f}\n"
        f"Test average precision: "
        f"{average_precision_score(y_test, test_scores):.4f}\n\n"
        f"{report}"
    )

    print(summary)
    (RESULTS_DIR / "metrics.txt").write_text(summary, encoding="utf-8")

    matrix = confusion_matrix(y_test, predictions, labels=[0, 1])
    display = ConfusionMatrixDisplay(
        confusion_matrix=matrix,
        display_labels=["Normal", "Fraud"],
    )
    display.plot(cmap="Blues", values_format="d")
    plt.title("PyOD AutoEncoder: Test Confusion Matrix")
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "confusion_matrix.png", dpi=200)
    plt.close()


if __name__ == "__main__":
    main()
