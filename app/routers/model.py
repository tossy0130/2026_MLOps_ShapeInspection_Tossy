from fastapi import APIRouter

from app.model_runtime import runtime

router = APIRouter(prefix="/model", tags=["model"])


@router.get("/current")
def get_current_model():
    return {
        "model_name": runtime.model_name,
        "loaded_from": runtime.loaded_from,
        "is_model_loaded": runtime.is_model_loaded,
    }