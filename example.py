from datetime import datetime
from main import PyApi


def logger_middleware(request):
    print(f"[{datetime.now()}] {request.request_method} {request.path_info}")


def local_middleware(request):
    print("Local Middleware")


pyapi = PyApi(middlewares=[logger_middleware])


@pyapi.get("/hello/{id}", middlewares=[local_middleware])
def hello(request, response, id):
    response.render(
        "example",
        {
            "id": id,
            "name": request.queries.get("name", "World"),
            "message": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        },
    )


@pyapi.post("/users")
def create_user(request, response):
    response.send("User Created", status_code="201 Created")


@pyapi.route("/books")
class Book:
    def __init__(self):
        pass

    def get(self, request, response):
        response.send([{"id": 1, "title": "Book 1"}, {"id": 2, "title": "Book 2"}])
        response.headers.append(("Content-Type", "application/json"))

    def post(self, request, response):
        response.send("Book created", status_code="201 Created")
