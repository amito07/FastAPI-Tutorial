from pydantic import BaseModel


class ImageParameter(BaseModel):
    url: str
    path: str

class ParameterModel(BaseModel):
    name: str
    email: str
    image_info: ImageParameter