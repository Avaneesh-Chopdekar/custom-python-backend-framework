import json
import re


class Response:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text
        self.headers = []
        self.templates_directory = "templates"

    def as_wsgi(self, start_response):
        start_response(self.status_code, self.headers)
        return [(self.text).encode()]

    def send(self, text="", status_code="200 OK"):
        if isinstance(text, str):
            self.text = text
        elif isinstance(text, list):
            self.text = json.dumps(text)
        elif isinstance(text, dict):
            self.text = json.dumps(text)
        else:
            self.text = str(text)

        if isinstance(status_code, int):
            self.status_code = str(status_code)
        elif isinstance(status_code, str):
            self.status_code = status_code
        else:
            raise TypeError("status_code must be int or str")

    def render(self, template, context={}):
        if not isinstance(template, str):
            raise TypeError("template must be str")

        if ".html" not in template:
            path = f"{self.templates_directory}/{template}.html"
        else:
            path = f"{self.templates_directory}/{template}"

        with open(path) as file:
            template = file.read()

            for key, value in context.items():
                # {{ key }}
                template = re.sub(
                    r"{{\s*" + re.escape(key) + r"\s*}}", str(value), template
                )

        self.headers.append(("Content-Type", "text/html"))
        self.text = template
        self.status_code = "200 OK"
