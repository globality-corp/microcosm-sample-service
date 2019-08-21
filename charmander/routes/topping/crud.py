"""
Topping CRUD routes.

"""
from microcosm.api import binding
from microcosm_flask.conventions.base import EndpointDefinition
from microcosm_flask.conventions.crud import configure_crud
from microcosm_flask.operations import Operation
from microcosm_postgres.context import transactional

from charmander.resources.topping_resources import (
    NewToppingSchema,
    ToppingSchema,
    SearchToppingSchema,
)


@binding("topping_routes")
def configure_pizza_routes(graph):
    controller = graph.pizza_controller
    mappings = {
        Operation.Create: EndpointDefinition(
            func=transactional(controller.create),
            request_schema=NewPizzaSchema(),
            response_schema=PizzaSchema(),
        ),
        Operation.Delete: EndpointDefinition(
            func=transactional(controller.delete),
        ),
        Operation.Retrieve: EndpointDefinition(
            func=controller.retrieve,
            response_schema=PizzaSchema(),
        ),
        Operation.Search: EndpointDefinition(
            func=controller.search,
            request_schema=SearchPizzaSchema(),
            response_schema=PizzaSchema(),
        ),
    }
    configure_crud(graph, controller.ns, mappings)
    return controller.ns
