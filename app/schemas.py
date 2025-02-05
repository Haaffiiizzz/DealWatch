from pydantic import BaseModel


class LinkData(BaseModel):
    url: str