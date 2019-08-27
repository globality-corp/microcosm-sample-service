"""
Test order event state transitions

"""
from collections import namedtuple

from hamcrest import assert_that, equal_to, is_

from charmander.models.order_event_type import OrderEventType


def step(event_type, state):
    """
    Transition to event type given the current state. Ignores whether this is a
    valid transition.

    """
    return set(event_type.accumulate_state(state))


def transition_with_assertion(current_state, event_type, desired_state):
    """
    Transition from `current_state` to `event_type` and assert the resulting
    `desired_state`.

    """
    assert_that(event_type.may_transition(current_state))
    new_state = step(event_type, current_state)
    assert_that((event_type, new_state), equal_to((event_type, desired_state)))
    return new_state


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

    def test_add_second_pizzas(self):
        empty_state = set()
        initial_state = step(OrderEventType.OrderInitialized, empty_state)
        pizza_added = step(OrderEventType.PizzaCreated, initial_state)
        topping_added = step(OrderEventType.PizzaToppingAdded, pizza_added)
        customization_finished = step(
            OrderEventType.PizzaCustomizationFinished,
            topping_added,
        )
        assert_that(
            OrderEventType.PizzaCreated.may_transition(customization_finished),
            is_(equal_to(True)),
        )


    def test_fulfill_order(self):
        event_sequence = [
            (
                OrderEventType.OrderInitialized,
                {OrderEventType.OrderInitialized},
            ),
            (    
                OrderEventType.PizzaCreated,
                {
                    OrderEventType.PizzaCreated,
                },
            ),
            (
                OrderEventType.PizzaToppingAdded,
                {
                    OrderEventType.PizzaCreated,
                    OrderEventType.PizzaToppingAdded,
                },
            ),
            (
                OrderEventType.PizzaCustomizationFinished,
                {
                    OrderEventType.PizzaCustomizationFinished,
                },
            ),
            (
                OrderEventType.OrderDeliveryDetailsAdded,
                {
                    OrderEventType.OrderDeliveryDetailsAdded,
                },
            ),
            (
                OrderEventType.OrderSubmitted,
                {
                    OrderEventType.OrderSubmitted,
                },
            ),
            (
                OrderEventType.OrderFulfilled,
                {
                    OrderEventType.OrderFulfilled,
                },
            ),
        ]
        next_state = set()

        for event_type, desired_state in event_sequence:
            next_state = transition_with_assertion(
                next_state,
                event_type,
                desired_state,
            )
