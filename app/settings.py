from pathlib import Path
from pydantic import BaseModel


class AppSettings(BaseModel):
    app_name: str = "Negi Inspection FastAPI"
    base_dir: Path = Path(__file__).resolve().parent
    incoming_dir: Path = base_dir / "data" / "incoming"
    dataset_dir: Path = base_dir / "data" / "dataset"
    models_dir: Path = base_dir / "data" / "models"
    current_model_path: Path = models_dir / "current_model.joblib"
    current_model_meta_path: Path = models_dir / "current_model_meta.json"
    
settings = AppSettings()

for p in [settings.incoming_dir, settings.dataset_dir, settings.models_dir]:
    p.mkdir(parents=True, exist_ok=True)
    
    
    