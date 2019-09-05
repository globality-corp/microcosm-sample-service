"""
Order Event Factory.

"""
from microcosm.api import binding
from microcosm_eventsource.factory import EventFactory, EventInfo
from microcosm_flask.namespaces import Namespace
from microcosm_logging.decorators import logger

from charmander.models.order_event_model import OrderEvent
from charmander.models.order_event_type import OrderEventType


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

    def create_event(self, event_info,  **kwargs):
        super().create_event(event_info, **kwargs)
        if event_info.event_type == OrderEventType.OrderDeliveryDetailsAdded:
            self.set_order_submitted(event_info)

    def set_order_submitted(self, event_info):
        submitted_info = EventInfo(
            ns=event_info.ns,
            sns_producer=event_info.sns_producer,
            event_type=OrderEventType.OrderSubmitted,
            parent=event_info.event,
        )
        self.create_transition(
            submitted_info,
            order_id=submitted_info.parent.order_id,
        )
