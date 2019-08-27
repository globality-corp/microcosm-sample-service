"""
Order resources.

"""
from marshmallow import Schema, fields
from microcosm_flask.fields import EnumField
from microcosm_flask.linking import Link, Links
from microcosm_flask.namespaces import Namespace
from microcosm_flask.operations import Operation
from microcosm_flask.paging import PageSchema

from charmander.enums import Purpose, Resolution
from charmander.models.order_event_model import OrderEvent
from charmander.models.order_model import Order


class SearchOrderSchema(PageSchema):
    customer_id = fields.UUID()
    purpose = EnumField(
        enum=Purpose,
    )
    resolution = EnumField(
        enum=Resolution,
    )


class NewOrderSchema(Schema):
    customerId = fields.UUID(
        attribute="customer_id",
        required=True,
    )
    purpose = EnumField(
        Purpose,
    )


class OrderSchema(NewOrderSchema):
    id = fields.UUID(
        required=True,
    )
    resolution = EnumField(
        enum=Resolution,
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
                subject=Order,
                version="v1",
            ),
            order_id=obj.id,
        )
        links["child:events"] = Link.for_(
            Operation.Search,
            Namespace(
                subject=OrderEvent,
                version="v1",
            ),
            order_id=obj.id,
        )
        return links.to_dict()
