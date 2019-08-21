"""
Topping controller.

"""
from microcosm.api import binding
from microcosm_flask.conventions.crud_adapter import CRUDStoreAdapter
from microcosm_flask.namespaces import Namespace

from charmander.models.topping_model import Topping


@binding("topping_controller")
class ToppingController(CRUDStoreAdapter):

    def __init__(self, graph):
        super().__init__(graph, graph.topping_store)

        self.ns = Namespace(
            subject=Topping,
            version="v1",
        )
