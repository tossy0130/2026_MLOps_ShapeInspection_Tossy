from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

from app.settings import settings

# from common import (
from app.common import (
    FEATURE_COLUMNS,
    RULE_LABEL_COL,
    find_csv_files,
    load_dataset_from_csvs,
    prepare_rule_training_data,
    summarize_dataframe,
)


def main() -> None:
    print("=== train_rule_model.py start ===")
    print(f"[INFO] dataset_dir = {settings.dataset_dir}")
    print(f"[INFO] models_dir  = {settings.models_dir}")
    
    csv_paths = find_csv_files(settings.dataset_dir)
    if not csv_paths:
        raise FileNotFoundError(
            f"CSVファイルが見つかりません: {settings.dataset_dir}"
        )
        
    print(f"[INFO] csv_files = {len(csv_paths)}")
    
    for p in csv_paths[:10]:
        print(f"  - {p}")
    
    if len(csv_paths) > 10:
        print("  ...")
        
    df = load_dataset_from_csvs(csv_paths)
    
    print("[INFO] raw dataframe summary")
    print(summarize_dataframe(df))
    
    x, y, cleaned_df = prepare_rule_training_data(
        df=df,
        feature_columns=FEATURE_COLUMNS,
        label_col=RULE_LABEL_COL,
    )
    
    print(f"[INFO] usable_rows = {len(x)}")
    print(f"[INFO] label_counts = {dict(Counter(y))}")
    
    if len(x) < 10:
        raise ValueError(
            "学習データが少なすぎます。まずはCSV件数を増やしてください。"
        )
        
    unique_labels = sorted(y.unique().tolist())
    if len(unique_labels) < 2:
        raise ValueError(
             f"label_rule_current のクラスが1種類しかありません: {unique_labels}"
        )
        
    x_train, x_test, y_train, y_test, idx_train, idx_test = train_test_split(
        x,
        y,
        cleaned_df.index,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )
    
    
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=1,
        class_weight="balanced",
    )
    
    model.fit(x_train, y_train)
    
    y_pred = model.predict(x_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"\n[RESULT] accuracy = {acc:.4f}\n")
    print("[RESULT] confusion matrix")
    print(confusion_matrix(y_test, y_pred))
    
    print("\n[RESULT] classification report")
    print(classification_report(y_test, y_pred, digits=4))

    importance_df = pd.DataFrame(
        {
            "feature": FEATURE_COLUMNS,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)
    
    print("\n[RESULT] feature importances")
    print(importance_df.to_string(index=False))

    # model_runtime.py に合わせて、モデル本体をそのまま保存
    model.name = "rule-random-forest-v1"
    joblib.dump(model, settings.current_model_path)
    print(f"\n[SAVED] current model: {settings.current_model_path}")

    meta = {
        "model_name": model.name,
        "model_type": "RandomForestClassifier",
        "label_col": RULE_LABEL_COL,
        "feature_columns": FEATURE_COLUMNS,
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
        "accuracy": float(acc),
        "csv_file_count": int(len(csv_paths)),
        "source_dataset_dir": str(settings.dataset_dir),
    }
    
    settings.current_model_meta_path.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[SAVED] current model meta: {settings.current_model_meta_path}")

    # 参考出力
    importance_csv_path = settings.models_dir / "rule_model_feature_importances.csv"
    importance_df.to_csv(importance_csv_path, index=False, encoding="utf-8-sig")
    print(f"[SAVED] feature importances: {importance_csv_path}")
    
    eval_df = x_test.copy()
    eval_df["y_true"] = y_test.values
    eval_df["y_pred"] = y_pred

    raw_eval_df = cleaned_df.loc[idx_test].copy()
    raw_eval_df = raw_eval_df.reset_index(drop=True)
    eval_df = eval_df.reset_index(drop=True)

    merged_eval_df = pd.concat([raw_eval_df, eval_df[["y_true", "y_pred"]]], axis=1)

    eval_csv_path = settings.models_dir / "rule_model_eval_samples.csv"
    merged_eval_df.to_csv(eval_csv_path, index=False, encoding="utf-8-sig")
    print(f"[SAVED] eval samples: {eval_csv_path}")

    print("\n=== train_rule_model.py done ===")
    
if __name__ == '__main__' :
    main()