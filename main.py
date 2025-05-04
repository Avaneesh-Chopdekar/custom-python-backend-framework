from response import Response
from parse import parse


class PyApi:
    def __init__(self, middlewares=[]):
        self.routes = dict()
        self.middlewares = middlewares
        self.route_middlewares = dict()

    def __call__(self, environ, start_response):
        response = Response(status_code="404 Not Found", text="Not Found")

        for middleware in self.middlewares:
            if callable(middleware):
                middleware(environ)
            else:
                raise TypeError("Middleware must be callable")

        for path, handler_dict in self.routes.items():
            res = parse(path, environ["PATH_INFO"])
            for request_method, handler in handler_dict.items():
                if res and environ["REQUEST_METHOD"] == request_method:
                    middleware_list = self.route_middlewares[path][request_method]
                    for middleware in middleware_list:
                        if callable(middleware):
                            middleware(environ)
                        else:
                            raise TypeError("Middleware must be callable")
                    handler(environ, response, **res.named)

        return response.as_wsgi(start_response)

    def __map_route_to_handler(self, path, request_method, handler, middlewares):
        # {
        #     '/hello': {
        #         'GET': handler
        #     }
        # }
        path_name = path if path else f"/{handler.__name__}"
        if path_name not in self.routes:
            self.routes[path_name] = dict()

        self.routes[path_name][request_method] = handler

        # {
        #     '/hello': {
        #         'GET': [middleware1, middleware2]
        #     }
        # }

        if path_name not in self.route_middlewares:
            self.route_middlewares[path_name] = dict()

        self.route_middlewares[path_name][request_method] = middlewares

        return handler

    def get(self, path=None, middlewares=[]):
        def wrapper(handler):
            return self.__map_route_to_handler(path, "GET", handler, middlewares)

        return wrapper

    def post(self, path=None, middlewares=[]):
        def wrapper(handler):
            return self.__map_route_to_handler(path, "POST", handler, middlewares)

        return wrapper

    def put(self, path=None, middlewares=[]):
        def wrapper(handler):
            return self.__map_route_to_handler(path, "PUT", handler, middlewares)

        return wrapper

    def patch(self, path=None, middlewares=[]):
        def wrapper(handler):
            return self.__map_route_to_handler(path, "PATCH", handler, middlewares)

        return wrapper

    def delete(self, path=None, middlewares=[]):
        def wrapper(handler):
            return self.__map_route_to_handler(path, "DELETE", handler, middlewares)

        return wrapper


pyapi = PyApi()
