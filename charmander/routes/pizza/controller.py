"""
Pizza controller.

"""
from microcosm.api import binding
from microcosm_flask.conventions.crud_adapter import CRUDStoreAdapter
from microcosm_flask.namespaces import Namespace

from charmander.models.pizza_model import Pizza


@binding("pizza_controller")
class PizzaController(CRUDStoreAdapter):

    def __init__(self, graph):
        super().__init__(graph, graph.pizza_store)

        self.ns = Namespace(
            subject=Pizza,
            version="v1",
        )
