"""
Pizza persistence.

"""
from microcosm.api import binding
from microcosm_postgres.store import Store

from charmander.models.pizza_model import Pizza


@binding("pizza_store")
class PizzaStore(Store):

    def __init__(self, graph):
        super().__init__(
            graph,
            Pizza,
            auto_filter_fields=(
                Pizza.customer_id,
                Pizza.order_id,
                Pizza.crust_type,
                Pizza.size,
            ),
        )
