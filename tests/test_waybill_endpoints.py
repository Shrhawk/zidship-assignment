import easypost
import pytest
from sqlalchemy.orm import Session

from config import EASYPOST_API_KEY
from courier_client.easypost_courier import easypost_obj
from tests.database import get_test_db
from models import WaybillModel, CourierModel, PackageModel, AddressModel

easypost.api_key = EASYPOST_API_KEY


@pytest.fixture
def db_session():
    yield from get_test_db()


def test_create_waybill(db_session: Session, client):
    # Test the creation of a waybill
    courier = CourierModel(name="EasyPost")
    db_session.add(courier)
    db_session.commit()
    waybill_data = {
        "to_address": {
            "name": "easypost",
            "street1": "179 N Harbor Dr",
            "city": "Redondo Beach",
            "state": "CA",
            "zip": "90277",
            "type": "sender",
            "phone": "+923228095217"
        },
        "from_address": {
            "name": "Hassan Raza",
            "street1": "417 Montgomery Street",
            "street2": "5th Floor",
            "city": "San Francisco",
            "state": "CA",
            "zip": "54775",
            "type": "receiver",
            "phone": "+4153334444"
        },
        "parcel": {
            "weight": 10,
            "length": 10,
            "width": 10,
            "height": 10
        }
    }
    response = client.post("/api/v1/easypost/waybill", json=waybill_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["id"]
    assert response_data["label_url"]
    assert response_data["status"] == "unknown"


def test_print_waybill_label(db_session: Session, client):
    # Test the retrieval of a waybill label
    courier = CourierModel(name="test")
    db_session.add(courier)
    package = PackageModel(**{
        "weight": 10,
        "length": 10,
        "width": 10,
        "height": 10
    })
    db_session.add(package)
    db_session.flush()
    waybill = WaybillModel(
        courier_id=courier.id,
        label_url="https://some.label/url",
        status="label_created",
        package_id=package.id
    )
    receiver_address = AddressModel(**{
        "name": "easypost",
        "street1": "179 N Harbor Dr",
        "city": "Redondo Beach",
        "state": "CA",
        "zip": "90277",
        "type": "sender",
        "phone": "+923228095217"
    })
    sender_address = AddressModel(**{
        "name": "Hassan Raza",
        "street1": "417 Montgomery Street",
        "street2": "5th Floor",
        "city": "San Francisco",
        "state": "CA",
        "zip": "54775",
        "type": "receiver",
        "phone": "+4153334444"
    })
    db_session.add(waybill)
    db_session.flush()
    receiver_address.waybill_id, sender_address.waybill_id = waybill.id, waybill.id
    db_session.add_all([sender_address, receiver_address])
    db_session.commit()
    response = client.get(f"/api/v1/easypost/waybill/label?waybill_id={waybill.id}")
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["id"] == waybill.id
    assert response_data["label_url"] == waybill.label_url
    assert response_data["status"] == waybill.status


def test_track_status():
    # Test the tracking of a shipment status
    waybill_id = "some_waybill_id"

    with pytest.raises(easypost.Error):
        easypost_obj.track_shipment_status(waybill_id)


def test_cancel_shipment():
    # Test the cancellation of a shipment
    waybill_id = "some_waybill_id"

    with pytest.raises(easypost.Error):
        easypost_obj.cancel_shipment(waybill_id)
