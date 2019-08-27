"""
Order controller.

"""
from microcosm.api import binding
from microcosm_flask.conventions.crud_adapter import CRUDStoreAdapter
from microcosm_flask.namespaces import Namespace

from charmander.models.order_model import Order


@binding("order_controller")
class OrderController(CRUDStoreAdapter):

    def __init__(self, graph):
        super().__init__(graph, graph.order_store)

        self.ns = Namespace(
            subject=Order,
            version="v1",
        )
