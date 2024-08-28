from fastapi import APIRouter

router = APIRouter(prefix = "/amazon", tags= ["Amazon"]) 

@router.get("/")
def root():
    print("Amazon sent.")
    return "Amazon"

