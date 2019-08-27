"""
Order Event CRUD routes tests.

Tests are sunny day cases under the assumption that framework conventions
handle most error conditions.

"""
from unittest.mock import patch

from hamcrest import (
    assert_that,
    contains,
    equal_to,
    has_entries,
    is_,
)
from microcosm_postgres.context import SessionContext, transaction
from microcosm_postgres.identifiers import new_object_id
from microcosm_postgres.operations import recreate_all

from charmander.app import create_app
from charmander.models.order_event_type import OrderEventType
from charmander.models.order_model import Order
from charmander.models.pizza_model import CrustType, PizzaSize


class TestOrderEventRoutes:

    def setup(self):
        self.graph = create_app(testing=True)
        self.client = self.graph.flask.test_client()
        self.uri = "/api/v1/order_event"
        recreate_all(self.graph)

        self.factory = self.graph.order_event_factory

        self.customer_id = new_object_id()

        with SessionContext(self.graph), transaction():
            self.order = Order(
                id=new_object_id(),
                customer_id=new_object_id(),
            )
            self.order.create()

    def create_initial_event(self):
        with self.graph.flask.test_request_context():
            with SessionContext(self.graph), transaction():
                self.initial_order_event = self.factory.create(
                    ns=None,
                    sns_producer=self.graph.sns_producer,
                    event_type=OrderEventType.OrderInitialized,
                    order_id=self.order.id,
                    customer_id=self.customer_id,
                )

    def teardown(self):
        self.graph.postgres.dispose()
        self.graph.sns_producer.sns_client.reset_mock()

    def test_search(self):
        self.create_initial_event()
        response = self.client.get(self.uri)

        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            response.json,
            has_entries(
                items=contains(
                    has_entries(
                        id=str(self.initial_order_event.id),
                        eventType=str(self.initial_order_event.event_type),
                        orderId=str(self.initial_order_event.order_id),
                        customerId=str(self.initial_order_event.customer_id),
                    ),
                ),
            ),
        )

    def test_search_with_filters(self):
        self.create_initial_event()
        uri = f"{self.uri}?customer_id={new_object_id()}"

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            len(response.json["items"]),
            is_(equal_to(0)),
        )

    def test_create_first(self):
        initial_order_event_id = new_object_id()
        with patch.object(self.graph.order_event_store, "new_object_id") as mocked:
            mocked.return_value = initial_order_event_id
            response = self.client.post(
                self.uri,
                json=dict(
                    customerId=str(self.customer_id),
                    orderId=str(self.order.id),
                    eventType=OrderEventType.OrderInitialized.name,
                ),
            )

        assert_that(response.status_code, is_(equal_to(201)))
        assert_that(
            response.json,
            has_entries(
                id=str(initial_order_event_id),
                customerId=str(self.customer_id),
                orderId=str(self.order.id),
                eventType=OrderEventType.OrderInitialized.name
            ),
        )

    def test_create_pizza_created(self):
        self.create_initial_event()

        pizza_created_id = new_object_id()

        with patch.object(self.graph.order_event_store, "new_object_id") as mocked:
            mocked.return_value = pizza_created_id
            response = self.client.post(
                self.uri,
                json=dict(
                    customerId=str(self.customer_id),
                    orderId=str(self.order.id),
                    eventType=OrderEventType.PizzaCreated.name,
                    crustType=CrustType.REGULAR.name,
                    pizzaSize=PizzaSize.REGULAR.name,
                ),
            )

        assert_that(response.status_code, is_(equal_to(201)))
        assert_that(
            response.json,
            has_entries(
                id=str(pizza_created_id),
                customerId=str(self.customer_id),
                orderId=str(self.order.id),
                eventType=OrderEventType.PizzaCreated.name,
                crustType=CrustType.REGULAR.name,
                pizzaSize=PizzaSize.REGULAR.name,
            ),
        )

    def test_retrieve(self):
        self.create_initial_event()

        retrieve_uri = f"{self.uri}/{self.initial_order_event.id}"

        response = self.client.get(retrieve_uri)

        assert_that(
            response.json,
            has_entries(
                id=str(self.initial_order_event.id),
                customerId=str(self.customer_id),
                orderId=str(self.order.id),
                eventType=OrderEventType.OrderInitialized.name
            ),
        )
