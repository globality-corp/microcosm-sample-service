"""
Event type to specify state machine for an Order

"""
from microcosm_eventsource.event_types import EventType, event_info
from microcosm_eventsource.transitioning import (
    all_of,
    any_of,
    nothing,
    event,
)
from microcosm_eventsource.accumulation import (
    addition,
    compose,
    difference,
    union,
)

class OrderEventType(EventType):
    """
        Order event type. Models the user journey through specifying an order
        for a pizza as described here:
        https://globality.atlassian.net/wiki/spaces/GLOB/pages/917733426/Product+Spec+Ordering+a+Pizza

    """
    # NB: Our state machines always start with an initial event
    OrderInitialized = event_info(
        follows=nothing(),
        requires=["customer_id"],
    )

    PizzaCreated = event_info(
        follows=any_of(
            "OrderInitialized",
            "PizzaCustomizationFinished",
        ),
        requires=[
            "pizza_size",
            "crust_type",
        ],
        accumulate=addition(
            "PizzaCreated",
        ),
    )

    PizzaToppingAdded = event_info(
        follows=any_of(
            "PizzaCreated",
            "PizzaToppingAdded",
        ),
        requires=[
            "topping_type",
        ],
        accumulate=addition(
            "PizzaToppingAdded",
        ),
    )

    PizzaCustomizationFinished = event_info(
        follows=all_of(
            "PizzaCreated",
            "PizzaToppingAdded",
        ),
        accumulate=difference(
            "PizzaToppingAdded",
        ),
    )

    OrderDeliveryDetailsAdded = event_info(
        follows=event("PizzaCustomizationFinished"),
    )

    OrderSubmitted = event_info(
        follows=event("OrderDeliveryDetailsAdded"),
    )

    OrderFulfilled = event_info(
        follows=event("OrderSubmitted"),
    )
