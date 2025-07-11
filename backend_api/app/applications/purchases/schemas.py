from pydantic import BaseModel


class PurchaseProductSchema(BaseModel):
    id: int
    title: str
    price: float
    main_image: str


class PurchaseSchema(BaseModel):
    product: PurchaseProductSchema
    created_at: str
