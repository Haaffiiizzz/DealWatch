from pydantic import BaseModel
from typing import Dict, Any


class LinkData(BaseModel):
    url: str

class SearchData(BaseModel):
    userSearchTerm: str
    userDescription: str = None

class Wishlist(BaseModel):
    wishlistURL : str
    
class WishlistItem(BaseModel):
    item: Dict[str, Any]
    
class ItemData(BaseModel):
    itemLink: str
    site: str
    
class ItemSearch(BaseModel):
    item: Dict[str, Any]
    site: str