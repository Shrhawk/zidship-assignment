from sqlalchemy import Column, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship

from models.base import BaseModel
from utils.custom_enums import AddressEnum


class CourierModel(BaseModel):
    __tablename__ = 'courier'

    name = Column(String, nullable=False)
    waybill_obj = relationship("WaybillModel", back_populates="courier")


class PackageModel(BaseModel):
    __tablename__ = 'package'

    weight = Column(Float, nullable=True)
    length = Column(Float, nullable=True)
    width = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    waybill_obj = relationship("WaybillModel", back_populates="package")


class WaybillModel(BaseModel):
    __tablename__ = 'waybill'

    courier_id = Column(String, ForeignKey("courier.id"), nullable=False)
    courier = relationship("CourierModel", foreign_keys=[courier_id], back_populates="waybill_obj")  # NoQa
    package_id = Column(String, ForeignKey("package.id"), nullable=False)
    package = relationship("PackageModel", foreign_keys=[package_id], back_populates="waybill_obj")  # NoQa
    label_url = Column(String, nullable=True)
    status = Column(String, nullable=False)
    addresses = relationship("AddressModel", back_populates="waybill")


class AddressModel(BaseModel):
    __tablename__ = 'address'

    name = Column(String, nullable=False)
    street1 = Column(String, nullable=False)
    street2 = Column(String, nullable=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    type = Column(Enum(AddressEnum), nullable=False)
    waybill_id = Column(String, ForeignKey("waybill.id"), nullable=False)
    waybill = relationship("WaybillModel", foreign_keys=[waybill_id], back_populates="addresses")  # NoQa
