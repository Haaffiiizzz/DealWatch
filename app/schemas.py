from pydantic import BaseModel
from typing import Dict, Any


class LinkData(BaseModel):
    url: str

class SearchData(BaseModel):
    userSearch: str
    description: str = None

class Wishlist(BaseModel):
    wishlistURL : str
    
class WishlistItem(BaseModel):
    item: Dict[str, Any]