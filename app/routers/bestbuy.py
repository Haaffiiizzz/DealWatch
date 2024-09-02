from fastapi import APIRouter

router = APIRouter(prefix = "/bestbuy", tags= ["BestBuy"]) 

@router.get("/")
def root():
    print("BestBuy has been sent.")
    return "BestBuy"
