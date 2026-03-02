import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

# Default feature set based on user's dataset
DEFAULT_FEATURES: List[str] = [
    'sleep_score',
    'study_score',
    'social_media_score',
    'meals_score',
    'productivity_score_clean',
]

MODEL_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = MODEL_DIR.parents[1]
LOGS_DIR = PROJECT_ROOT / 'logs'
MODEL_PATH = MODEL_DIR / 'fatigue_model.joblib'
META_PATH = MODEL_DIR / 'fatigue_model.meta.json'

LOGS_DIR.mkdir(exist_ok=True, parents=True)
MODEL_DIR.mkdir(exist_ok=True, parents=True)


def train_from_csv(csv_path: str,
                   test_csv_path: Optional[str] = None,
                   features: Optional[List[str]] = None,
                   target_col: str = 'fatigue_level',
                   random_state: int = 42,
                   model_out: Path = MODEL_PATH,
                   meta_out: Path = META_PATH) -> dict:
    features = features or DEFAULT_FEATURES

    df = pd.read_csv(csv_path)
    for col in features + [target_col]:
        if col not in df.columns:
            raise ValueError(f'Missing column in training CSV: {col}')

    X = df[features]
    y = df[target_col]

    if test_csv_path and os.path.exists(test_csv_path):
        test_df = pd.read_csv(test_csv_path)
        for col in features + [target_col]:
            if col not in test_df.columns:
                raise ValueError(f'Missing column in test CSV: {col}')
        X_train, y_train = X, y
        X_test, y_test = test_df[features], test_df[target_col]
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=random_state, stratify=y
        )

    clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=random_state)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=False)

    # Persist
    joblib.dump(clf, model_out)
    meta = {
        'features': features,
        'target': target_col,
        'trained_at': datetime.utcnow().isoformat() + 'Z',
        'metrics': {
            'accuracy': acc
        }
    }
    with open(meta_out, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2)

    # Log
    log_path = LOGS_DIR / f"train_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f"Model saved to: {model_out}\n")
        f.write(f"Meta saved to: {meta_out}\n")
        f.write(f"Accuracy: {acc*100:.2f}%\n\n")
        f.write(report)

    return {
        'model_path': str(model_out),
        'meta_path': str(meta_out),
        'accuracy': acc,
        'report': report,
    }
