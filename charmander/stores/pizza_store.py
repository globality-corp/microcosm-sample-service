"""
Pizza persistence.

"""
from microcosm.api import binding
from microcosm_postgres.store import Store

from charmander.models.pizza_model import Pizza


@binding("pizza_store")
class PizzaStore(Store):

    def __init__(self, graph):
        super().__init__(self, Pizza)

    def _filter(
        self,
        query,
        customer_id=None,
        crust_type=None,
        size=None,
        **kwargs,
    ):
        if customer_id is not None:
            query = query.filter(
                Pizza.customer_id == customer_id,
            )

        if crust_type is not None:
            query = query.filter(
                Pizza.crust_type == crust_type,
            )

        if size is not None:
            query = query.filter(
                Pizza.size == size,
            )

        return super()._filter(query, **kwargs)
