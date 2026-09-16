from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    sku: str
    name: str
    category: str


class ProductResponse(BaseModel):
    id: int
    sku: str
    name: str
    category: str

    model_config = ConfigDict(from_attributes=True)