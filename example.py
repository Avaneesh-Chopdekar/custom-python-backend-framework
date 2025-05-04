from datetime import datetime
from main import PyApi


def logger_middleware(request):
    print(f'[{datetime.now()}] {request['REQUEST_METHOD']} {request["PATH_INFO"]}')


def local_middleware(request):
    print("Local Middleware")


pyapi = PyApi(middlewares=[logger_middleware])


@pyapi.get("/hello/{id}", middlewares=[local_middleware])
def hello(request, response, id):
    response.send(f"Hello {id}")


@pyapi.post("/users")
def create_user(request, response):
    response.send("User Created", status_code="201 Created")
