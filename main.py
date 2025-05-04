class PyApi:
    def __init__(self):
        pass

    def __call__(self, environ, start_response):
        print(environ)
        start_response("200 OK", [("Content-Type", "text/plain")])
        return [b"Hello Avaneesh!"]


pyapi = PyApi()
