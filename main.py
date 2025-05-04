import inspect
from response import Response
from request import Request
from parse import parse

SUPPORTED_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


class PyApi:
    def __init__(self, middlewares=[]):
        self.routes = dict()
        self.middlewares = middlewares
        self.route_middlewares = dict()

    def __call__(self, environ, start_response):
        response = Response(status_code="404 Not Found", text="Not Found")
        request = Request(environ)

        for middleware in self.middlewares:
            if callable(middleware):
                middleware(request)
            else:
                raise TypeError("Middleware must be callable")

        requested_path = request.path_info
        request_method = request.request_method.upper()

        for path, handler_info in self.routes.items():
            res = parse(path, requested_path)
            if res:  # Check if the path pattern matches
                # Check if it's a function-based route
                if request_method in handler_info:
                    handler = handler_info[request_method]["handler"]
                    middleware_list = handler_info[request_method]["middlewares"]

                    for middleware in middleware_list:
                        if callable(middleware):
                            middleware(request)
                        else:
                            raise TypeError("Middleware must be callable")

                    handler(request, response, **res.named)
                    return response.as_wsgi(start_response)

                # Check if it's a class-based route (registered with @route)
                elif "CLASS_BASED" in handler_info:
                    handler_class = handler_info["CLASS_BASED"]["handler"]
                    middleware_list = handler_info["CLASS_BASED"]["middlewares"]

                    for middleware in middleware_list:
                        if callable(middleware):
                            middleware(request)
                        else:
                            raise TypeError("Middleware must be callable")

                    # Create an instance of the class
                    instance = handler_class()
                    # Get the appropriate method based on the request method
                    method = getattr(instance, request_method.lower(), None)

                    if method and callable(method):
                        method(request, response, **res.named)
                        return response.as_wsgi(start_response)
                    else:
                        # Method not found on the class for this request method
                        response = Response(
                            status_code="405 Method Not Allowed",
                            text="Method Not Allowed",
                        )
                        return response.as_wsgi(start_response)

        # If no path matches, return the initial 404 response
        return response.as_wsgi(start_response)

    def __map_route_to_handler(self, path, request_method, handler, middlewares):
        path_name = path if path else f"/{handler.__name__}"
        if path_name not in self.routes:
            self.routes[path_name] = dict()

        self.routes[path_name][request_method] = {
            "handler": handler,
            "middlewares": middlewares,
        }

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

    def route(self, path=None, middlewares=[]):
        def wrapper(handler_class):
            if isinstance(handler_class, type):
                self.__map_route_to_handler(
                    path
                    or f"/{handler_class.__name__.lower()}",  # Use lowercase for class route paths
                    "CLASS_BASED",
                    handler_class,
                    middlewares,
                )
            else:
                raise ValueError("@route can only be used for classes")

        return wrapper
