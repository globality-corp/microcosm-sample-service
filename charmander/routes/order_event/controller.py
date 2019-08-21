"""
OrderEvent controller.

"""
from microcosm.api import binding
from microcosm_eventsource.controllers import EventController
from microcosm_flask.namespaces import Namespace

from charmander.models.order_event_model import OrderEvent


@binding("v1_order_event_controller")
class OrderEventController(EventController):
    def __init__(self, graph):
        super(OrderEventController, self).__init__(graph, graph.order_event_store)

        self.ns = Namespace(
            subject=OrderEvent,
            version="v1",
        )

        self.order_store = graph.order_store
        self.order_event_factory = graph.order_event_factory

    @property
    def event_factory(self):
        return self.order_event_factory
