from collections import namedtuple
from enum import Enum, unique

from microcosm_postgres.models import EntityMixin, Model
from microcosm_postgres.types import EnumType
from sqlalchemy import Column
from sqlalchemy_utils import UUIDType


@unique
class CrustType(Enum):
    def __str__(self):
        return self.name

    PEPPERONI = "PEPPERONI"
    MUSHROOM = "MUSHROOM" 
    ONION = "ONION" 
    SAUSAGE = "SAUSAGE" 
    BACON = "BACON" 
    OLIVE = "OLIVE" 
    BELL_PEPPER = "BELL_PEPPER"
    PINEAPPLE = "PINEAPPLE"
    SPINACH = "SPINACH"
    FOUR_CHEESE = "FOUR_CHEESE" 


class Topping(EntityMixin, Model):
    """
    A  topping for a specific pizza

    """
    __tablename__ = "pizza"

    pizza_id = Column(
        UUIDType,
        ForeignKey("pizza.id"),
        nullable=False,
    )
    topping_type = Column(EnumType(ToppingType), nullable=False)
