"""
Order CRUD routes.

"""
from microcosm.api import binding
from microcosm_flask.conventions.base import EndpointDefinition
from microcosm_flask.conventions.crud import configure_crud
from microcosm_flask.operations import Operation
from microcosm_postgres.context import transactional

from charmander.resources.order_resources import NewOrderSchema, OrderSchema, SearchOrderSchema


@binding("order_routes")
def configure_order_routes(graph):
    controller = graph.order_controller
    mappings = {
        Operation.Create: EndpointDefinition(
            func=transactional(controller.create),
            request_schema=NewOrderSchema(),
            response_schema=OrderSchema(),
        ),
        Operation.Retrieve: EndpointDefinition(
            func=controller.retrieve,
            response_schema=OrderSchema(),
        ),
        Operation.Search: EndpointDefinition(
            func=controller.search,
            request_schema=SearchOrderSchema(),
            response_schema=OrderSchema(),
        ),
    }
    configure_crud(graph, controller.ns, mappings)
    return controller.ns
