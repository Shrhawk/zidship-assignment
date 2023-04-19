from pydantic import BaseModel
from typing import Any, Optional

from utils.custom_enums import AddressEnum


class AddressSchema(BaseModel):
    name: str
    street1: str
    street2: Optional[str]
    city: str
    state: str
    zip: str
    phone: str
    type: AddressEnum

    class Config:
        orm_mode = True


class WaybillItem(BaseModel):
    name: str
    quantity: int
    weight: float


class ProductDimension(BaseModel):
    weight: float
    length: float
    width: float
    height: float

    class Config:
        orm_mode = True


class WaybillRequestSchema(BaseModel):
    to_address: AddressSchema
    from_address: AddressSchema
    parcel: ProductDimension


class WaybillResponseSchema(WaybillRequestSchema):
    id: str
    label_url: str
    status: str

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj: Any):
        for address in obj.addresses:
            if address.type == "sender":
                obj.to_address = address
                continue
            obj.from_address = address
        obj.parcel = obj.package
        obj.weight = obj.package.weight
        obj.length = obj.package.length
        obj.width = obj.package.width
        obj.height = obj.package.height
        return super().from_orm(obj)


class WaybillCancelSchema(BaseModel):
    cancel_reason: str
