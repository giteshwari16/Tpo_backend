import json
from pathlib import Path
from typing import Optional, Dict, Any

import joblib

MODEL_DIR = Path(__file__).resolve().parent
MODEL_PATH = MODEL_DIR / 'fatigue_model.joblib'
META_PATH = MODEL_DIR / 'fatigue_model.meta.json'

_cached_model = None
_cached_meta: Optional[Dict[str, Any]] = None


def get_model():
    global _cached_model, _cached_meta
    if _cached_model is None and MODEL_PATH.exists():
        _cached_model = joblib.load(MODEL_PATH)
    if _cached_meta is None and META_PATH.exists():
        _cached_meta = json.loads(META_PATH.read_text(encoding='utf-8'))
    return _cached_model, _cached_meta


def predict(payload: Dict[str, float]) -> Optional[str]:
    model, meta = get_model()
    if not model or not meta:
        return None
    features = meta.get('features') or []
    X = [[float(payload.get(f, 0.0)) for f in features]]
    pred = model.predict(X)[0]
    if isinstance(pred, (list, tuple)):
        return pred[0]
    return str(pred)
