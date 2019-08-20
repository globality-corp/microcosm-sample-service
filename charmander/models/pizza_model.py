from collections import namedtuple
from enum import unique, Enum

from microcosm_postgres.models import EntityMixin, Model
from microcosm_postgres.types import EnumType
from sqlalchemy import Column, String
from sqlalchemy_utils import UUIDType


PizzaSizeInfo = namedtuple(
    "PizzaSizeInfo",
    [
        "value",
        "description",
    ],
)


@unique
class PizzaSize(Enum):
    def __str__(self):
        return self.name

    PERSONAL = PizzaSizeInfo(
        "PERSONAL",
        "A nice pizza for 1, maybe 1.5 people",
    )
    REGULAR = PizzaSizeInfo(
        "REGULAR",
        "The size you would expect a pizza to be. Nothing more, nothing less.",
    )
    LARGE = PizzaSizeInfo(
        "LARGE",
        "More than you need, but just as much as you want."
    )


@unique
class CrustType(Enum):
    def __str__(self):
        return self.name

    REGULAR = "REGULAR"
    CHEESE_STUFFED = "CHEESE_STUFFED"


class Pizza(EntityMixin, Model):
    """
    A  pizza
 
    """
    __tablename__ = "pizza"

    customer_id = Column(UUIDType, nullable=False)
    size = Column(EnumType(PizzaSize), nullable=False)
    crust_type = Column(EnumType(CrustType), nullable=False)
