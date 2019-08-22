"""
Order CRUD routes tests.

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
from charmander.models.order_model import Order


class TestOrderRoutes:

    def setup(self):
        self.graph = create_app(testing=True)
        self.client = self.graph.flask.test_client()
        self.uri = "/api/v1/order"
        recreate_all(self.graph)

        self.order = Order(
            id=new_object_id(),
            customer_id=new_object_id(),
        )

    def teardown(self):
        self.graph.postgres.dispose()

    def test_search(self):
        with SessionContext(self.graph), transaction():
            self.order.create()

        response = self.client.get(self.uri)

        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            response.json,
            has_entries(
                items=contains(
                    has_entries(
                        id=str(self.order.id),
                        customerId=str(self.order.customer_id),
                    ),
                ),
            ),
        )

    def test_search_with_filters(self):
        with SessionContext(self.graph), transaction():
            self.order.create()

        uri = f"{self.uri}?customer_id={new_object_id()}"

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            len(response.json["items"]),
            is_(equal_to(0)),
        )

        valid_uri = f"{self.uri}?customer_id={self.order.customer_id}"
        response = self.client.get(valid_uri)

        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            len(response.json["items"]),
            is_(equal_to(1)),
        )

    def test_create(self):
        with patch.object(self.graph.order_store, "new_object_id") as mocked:
            mocked.return_value = self.order.id
            response = self.client.post(
                self.uri,
                json=dict(
                    customerId=self.order.customer_id,
                ),
            )

        assert_that(response.status_code, is_(equal_to(201)))
        assert_that(
            response.json,
            has_entries(
                id=str(self.order.id),
                customerId=str(self.order.customer_id),
            ),
        )

    def test_retrieve(self):
        with SessionContext(self.graph), transaction():
            self.order.create()

        retrieve_uri = f"{self.uri}/{self.order.id}"

        response = self.client.get(retrieve_uri)

        assert_that(
            response.json,
            has_entries(
                id=str(self.order.id),
                customerId=str(self.order.customer_id),
            ),
        )
