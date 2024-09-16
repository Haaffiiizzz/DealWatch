from fastapi import APIRouter

router = APIRouter(tags= ["User"])

@router.get("/users")
def root():
    return "Users page" 