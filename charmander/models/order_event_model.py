"""
OrderEvent model.

"""
from microcosm_eventsource.models import EventMeta
from microcosm_postgres.models import UnixTimestampEntityMixin
from six import add_metaclass
from sqlalchemy import (
    CheckConstraint,
    Column,
    Index,
    String,
    or_,
    text,
)
from sqlalchemy_utils import UUIDType

from charmander.models.order_event_type import OrderEventType
from charmander.models.order_model import Order


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
