from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

import pandas as pd


FEATURE_COLUMNS: List[str] = [
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

RULE_LABEL_COL = "label_rule_current"
RULE_LABEL_TEXT_COL = "label_rule_text"
TARGET_LABEL_COL = "target_label"
HUMAN_LABEL_COL = "label_human"
IS_REVIEWED_COL = "is_reviewed"
NG_REASON_PRIMARY_COL = "ng_reason_primary"

def find_csv_files(dataset_dir: Path) -> List[Path]:
    """
    dataset_dir 配下の CSV を再帰的に探す
    """
    if not dataset_dir.exists():
        return []
    return sorted(dataset_dir.rglob("*.csv"))

def load_dataset_from_csvs(csv_paths: List[Path]) -> pd.DataFrame:
    """
    複数CSVを結合して1つのDataFrameにする
    """
    if not csv_paths:
        raise FileNotFoundError("CSVファイルが見つかりません。")
    
    frames: List[pd.DataFrame] = []
    for path in csv_paths:
        df = pd.read_csv(path)
        df["__source_csv__"] = str(path)
        frames.append(df)
        
    return pd.concat(frames, ignore_index=True)

def prepare_rule_training_data(
    df:pd.DataFrame,
    feature_columns: List[str] | None = None,
    label_col: str = RULE_LABEL_COL,
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    """
    label_rule_current を目的変数として学習用データを作る
    戻り値:
      X, y, cleaned_df
    """
    features = feature_columns or FEATURE_COLUMNS
    
    missing_features = [c for c in features if c not in df.columns]
    if missing_features:
        raise ValueError(f"特徴量列が不足しています: {missing_features}")
    
    if label_col not in df.columns:
        raise ValueError("fラベル列が見つかりません: {label_col}")
    
    work = df.copy()
    
    # ラベル欠損の除外
    work = work[work[label_col].notna()].copy()
    
    # 数値化
    for c in features:
        work[c] = pd.to_numeric(work[c], errors = "coerce")
        
    work[label_col] = pd.to_numeric(work[label_col], errors="coerce")
    
    # 学習に必要な列に欠損がある行は除外
    work = work.dropna(subset=features + [label_col]).copy()
    
    work[label_col] = work[label_col].astype(int)
    
    x = work[features].copy()
    y = work[label_col].copy()
    
    return x, y, work

def summarize_dataframe(df: pd.DataFrame) -> str:
    lines: List[str] = []
    lines.append(f"rows={len(df)}")
    lines.append(f"columns={len(df.columns)}")
    lines.append(f"column_names={list(df.columns)}")
    
    return "¥n".join(lines)

