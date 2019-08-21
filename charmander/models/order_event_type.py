"""
Event type to specify state machine for an Order

"""
from microcosm_eventsource.event_types import EventType, event_info
from microcosm_eventsource.transitioning import any_of, nothing


class OrderEventType(EventType):
    """
        Order event type. Models the user journey through specifying an order
        for a pizza as described here:
        https://globality.atlassian.net/wiki/spaces/GLOB/pages/917733426/Product+Spec+Ordering+a+Pizza

    """
    # NB: Our state machines always start with an initial event
    OrderInitialized = event_info(
        follows=nothing(),
    )

    PizzaCreated = event_info(
        follows=any_of(
            "OrderInitialized",
            "PizzaCustomizationFinished",
        ),
    )
    
    PizzaToppingAdded = event_info(
        follows=any_of(
            "PizzaCreated",
            "PizzaToppingAdded",
        ),
    )
    
    PizzaCustomizationFinished = event_info(
        follows=any_of(
            "PizzaCreated",
            "PizzaToppingAdded",
        ),
    )

    OrderDeliveryDetailsAdded = event_info(
        follows="PizzaCustomizationFinished",
    )

    OrderSubmitted = event_info(
        follows="OrderDeliveryDetailsAdded",
    )

    OrderSatisfied = event_info(
        follows="OrderSubmitted",
    )
