"""
Topping resources.

"""
from marshmallow import Schema, fields
from microcosm_flask.fields import EnumField
from microcosm_flask.linking import Link, Links
from microcosm_flask.namespaces import Namespace
from microcosm_flask.operations import Operation
from microcosm_flask.paging import PageSchema

from charmander.models.order_model import Order
from charmander.models.pizza_model import Pizza
from charmander.models.topping_model import Topping, ToppingType


class NewToppingSchema(Schema):
    pizzaId = fields.UUID(required=True, attribute="pizza_id")
    orderId = fields.UUID(required=True, attribute="order_id")
    toppingType = EnumField(ToppingType, required=True, attribute="topping_type")


class ToppingSchema(NewToppingSchema):
    id = fields.UUID(
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
                subject=Topping,
                version="v1",
            ),
            topping_id=obj.id,
        )
        links["parent:pizza"] = Link.for_(
            Operation.Retrieve,
            Namespace(
                subject=Pizza,
                version="v1",
            ),
            pizza_id=obj.pizza_id,
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


class SearchToppingSchema(PageSchema):
    pizza_id = fields.UUID()
    order_id = fields.UUID()
    topping_type = EnumField(ToppingType)
