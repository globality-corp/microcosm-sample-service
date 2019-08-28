"""
Command line entry point for asynchronous processing.

"""
from microcosm.loaders import (
    load_each,
    load_from_dict,
    load_from_environ,
    load_from_json_file,
)
from microcosm_pubsub.daemon import ConsumerDaemon
from microcosm_secretsmanager.loaders.conventions import load_from_secretsmanager

import charmander.daemon.handlers  # noqa: F401


class CharmanderDaemon(ConsumerDaemon):
    """
    Asynchronous worker.

    """
    @property
    def name(self):
        return "charmander"

    @property
    def loader(self):
        """
        Define the object graph config loader.

        """
        return load_each(
            load_from_dict(self.defaults),
            load_from_secretsmanager(),
            load_from_json_file,
            load_from_environ,
        )

    @property
    def components(self):
        return super().components + [
            # clients
            # "charmander_v1", XXX We will return to the subject of service
            # clients in a subsequent PR
            # handlers
            "record_pizza_delivery",
        ]


def main():
    """
    Command line entry point.

    """
    daemon = CharmanderDaemon()
    daemon.run()


if __name__ == '__main__':
    main()
