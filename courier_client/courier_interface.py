from abc import ABC, abstractmethod


class CourierABC(ABC):
    @abstractmethod
    def create_waybill(self, data: dict) -> dict:
        pass

    @abstractmethod
    def print_waybill_label(self, waybill_id: str) -> bytes:
        pass

    @abstractmethod
    def track_shipment_status(self, waybill_id: str) -> str:
        pass

    def map_statuses(self, waybill_id: str) -> dict:
        pass

    def cancel_shipment(self, waybill_id: str) -> bool:
        pass
