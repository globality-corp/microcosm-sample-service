from collections import namedtuple
from urllib.parse import urljoin

from microcosm.api import binding, defaults
from microcosm_logging.decorators import logger
from microcosm_pubsub.chain import Chain, assign, extracts
from microcosm_pubsub.conventions import created
from microcosm_pubsub.decorators import handles
from microcosm_pubsub.errors import Nack, SkipMessage
from microcosm_pubsub.handlers import ChainURIHandler
from requests import get, post

from charmander.models.order_event_type import OrderEventType


DeliveryEvent = namedtuple("DeliveryEvent", "id orderId eventType")


@binding("record_pizza_delivery")
@defaults(
    visibility_timeout_seconds=4,
)
@handles(created("DeliveryEvent.PizzaDelivered"))
@logger
class RecordPizzaDelivery(ChainURIHandler):
    """
    Handle creation DeliveryEvent.PizzaDelivered

    The recording of events coming in from pizza delivery couriers is handled by
    a separate system which publishes `DeliveryEvents`. When a pizza is
    delivered, this is the system that is notified, but it requires us to update
    our OrderEvent state machine to reflect the state change for end users.

    Delivery Event {
        id,
        orderId,
        eventType

    }
    """

    def __init__(self, graph):
        super().__init__(graph)
        self.charmander_url = "http://localhost:6999"
        self.visibility_timeout_seconds = graph.config.record_pizza_delivery.visibility_timeout_seconds

    def get_chain(self):
        return Chain(
            assign("delivery_event.orderId").to("order_id"),
            self.extract_order,
            assign("order.customerId").to("customer_id"),
            self.extract_latest_order_event,
            assign("latest_order_event.eventType").to("last_event_type"),
            self.assert_order_ready_for_fulfillment,
            self.create_order_fulfilled_event,
        )

    @property
    def resource_name(self):
        return "delivery_event"

    @property  # type: ignore
    def resource_type(self):
        return DeliveryEvent

    @extracts("order")
    def extract_order(self, order_id):
        return get(urljoin(self.charmander_url, "api/v1/order", str(order_id)))

    @extracts("latest_order_event")
    def extract_latest_order_event(self, order_id):
        return get(urljoin(self.charmander_url, "api/v1/order_event", str(order_id)))

    def assert_order_ready_for_fulfillment(self, last_event_type, order_id):
        # This is the desired case, be happy
        if last_event_type == OrderEventType.OrderSubmitted:
            return

        # Order already shows as submitted, this can happen as SQS has at least
        # once semantics and duplicate messages can be delivered
        if last_event_type == OrderEventType.OrderFulfilled:
            raise SkipMessage(f"Order {order_id} already fulfilled")

        # It might be taking some time for the submitted event to go through,
        # try gain
        raise Nack(self.visibility_timeout_seconds)

    def create_order_fulfilled_event(self, order_id, customer_id):
        post(
            url=urljoin(self.charmander_url, "api/v1/order_event"),
            data=dict(
                customerId=str(customer_id),
                orderId=str(order_id),
                eventType=OrderEventType.OrderFulfilled.name,
            ),
        )
        return True
