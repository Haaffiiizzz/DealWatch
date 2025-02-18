from pydantic import BaseModel


class LinkData(BaseModel):
    url: str

class SearchData(BaseModel):
    userSearch: str
    description: str = None