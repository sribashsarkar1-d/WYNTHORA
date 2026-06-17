from fastapi import APIRouter
router = APIRouter()
@router.post("/train")
def train(): return {"status": "training started"}
