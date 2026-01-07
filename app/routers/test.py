from fastapi import APIRouter


router = APIRouter(
    prefix="/test",
    tags=["tests"],
)

@router.get("/")
def read_root():
    return {"Hello": "World"}