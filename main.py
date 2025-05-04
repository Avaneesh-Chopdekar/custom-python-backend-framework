from response import Response
from parse import parse


class PyApi:
    def __init__(self):
        self.routes = dict()

    def __call__(self, environ, start_response):
        response = Response(status_code="404 Not Found", text="Not Found")
        for path, handler_dict in self.routes.items():
            res = parse(path, environ["PATH_INFO"])
            for request_method, handler in handler_dict.items():
                if res and environ["REQUEST_METHOD"] == request_method:
                    handler(environ, response, **res.named)

        return response.as_wsgi(start_response)

    def __map_route_to_handler(self, path, request_method, handler):
        # {
        #     '/hello': {
        #         'GET': handler
        #     }
        # }
        path_name = path if path else f"/{handler.__name__}"
        if path_name not in self.routes:
            self.routes[path_name] = dict()

        self.routes[path_name][request_method] = handler
        return handler

    def get(self, path=None):
        def wrapper(handler):
            return self.__map_route_to_handler(path, "GET", handler)

        return wrapper

    def post(self, path=None):
        def wrapper(handler):
            return self.__map_route_to_handler(path, "POST", handler)

        return wrapper

    def put(self, path=None):
        def wrapper(handler):
            return self.__map_route_to_handler(path, "PUT", handler)

        return wrapper

    def patch(self, path=None):
        def wrapper(handler):
            return self.__map_route_to_handler(path, "PATCH", handler)

        return wrapper

    def delete(self, path=None):
        def wrapper(handler):
            return self.__map_route_to_handler(path, "DELETE", handler)

        return wrapper


pyapi = PyApi()
