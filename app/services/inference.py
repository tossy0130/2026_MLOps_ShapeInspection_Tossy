from __future__ import annotations

from typing import List

import pandas as pd

from app.model_runtime import runtime
from app.schemas import ClusterFeature, ClusterPrediction

FEATURE_COLUMNS = [
    "areaCells",
    "perimeter",
    "aspect",
    "elong",
    "oriented_fill",
    "eccentricity",
    "circularity",
    "avgY",
    "avgHue",
    "avgC255",
    "avgNegi03",
    "avgNegi05",
    "avgS255",
    "bbox_w",
    "bbox_h",
    "centroid_x",
    "centroid_y",
]

def predict_clusters(clusters: List[ClusterFeature]) -> List[ClusterPrediction]:
    rows = [c.model_dump() for c in clusters]
    df = pd.DataFrame(rows)
    
    for col in FEATURE_COLUMNS:
        if col not in df.columns:
            df[col] = None
            
    
    df = df[FEATURE_COLUMNS].copy()
    df = df.fillna(0)
    
    if hasattr(runtime.model, "predict_proba"):
        proba = runtime.model.predict_proba(df)[:, 1]
        labels = (proba >= 0.5).astype(int)
        scores = proba.tolist()
    elif hasattr(runtime.model, "predict_with_score"):
        labels, scores = runtime.model.predict_with_score(df.to_dict(orient="records"))
    else:
        labels = runtime.model.predict(df)
        scores = [float(x) for x in labels]
        
    return [
        ClusterPrediction(
            cluster_id=clusters[i].cluster_id,
            label=int(labels[i]),
            score_ng=float(scores[i]),
        )
        for i in range(len(clusters))
    ]