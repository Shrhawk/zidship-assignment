import enum


class WaybillStatusEnum(str, enum.Enum):
    created = "created"
    purchased = "purchased"
    label_generated = "label_generated"
    shipped = "shipped"
    delivered = "delivered"
    returned = "returned"
    cancelled = "cancelled"
    error = "error"
    unknown = "unknown"


class AddressEnum(str, enum.Enum):
    sender = "sender"
    receiver = "receiver"
