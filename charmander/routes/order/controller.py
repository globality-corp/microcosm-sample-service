"""
Order controller.

"""
from microcosm.api import binding
from microcosm_flask.conventions.crud_adapter import CRUDStoreAdapter
from microcosm_flask.namespaces import Namespace

from charmander.models.order_model import Order
from charmander.models.order_event_type import OrderEventType


@binding("order_controller")
class OrderController(CRUDStoreAdapter):

    def __init__(self, graph):
        super().__init__(graph, graph.order_store)

        self.ns = Namespace(
            subject=Order,
            version="v1",
        )
        self.sns_producer = graph.sns_producer
        self.order_event_factory = graph.order_event_factory

    def create(self, **kwargs):
        order = super().create(**kwargs)

        self.order_event_factory.create(
            ns=None,
            sns_producer=self.sns_producer,
            order_id=order.id,
            event_type=OrderEventType.OrderInitialized,
        )

        return order
