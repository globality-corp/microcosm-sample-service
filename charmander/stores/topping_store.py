"""
Topping persistence.

"""
from microcosm.api import binding
from microcosm_postgres.store import Store

from charmander.models.topping_model import Topping


@binding("topping")
class ToppingStore(Store):

    def __init__(self, graph):
        super().__init__(self, Topping)

    def _filter(
        self,
        query,
        pizza_id=None,
        topping_type=None,
        **kwargs,
    ):
        if pizza_id is not None:
            query = query.filter(
                Topping.pizza_id == pizza_id,
            )

        if topping_type is not None:
            query = query.filter(
                Topping.topping_type == topping_type,
            )

        return super()._filter(query, **kwargs)
