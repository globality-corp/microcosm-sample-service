"""
Order events persistence.

"""
from microcosm.api import binding
from microcosm_eventsource.stores import EventStore
from sqlalchemy.dialects.postgresql import insert

from charmander.models.order_event_model import OrderEvent
from charmander.models.order_model import Order


@binding("order_event_store")
class OrderEventStore(EventStore):

    def __init__(self, graph):
        super().__init__(
            graph,
            OrderEvent,
            auto_filter_fields=(
                OrderEvent.event_type,
                OrderEvent.order_id,
                OrderEvent.customer_id,
                OrderEvent.pizza_size,
                OrderEvent.crust_type,
                OrderEvent.topping_type,
                OrderEvent.purpose,
                OrderEvent.resolution,
            )
        )

    def _order_by(self, query, **kwargs):
        """
        Order events by logical clock.

        """
        return query.order_by(
            self.model_class.order_id.desc(),
            self.model_class.clock.desc(),
        )
