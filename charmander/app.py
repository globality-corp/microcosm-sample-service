"""
Create the application.

"""
from microcosm.api import create_object_graph
from microcosm.loaders import load_each, load_from_environ, load_from_json_file
from microcosm.loaders.compose import load_config_and_secrets
from microcosm_secretsmanager.loaders.conventions import load_from_secretsmanager

import charmander.postgres  # noqa
import charmander.routes  # noqa
import charmander.stores  # noqa
import charmander.factories.order_event_factory  # noqa
from charmander.config import load_default_config


def create_app(debug=False, testing=False, model_only=False):
    """
    Create the object graph for the application.

    """
    config_loader = load_each(
        load_default_config,
        load_from_environ,
        load_from_json_file,
    )
    partitioned_loader = load_config_and_secrets(
        config=config_loader,
        secrets=load_from_secretsmanager(),
    )

    graph = create_object_graph(
        name=__name__.split(".")[0],
        debug=debug,
        testing=testing,
        loader=partitioned_loader,
    )

    graph.use(
        "pizza_store",
        "order_store",
        "order_event_store",
        "topping_store",
        "logging",
        "postgres",
        "sessionmaker",
        "session_factory",
    )

    if not model_only:
        graph.use(
            # conventions
            "build_info_convention",
            "config_convention",
            "discovery_convention",
            "health_convention",
            "landing_convention",
            "port_forwarding",
            "postgres_health_check",
            "swagger_convention",
            # routes
            "pizza_routes",
            "order_routes",
            "order_event_routes",
            "topping_routes",
        )

    return graph.lock()
