from pyms.config.loader import ConfigLoader
from pyms.exceptions import ServiceDoesNotExistException


def get_conf(*args, **kwargs):
    """
    Returns an object with a set of attributes retrieved from the configuration file. Each subblock is a append of the
    parent and this name, in example of the next yaml, tracer will be `pyms.tracer`. If we have got his config file:
    ```
    pyms:
        services:
            metrics: true
            requests: true
            swagger:
                path: ""
                file: "swagger.yaml"
            tracer:
                client: "jaeger"
                host: "localhost"
                component_name: "Python Microservice"
        config:
            DEBUG: true
            TESTING: true
    ```
    * `pyms` block is the default key to load in the pyms.flask.app.create_app.Microservice class.
        * `metrics`: is set as the service `pyms.metrics`
        * `swagger`: is set as the service `pyms.swagger`
        * `tracer`: is set as the service `pyms.tracer`
    * `my-ms` block is defined by the env var `CONFIGMAP_SERVICE`. By default is `ms`. This block is the default flask
    block config
    :param args:
    :param kwargs:
    :return:
    """
    service = kwargs.pop("service", None)
    if not service:
        raise ServiceDoesNotExistException("Service not defined")
    config_loader = ConfigLoader(*args, **kwargs)
    service_config = config_loader.config or {}
    for dict_part in service.split('.'):
        service_config = service_config.get(dict_part, {})
    return service_config