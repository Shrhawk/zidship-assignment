import easypost
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config import EASYPOST_API_KEY
from courier_client.easypost_courier import easypost_obj
from db import get_db
from models import WaybillModel, CourierModel, PackageModel, AddressModel
from schema.waybill import WaybillRequestSchema, WaybillResponseSchema

easypost_router = APIRouter()

easypost.api_key = EASYPOST_API_KEY


@easypost_router.post("/waybill", response_model=WaybillResponseSchema)
def create_waybill(request: WaybillRequestSchema, db: Session = Depends(get_db)):
    courier = db.query(CourierModel).filter(CourierModel.name == "EasyPost").first()  # NoQa
    waybill = easypost_obj.create_waybill(request)
    if not waybill or not waybill.get("waybill_id"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Waybill not created"
        )
    waybill_obj = WaybillModel(
        id=waybill.get("waybill_id"),
        courier_id=courier.id,
        label_url=waybill.get("label_url"),
        status=waybill.get("status")
    )
    package_dimension = PackageModel(**request.parcel.dict())
    db.add(package_dimension)
    db.flush()
    waybill_obj.package_id = package_dimension.id
    db.add(waybill_obj)
    receiver_address = AddressModel(**request.to_address.dict())
    sender_address = AddressModel(**request.from_address.dict())
    receiver_address.waybill_id, sender_address.waybill_id = waybill.get("waybill_id"), waybill.get("waybill_id")
    db.add_all([sender_address, receiver_address])
    db.commit()
    return waybill_obj


@easypost_router.get("/waybill/label", response_model=WaybillResponseSchema)
def print_waybill_label(waybill_id: str, db: Session = Depends(get_db)):
    return db.query(WaybillModel).filter(WaybillModel.id == waybill_id).first()  # NoQa


@easypost_router.get("/waybill/status")
def track_status(waybill_id: str):
    return easypost_obj.track_shipment_status(waybill_id)


@easypost_router.get("/waybill/cancel")
def cancel_shipment(waybill_id: str):
    return easypost_obj.cancel_shipment(waybill_id)
