from pydantic import BaseModel, HttpUrl


class BannerResponse(BaseModel):
    """
    A Pydantic model representing a banner response.
    """

    name: str
    raw_location: HttpUrl
