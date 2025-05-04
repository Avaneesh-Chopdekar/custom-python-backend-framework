from main import PyApi


pyapi = PyApi()


@pyapi.get("/hello/{id}")
def hello(request, response, id):
    response.send(f"Hello {id}")


@pyapi.post("/users")
def create_user(request, response):
    response.send("User Created", status_code="201 Created")
