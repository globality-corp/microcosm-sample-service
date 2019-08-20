"""
Pizza CRUD routes tests.

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
from charmander.models.pizza_model import (
    CrustType,
    Pizza,
    PizzaSize,
)


class TestPizzaRoutes:

    def setup(self):
        self.graph = create_app(testing=True)
        self.client = self.graph.flask.test_client()
        self.uri = "/api/v1/pizza"
        recreate_all(self.graph)

        self.pizza = Pizza(
            id=new_object_id(),
            customer_id=new_object_id(),
            crust_type=CrustType.CHEESE_STUFFED,
            size=PizzaSize.LARGE,
        )

    def teardown(self):
        self.graph.postgres.dispose()

    def test_search(self):
        with SessionContext(self.graph), transaction():
            self.pizza.create()

        response = self.client.get(self.uri)

        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            response.json,
            has_entries(
                items=contains(
                    has_entries(
                        id=str(self.pizza.id),
                        customerId=str(self.pizza.customer_id),
                        crustType=self.pizza.crust_type.name,
                        size=self.pizza.size.name,
                    ),
                ),
            ),
        )

    def test_search_with_filters(self):
        with SessionContext(self.graph), transaction():
            self.pizza.create()

        uri = f"{self.uri}?size={PizzaSize.PERSONAL}"

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            len(response.json["items"]),
            is_(equal_to(0)),
        )

    def test_create(self):
        with patch.object(self.graph.pizza_store, "new_object_id") as mocked:
            mocked.return_value = self.pizza.id
            response = self.client.post(
                self.uri,
                json=dict(
                    customerId=self.pizza.customer_id,
                    crustType=self.pizza.crust_type.name,
                    size=self.pizza.size.name,
                ),
            )

        assert_that(response.status_code, is_(equal_to(201)))
        assert_that(
            response.json,
            has_entries(
                id=str(self.pizza.id),
                customerId=str(self.pizza.customer_id),
                crustType=self.pizza.crust_type.name,
                size=self.pizza.size.name,
            ),
        )

    def test_replace_with_new(self):
        replace_uri = f"{self.uri}/{self.pizza.id}"

        response = self.client.put(
            replace_uri,
            json=dict(
                crustType=CrustType.REGULAR.name,
                customerId=str(self.pizza.customer_id),
                size=str(self.pizza.size),
            ),
        )

        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            response.json,
            has_entries(
                id=str(self.pizza.id),
                customerId=str(self.pizza.customer_id),
                crustType=CrustType.REGULAR.name,
                size=str(self.pizza.size),
            ),
        )

    def test_retrieve(self):
        with SessionContext(self.graph), transaction():
            self.pizza.create()

        retrieve_uri = f"{self.uri}/{self.pizza.id}"

        response = self.client.get(retrieve_uri)

        assert_that(
            response.json,
            has_entries(
                id=str(self.pizza.id),
                customerId=str(self.pizza.customer_id),
                crustType=self.pizza.crust_type.name,
                size=self.pizza.size.name,
            ),
        )

    def test_delete(self):
        with SessionContext(self.graph), transaction():
            self.pizza.create()

        delete_uri = f"{self.uri}/{self.pizza.id}"

        response = self.client.delete(delete_uri)
        assert_that(response.status_code, is_(equal_to(204)))
