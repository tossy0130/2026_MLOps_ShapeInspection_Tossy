from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from app.settings import settings
from app.schemas import InspectFeaturesRequest


def append_request_to_dataset_csv(req: InspectFeaturesRequest) -> Path:
    rows = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    for c in req.clusters:
        row = c.model_dump()
        row.update(
            {
                "request_id": req.request_id,
                "source": req.source,
                "preset_name": req.preset_name,
                "image_name": req.image_name,
                "image_path": req.image_path,
                "inspected_at": req.inspected_at,
                "saved_at": now,
            }
        )
        rows.append(row)
        
    df = pd.DataFrame(rows)
    out_path = settings.dataset_dir / "incoming_features_log.csv"
    
    write_header = not out_path.exists()
    df.to_csv(out_path, mode="a", index=False, header=write_header, encoding="utf-8-sig")
    return out_path