"""
Order Event Factory.

"""
from microcosm.api import binding
from microcosm_eventsource.factory import EventFactory
from microcosm_flask.namespaces import Namespace
from microcosm_logging.decorators import logger

from charmander.models.order_event_model import OrderEvent


@binding("order_event_factory")
@logger
class OrderEventFactory(EventFactory):

    def __init__(self, graph):
        super().__init__(
            event_store=graph.order_event_store,
            identifier_key="order_event_id",
            default_ns=Namespace(
                subject=OrderEvent,
                version="v1",
            ),
        )
