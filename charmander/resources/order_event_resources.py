"""
Order Event resources.

"""
from marshmallow import Schema, fields
from microcosm_eventsource.resources import EventSchema, SearchEventSchema
from microcosm_flask.fields import EnumField
from microcosm_flask.linking import Link, Links
from microcosm_flask.namespaces import Namespace
from microcosm_flask.operations import Operation

from charmander.enums import Purpose, Resolution
from charmander.models.order_event_model import OrderEvent
from charmander.models.order_event_type import OrderEventType
from charmander.models.order_model import Order
from charmander.models.pizza_model import CrustType, PizzaSize
from charmander.models.topping_model import ToppingType 


class SearchOrderEventSchema(SearchEventSchema):
    event_type = EnumField(
        ProposalEventType,
    )
    order_id = fields.UUID()
    customer_id = fields.UUID()
    pizza_size = EnumField(
        PizzaSize,
    )
    crust_type = EnumField(
        CrustType,
    )
    topping_type = EnumField(
        ToppingType,
    )
    purpose = EnumField(
        Purpose,
    )
    resolution = EnumField(
        Resolution,
    )


class NewOrderEventSchema(Schema):
    eventType = EnumField(
        OrderEventType,
        attribute="event_type",
        required=True,
    )
    customerId = fields.UUID(
        attribute="customer_id",
    )
    pizzaSize = EnumField(
        attribute="pizza_size",
    )
    crustType = EnumField(
        attribute="crust_type",
    )
    toppingType = EnumField(
        attribute="topping_type",
    )


class OrderEventSchema(NewProposalEventSchema, EventSchema):
    id = fields.UUID(
        required=True,
    )
    createdAt = fields.Float(
        attribute="created_at",
        required=True,
    )
    _links = fields.Method(
        "get_links",
        dump_only=True,
    )

    def get_links(self, obj):
        links = Links()
        links["self"] = Link.for_(
            Operation.Retrieve,
            Namespace(
                subject=OrderEvent,
                version="v1",
            ),
            order_event_id=obj.id,
        )
        links["parent:order"] = Link.for_(
            Operation.Retrieve,
            Namespace(
                subject=Order,
                version="v1",
            ),
            order_id=obj.order_id,
        )
        return links.to_dict()
