class PyApi:
    def __init__(self):
        self.routes = dict()

    def __call__(self, environ, start_response):
        response = {}
        for path, handler_dict in self.routes.items():
            for request_method, handler in handler_dict.items():
                if (
                    environ["PATH_INFO"] == path
                    and environ["REQUEST_METHOD"] == request_method
                ):
                    handler(environ, response)
                    start_response(response["status_code"], response["headers"])
                    return [(response["text"]).encode()]

        status_code = "404 Not Found"
        headers = [("Content-Type", "text/plain")]
        body = b"Not Found"

        start_response(status_code, headers)
        return [body]

    def get(self, path=None):
        def wrapper(handler):
            # {
            #     '/hello': {
            #         'GET': handler
            #     }
            # }
            path_name = path if path else f"/{handler.__name__}"
            if path_name not in self.routes:
                self.routes[path_name] = dict()

            self.routes[path_name]["GET"] = handler

            # print(self.routes)

        return wrapper


pyapi = PyApi()
