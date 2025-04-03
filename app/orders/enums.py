from enum import Enum

class SendersEnum(Enum):
    USER = "user"
    COMPANY = "company"


class OrderStatusEnum(Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"
    FUCKED = "fucked"
