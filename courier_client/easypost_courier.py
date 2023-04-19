import easypost

from config import EASYPOST_API_KEY
from courier_client.courier_interface import CourierABC
from schema.waybill import WaybillRequestSchema
from utils.custom_enums import WaybillStatusEnum
from typing import Optional

easypost.api_key = EASYPOST_API_KEY


class EasyPostCourier(CourierABC):
    def create_waybill(self, waybill: WaybillRequestSchema):
        """
        Create a waybill for a shipment using EasyPost API.
        Args:
            waybill (WaybillRequestSchema): The waybill information as a Pydantic model instance.
        Returns:
            dict: A dictionary containing the waybill ID and the label URL.
        """
        waybill = waybill.dict()
        # Create shipment object and buy the lowest rate
        shipment = easypost.Shipment.create(
            to_address=waybill.get("to_address"),
            from_address=waybill.get("from_address"),
            parcel=waybill.get("parcel")
        )
        shipment.buy(rate=shipment.lowest_rate())
        # Return the waybill ID and label URL
        return {"waybill_id": shipment.id, "label_url": shipment.postage_label.label_url, "status": shipment.status}

    def print_waybill_label(self, waybill_id: str) -> dict:
        """
        Retrieve the label URL for a previously created waybill using EasyPost API.
        Args:
            waybill_id (str): The ID of the waybill to retrieve the label URL for.
        Returns:
            dict: A dictionary containing the waybill ID and the label URL.
        """
        return {
            "waybill_id": waybill_id,
            "label_url": easypost.Shipment.retrieve(waybill_id).postage_label['label_url']
        }

    def track_shipment_status(self, waybill_id: str) -> dict:
        """
        Retrieve the shipment status for a previously created waybill using EasyPost API.
        Args:
            waybill_id (str): The ID of the waybill to retrieve the shipment status for.
        Returns:
            dict: A dictionary containing the waybill ID and the shipment status.
        """
        return {"waybill_id": waybill_id, "status": easypost.Shipment.retrieve(waybill_id).status}

    def cancel_shipment(self, waybill_id: str) -> dict:
        """
        Cancel a previously created waybill using EasyPost API.
        Args:
            waybill_id (str): The ID of the waybill to cancel.
        Returns:
            bool: A boolean indicating whether the waybill was successfully cancelled.
        """
        easypost.Shipment.retrieve(waybill_id).refund()
        return {"waybill_id": waybill_id, "cancellation_status": True}

    def map_status(status: Optional[str]) -> WaybillStatusEnum:
        if status is None:
            return WaybillStatusEnum.unknown

        status = status.lower()

        if status == "created":
            return WaybillStatusEnum.created
        elif status == "purchased":
            return WaybillStatusEnum.purchased
        elif status == "label_generated":
            return WaybillStatusEnum.label_generated
        elif status == "shipped":
            return WaybillStatusEnum.shipped
        elif status == "delivered":
            return WaybillStatusEnum.delivered
        elif status == "returned":
            return WaybillStatusEnum.returned
        elif status == "cancelled":
            return WaybillStatusEnum.cancelled
        elif status == "error":
            return WaybillStatusEnum.error
        else:
            return WaybillStatusEnum.unknown


easypost_obj = EasyPostCourier()
