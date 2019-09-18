"""
Event type to specify state machine for an Order

"""
from microcosm_eventsource.accumulation import addition, compose, difference
from microcosm_eventsource.event_types import EventType, event_info
from microcosm_eventsource.transitioning import (
    all_of,
    any_of,
    event,
    nothing,
)


class OrderEventType(EventType):
    """
        Order event type. Models the user journey through specifying an order
        for a pizza as described here:
        https://globality.atlassian.net/wiki/spaces/GLOB/pages/917733426/Product+Spec+Ordering+a+Pizza

    """
    # NB: Our state machines always start with an initial event
    # order created
    OrderInitialized = event_info(
        follows=nothing(),
        requires=["customer_id"],
    )

    # pizza created
    PizzaCreated = event_info(
        follows=any_of(
            "OrderInitialized",
            "PizzaCustomizationFinished",
        ),
        requires=[
            "pizza_size",
            "crust_type",
        ],
        accumulate=compose(
            addition("PizzaCreated"),
            difference("PizzaCustomizationFinished"),
            difference("OrderInitialized"),
        ),
    )

    # topping created
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

    # event initiated by user
    PizzaCustomizationFinished = event_info(
        follows=all_of(
            "PizzaCreated",
            "PizzaToppingAdded",
        ),
        accumulate=compose(
            addition("PizzaCustomizationFinished"),
            difference("PizzaCreated"),
            difference("PizzaToppingAdded"),
        ),
    )

    # by user (or an external event from some other service)
    OrderDeliveryDetailsAdded = event_info(
        follows=event("PizzaCustomizationFinished"),
        accumulate=compose(
            addition("OrderDeliveryDetailsAdded"),
            difference("PizzaCustomizationFinished"),
        ),
    )

    # automatic after submitting details FOR NOW XXX
    OrderSubmitted = event_info(
        follows=event("OrderDeliveryDetailsAdded"),
        accumulate=compose(
            addition("OrderSubmitted"),
            difference("OrderDeliveryDetailsAdded"),
        ),
    )

    # from some other service
    OrderFulfilled = event_info(
        follows=event("OrderSubmitted"),
        accumulate=compose(
            addition("OrderFulfilled"),
            difference("OrderSubmitted"),
        ),
    )
