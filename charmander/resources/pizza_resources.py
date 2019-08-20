"""
Pizza resources.

"""
from marshmallow import Schema, fields
from microcosm_flask.fields import EnumField
from microcosm_flask.linking import Link, Links
from microcosm_flask.namespaces import Namespace
from microcosm_flask.operations import Operation
from microcosm_flask.paging import PageSchema

from charmander.models.pizza_model import CrustType, Pizza, PizzaSize


class NewPizzaSchema(Schema):
    customerId = fields.UUID(required=True, attribute="customer_id")
    size = EnumField(PizzaSize)
    crustType = EnumField(CrustType, attribute="crust_type")


class PizzaSchema(NewPizzaSchema):
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
                subject=Pizza,
                version="v1",
            ),
            pizza_id=obj.id,
        )
        return links.to_dict()


class SearchPizzaSchema(PageSchema):
    customer_id = fields.UUID()
    crust_type = EnumField(CrustType)
    size = EnumField(PizzaSize)