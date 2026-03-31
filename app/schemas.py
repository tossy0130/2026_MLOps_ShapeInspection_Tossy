from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ClusterFeature(BaseModel):
    cluster_id: int
    areaCells: int
    perimeter: int
    aspect: float
    elong: float
    oriented_fill: Optional[float] = None
    eccentricity: float
    circularity: float
    avgY: float
    avgHue: float
    avgC255: float
    avgNegi03: float
    avgNegi05: float
    avgS255: float
    bbox_min_x: Optional[int] = None
    bbox_min_y: Optional[int] = None
    bbox_max_x: Optional[int] = None
    bbox_max_y: Optional[int] = None
    bbox_w: Optional[int] = None
    bbox_h: Optional[int] = None
    centroid_x: Optional[float] = None
    centroid_y: Optional[float] = None
    
class InspectFeaturesRequest(BaseModel):
    request_id: str
    source: str = "trasum-local"
    preset_name: Optional[str] = None
    image_name: Optional[str] = None
    image_path: Optional[str] = None
    inspected_at: Optional[str] = None
    meta: Dict[str, Any] = Field(default_factory=dict)
    clusters: List[ClusterFeature]
    
class ClusterPrediction(BaseModel):
    cluster_id: int
    label: int
    score_ng: float
    
class InspectFeaturesResponse(BaseModel):
    request_id: str
    model_name: str
    cluster_count: int
    predictions: List[ClusterPrediction]
    
class HealthResponse(BaseModel):
    status: str
    app: str
    model_loaded: bool
        
