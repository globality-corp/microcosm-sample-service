"""
Test handle creation of DeliveryEvent.PizzaDelivered and record as Order
Fulfilled

"""
from contextlib import contextmanager
from unittest.mock import patch

from hamcrest import (
    assert_that,
    calling,
    equal_to,
    is_,
    raises,
)
from microcosm_postgres.identifiers import new_object_id
from microcosm_pubsub.errors import Nack, SkipMessage

from charmander.daemon.handlers.record_pizza_delivery import DeliveryEvent
from charmander.daemon.main import CharmanderDaemon
from charmander.models.order_event_model import OrderEventType


@contextmanager
def mock_handler_actions():
    with patch(
        "charmander.daemon.handlers.record_pizza_delivery.get"
    ) as mock_get_resources:
        with patch(
            "charmander.daemon.handlers.record_pizza_delivery.post"
        ) as mock_create_event:
            yield mock_get_resources, mock_create_event


class TestRecordPizzaDelivery:
    def setup(self):
        self.graph = CharmanderDaemon.create_for_testing().graph
        self.handler = self.graph.record_pizza_delivery

        self.customer_id = new_object_id()
        self.delivery_event_id = new_object_id()
        self.order_id = new_object_id()
        self.delivery_event_type = "OrderDeliveredToDestination"

        self.message = dict(
            uri=f"https://deliveries.dev.globaltiy.io/api/v1/delivery_event/{self.delivery_event_id}"
        )
        self.delivery_event = DeliveryEvent(
            id=self.delivery_event_id,
            orderId=self.order_id,
            eventType=self.delivery_event_type,
        )
        self.order = dict(
            customerId=self.customer_id,
        )
        self.order_event = dict(
            eventType=OrderEventType.OrderSubmitted,
        )

    def test_handle_sunny_day_case(self):
        with patch.object(self.handler, "get_resource") as mocked_get_delivery_event:
            with mock_handler_actions() as (mock_get, mock_post):
                mocked_get_delivery_event.return_value = self.delivery_event
                mock_get.side_effect = [
                    self.order,
                    self.order_event,
                ]

                assert_that(self.handler(self.message), is_(equal_to(True)))
                # Once to get the order, once to get the order_event
                assert_that(mock_get.call_count, equal_to(2))
                mock_post.assert_called_once_with(
                    url="http://localhost:6999/api/v1/order_event",
                    data=dict(
                        customerId=str(self.customer_id),
                        orderId=str(self.order_id),
                        eventType=OrderEventType.OrderFulfilled.name,
                    ),
                )

    def test_fulfilled_order_is_skipped(self):
        fulfilled_order_event = dict(
            eventType=OrderEventType.OrderFulfilled,
        )
        with patch.object(self.handler, "get_resource") as mocked_get_delivery_event:
            with mock_handler_actions() as (mock_get, mock_post):
                mocked_get_delivery_event.return_value = self.delivery_event
                mock_get.side_effect = [
                    self.order,
                    fulfilled_order_event,
                ]
                assert_that(
                    calling(self.handler).with_args(self.message),
                    raises(SkipMessage),
                )

    def test_unsubmitted_order_is_retried(self):
        unsubmitted_order_event = dict(
            eventType=OrderEventType.OrderDeliveryDetailsAdded,
        )
        with patch.object(self.handler, "get_resource") as mocked_get_delivery_event:
            with mock_handler_actions() as (mock_get, mock_post):
                mocked_get_delivery_event.return_value = self.delivery_event
                mock_get.side_effect = [
                    self.order,
                    unsubmitted_order_event,
                ]
                assert_that(
                    calling(self.handler).with_args(self.message),
                    raises(Nack),
                )
