from fastapi import APIRouter

from app.schemas import InspectFeaturesRequest, InspectFeaturesResponse
from app.services.dataset_writer import append_request_to_dataset_csv
from app.services.inference import predict_clusters
from app.model_runtime import runtime

router = APIRouter(prefix="/inspect", tags=["inspect"])


@router.post("/features", response_model=InspectFeaturesResponse)
def inspect_features(req: InspectFeaturesRequest) -> InspectFeaturesResponse:
    append_request_to_dataset_csv(req)
    predictions = predict_clusters(req.clusters)
    
    return InspectFeaturesResponse(
        request_id=req.request_id,
        model_name=runtime.model_name,
        cluster_count=len(req.clusters),
        predictions=predictions,
    )