from fastapi import APIRouter

router = APIRouter(prefix = "/bestbuy", tags= ["BestBuy"]) 

@router.get("/")
def root():
    print("BestBuy sent.")
    return "BestBuy"
