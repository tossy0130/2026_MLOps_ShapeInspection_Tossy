from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Tuple

import joblib

from app.settings import settings

class DummyNegiModel:
    name = "rule-based-dummy"

    def predict_with_score(self, rows: list[dict]) -> Tuple[list[int], list[float]]:
        labels: list[int] = []
        scores: list[float] = []

        for r in rows:
            score = 0.0

            if r.get("areaCells", 0) >= 40:
                score += 0.25
            if r.get("avgC255", 999) <= 37.7:
                score += 0.25
            if r.get("elong", 0) >= 2.8:
                score += 0.20
            if r.get("eccentricity", 0) >= 0.95:
                score += 0.15
            if r.get("avgHue", 0) >= 155 and r.get("avgHue", 0) <= 185:
                score += 0.15

            score = max(0.0, min(1.0, score))
            label = 1 if score >= 0.5 else 0
            labels.append(label)
            scores.append(score)

        return labels, scores
    
    
class ModelRuntime:
    def __init__(self) -> None:
        self.model = DummyNegiModel()
        self.model_name = self.model.name
        self.loaded_from = "dummy"
        self.try_load_current_model()

    def try_load_current_model(self) -> None:
        model_path: Path = settings.current_model_path
        meta_path: Path = settings.current_model_meta_path

        if not model_path.exists():
            return

        try:
            self.model = joblib.load(model_path)
            self.model_name = getattr(self.model, "name", model_path.name)
            self.loaded_from = str(model_path)

            if meta_path.exists():
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                self.model_name = meta.get("model_name", self.model_name)
        except Exception:
            self.model = DummyNegiModel()
            self.model_name = self.model.name
            self.loaded_from = "dummy-fallback"

    @property
    def is_model_loaded(self) -> bool:
        return self.loaded_from != "dummy"
    
runtime = ModelRuntime()