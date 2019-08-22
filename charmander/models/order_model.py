"""
Order model.

"""
from microcosm_postgres.models import Model, UnixTimestampEntityMixin
from microcosm_postgres.types import EnumType
from sqlalchemy import Column
from sqlalchemy_utils import UUIDType

from charmander.enums import Purpose, Resolution


class Order(UnixTimestampEntityMixin, Model):
    """
    A container for proposal events and versions.

    It should be created after the client reveals the project brief and their identity.

    """
    __tablename__ = "order"

    customer_id = Column(UUIDType, nullable=False, unique=True)
    purpose = Column(
            EnumType(Purpose),
            default=Purpose.NORMAL,
            nullable=False
    )
    resolution = Column(
        EnumType(Resolution),
        default=Resolution.ACTIVE,
        nullable=False,
    )

    __table_args__ = (
        # Put cool constraints in here
    )
