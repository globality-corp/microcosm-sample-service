"""
Topping persistence.

"""
from microcosm.api import binding
from microcosm_postgres.store import Store

from charmander.models.topping_model import Topping


@binding("topping_store")
class ToppingStore(Store):

    def __init__(self, graph):
        super().__init__(
            graph,
            Topping,
            auto_filter_fields=(
                Topping.pizza_id,
                Topping.topping_type,
            ),
        )
