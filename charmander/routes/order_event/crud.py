"""
OrderEvent CRUD routes.

"""
from microcosm.api import binding
from microcosm_flask.conventions.base import EndpointDefinition
from microcosm_flask.conventions.crud import configure_crud
from microcosm_flask.operations import Operation
from microcosm_postgres.context import transactional

from charmander.resources.order_event_resources import NewOrderEventSchema, OrderEventSchema, SearchOrderEventSchema


@binding("order_event_routes")
def configure_proposal_event_routes(graph):
    controller = graph.v1_order_event_controller
    mappings = {
        Operation.Create: EndpointDefinition(
            func=transactional(controller.create),
            request_schema=NewOrderEventSchema(),
            response_schema=OrderEventSchema(),
        ),
        Operation.Retrieve: EndpointDefinition(
            func=controller.retrieve,
            response_schema=OrderEventSchema(),
        ),
        Operation.Search: EndpointDefinition(
            func=controller.search,
            request_schema=SearchOrderEventSchema(),
            response_schema=OrderEventSchema(),
        ),
    }
    configure_crud(graph, controller.ns, mappings)
    return controller.ns
