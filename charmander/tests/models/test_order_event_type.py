"""
Test order event state transitions

"""
from hamcrest import assert_that, equal_to, is_

from charmander.models.order_event_type import OrderEventType


def step(event_type, state):
    return set(event_type.accumulate_state(state))


class TestCompanyEventType():

    def setup(self):
        pass

    def test_initial_state(self):
        """
        Ensure that the state machine can *only* start with the
        OrderInitializedEvent. Helpful for event machines with more than one
        initial state.

        """
        state = set()
        for event_type in OrderEventType:
            is_start = event_type == OrderEventType.OrderInitialized
            assert_that(event_type.may_transition(state), is_(equal_to(is_start)))

    def test_pizza_requires_at_least_one_topping(self):
        empty_state = set()
        initial_state = step(OrderEventType.OrderInitialized, empty_state)
        pizza_added = step(OrderEventType.PizzaCreated, initial_state)
        assert_that(OrderEventType.PizzaCustomizationFinished.may_transition(pizza_added), is_(equal_to(False)))

        topping_added = step(OrderEventType.PizzaToppingAdded, pizza_added)
        assert_that(
            OrderEventType.PizzaCustomizationFinished.may_transition(topping_added),
            is_(equal_to(True)),
        )

    def test_add_two_pizzas(self):
        pass

    def test_fulfill_order(self):
        pass
