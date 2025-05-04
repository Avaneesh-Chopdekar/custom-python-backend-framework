class Response:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text
        self.headers = []

    def as_wsgi(self, start_response):
        start_response(self.status_code, self.headers)
        return [(self.text).encode()]

    def send(self, text="", status_code="200 OK"):
        if isinstance(text, str):
            self.text = text
        else:
            self.text = str(text)

        if isinstance(status_code, int):
            self.status_code = str(status_code)
        elif isinstance(status_code, str):
            self.status_code = status_code
        else:
            raise TypeError("status_code must be int or str")
