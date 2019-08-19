# charmander

Sample project to showcase building services with our microcosm libraries.


## Goal

This is a special service designed to show how the various pieces of the
microcosm ecosystem work together in a sample service. This service uses the
same building blocks of our architecture and services as a concrete example of
how our `microcosm-` libraries work together. These include:

- Routes and resources with `microcosm-flask`
- Stores and models with `microcosm-postgres`
- Connecting the two through `microcosm-pubsub` and SQS/SNS



## Developing

To setup the project for local development, make sure you have a virtualenv setup, and then run:

    pip install -e .

This will install all the dependencies and set the project up for local usage.


## Postgres

The service requires a Postgres user and two datbases (one is for testing):

    createuser charmander
    createdb -O charmander charmander_db
    createdb -O charmander charmander_test_db

The service schema can be initialized using:

    createall [-D]


## Flask

To run the Flask web server when developing locally, invoke the following:

    runserver

The service publishes several endpoints by default.

 -  The service publishes its own health:

        GET /api/health

 -  The service publishes a [crawlable](https://en.wikipedia.org/wiki/HATEOAS) endpoint for discovery
    of its operations:

        GET /api/

 -  The service publishes [Swagger](http://swagger.io/) definitions for its operations (by API version)
    using [HAL JSON](http://stateless.co/hal_specification.html):

        GET /api/v1/swagger

