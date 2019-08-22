"""
Topping CRUD routes tests.

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
from charmander.models.pizza_model import CrustType, Pizza, PizzaSize
from charmander.models.topping_model import Topping, ToppingType


class TestPizzaRoutes:

    def setup(self):
        self.graph = create_app(testing=True)
        self.client = self.graph.flask.test_client()
        self.uri = "/api/v1/topping"
        recreate_all(self.graph)

        self.pizza = Pizza(
            id=new_object_id(),
            customer_id=new_object_id(),
            crust_type=CrustType.CHEESE_STUFFED,
            size=PizzaSize.LARGE,
        )
        self.topping = Topping(
            id=new_object_id(),
            pizza_id=self.pizza.id,
            topping_type=ToppingType.PEPPERONI,
        )

    def teardown(self):
        self.graph.postgres.dispose()

    def test_search(self):
        with SessionContext(self.graph), transaction():
            self.pizza.create()
            self.topping.create()

        response = self.client.get(self.uri)

        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            response.json,
            has_entries(
                items=contains(
                    has_entries(
                        id=str(self.topping.id),
                        pizzaId=str(self.topping.pizza_id),
                        toppingType=self.topping.topping_type.name,
                    ),
                ),
            ),
        )

    def test_search_with_filters(self):
        with SessionContext(self.graph), transaction():
            self.pizza.create()
            self.topping.create()

        uri = f"{self.uri}?topping_type={ToppingType.ONION}"

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            len(response.json["items"]),
            is_(equal_to(0)),
        )

    def test_create(self):
        with SessionContext(self.graph), transaction():
            self.pizza.create()

        with patch.object(self.graph.topping_store, "new_object_id") as mocked:
            mocked.return_value = self.topping.id
            response = self.client.post(
                self.uri,
                json=dict(
                    pizzaId=self.topping.pizza_id,
                    toppingType=self.topping.topping_type.name,
                ),
            )

        assert_that(response.status_code, is_(equal_to(201)))
        assert_that(
            response.json,
            has_entries(
                id=str(self.topping.id),
                toppingType=str(self.topping.topping_type),
                pizzaId=str(self.topping.pizza_id),
            ),
        )

    def test_retrieve(self):
        with SessionContext(self.graph), transaction():
            self.pizza.create()
            self.topping.create()

        retrieve_uri = f"{self.uri}/{self.topping.id}"

        response = self.client.get(retrieve_uri)

        assert_that(
            response.json,
            has_entries(
                id=str(self.topping.id),
                pizzaId=str(self.topping.pizza_id),
                toppingType=self.topping.topping_type.name,
            ),
        )

    def test_delete(self):
        with SessionContext(self.graph), transaction():
            self.pizza.create()
            self.topping.create()

        delete_uri = f"{self.uri}/{self.topping.id}"

        response = self.client.delete(delete_uri)
        assert_that(response.status_code, is_(equal_to(204)))
