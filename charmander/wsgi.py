"""
Entrypoint module for WSGI containers.

"""
from charmander.app import create_app


app = create_app().app
