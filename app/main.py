from fastapi import FastAPI, APIRouter
from .routers import amazon, bestbuy 
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
router = APIRouter()

origins = [
   "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@router.get("/")
def root():
    return "Hello"

app.include_router(router)
app.include_router(amazon.router)
app.include_router(bestbuy.router)

