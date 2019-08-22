"""
Order persistence.

"""
from microcosm.api import binding
from microcosm_postgres.store import Store

from charmander.models.order_model import Order


@binding("order_store")
class OrderStore(Store):

    def __init__(self, graph):
        super().__init__(
            graph,
            Order,
            auto_filter_fields=(
                Order.customer_id,
                Order.purpose,
                Order.resolution,
            ),
        )

    def _filter(
        self,
        query,
        **kwargs,
    ):
        return super()._filter(query, **kwargs)
