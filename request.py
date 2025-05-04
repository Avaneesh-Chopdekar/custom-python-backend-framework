from collections import defaultdict


class Request:
    def __init__(self, environ):
        self.queries = defaultdict()
        for key, value in environ.items():
            setattr(self, key.replace(".", "_").lower(), value)

        if self.query_string:
            for query in self.query_string.split("&"):
                key, value = query.split("=")
                self.queries[key] = value
