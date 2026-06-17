from fastapi import APIRouter
router = APIRouter()
@router.post("/predict")
def predict(): return {"status": "success", "prediction": 0.99}
