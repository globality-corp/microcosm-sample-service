"""
OrderEvent model.

"""
from microcosm_eventsource.models import EventMeta
from microcosm_postgres.models import UnixTimestampEntityMixin
from microcosm_postgres.types import EnumType
from six import add_metaclass
from sqlalchemy import Column
from sqlalchemy_utils import UUIDType

from charmander.enums import Purpose, Resolution
from charmander.models.order_event_type import OrderEventType
from charmander.models.order_model import Order
from charmander.models.pizza_model import CrustType, PizzaSize
from charmander.models.topping_model import ToppingType


@add_metaclass(EventMeta)
class OrderEvent(UnixTimestampEntityMixin):
    """
    Order events, handles pizza and topping creation as well as order status.

    """
    __tablename__ = "order_event"
    __eventtype__ = OrderEventType
    __container__ = Order
    __unique_parent__ = False

    customer_id = Column(UUIDType, nullable=False)
    pizza_size = Column(EnumType(PizzaSize), nullable=True)
    crust_type = Column(EnumType(CrustType), nullable=True)
    topping_type = Column(EnumType(ToppingType), nullable=True)
    # denormalize from parent order to make searching easier
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

    __mapper_args__ = dict(
        polymorphic_on="event_type",
    )

    @classmethod
    def infer_event_type(cls):
        return cls.__mapper_args__["polymorphic_identity"]

    @property
    def edges(self):
        yield (self.order_id, self.id)
        if self.parent_id:
            yield (self.parent_id, self.id)


class OrderInitialized(OrderEvent):
    __mapper_args__ = {
        "polymorphic_identity": OrderEventType.OrderInitialized,
    }


class PizzaCreated(OrderEvent):
    __mapper_args__ = {
        "polymorphic_identity": OrderEventType.PizzaCreated,
    }


class PizzaToppingAdded(OrderEvent):
    __mapper_args__ = {
        "polymorphic_identity": OrderEventType.PizzaToppingAdded,
    }


class PizzaCustomizationFinished(OrderEvent):
    __mapper_args__ = {
        "polymorphic_identity": OrderEventType.PizzaCustomizationFinished,
    }


class OrderDeliveryDetailsAdded(OrderEvent):
    __mapper_args__ = {
        "polymorphic_identity": OrderEventType.OrderDeliveryDetailsAdded,
    }


class OrderSubmitted(OrderEvent):
    __mapper_args__ = {
        "polymorphic_identity": OrderEventType.OrderSubmitted,
    }


class OrderSatisfied(OrderEvent):
    __mapper_args__ = {
        "polymorphic_identity": OrderEventType.OrderSatisfied,
    }
