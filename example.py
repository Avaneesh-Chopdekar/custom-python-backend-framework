from main import PyApi


pyapi = PyApi()


@pyapi.get("/hello")
def hello(request, response):
    response.send("Hello World")


@pyapi.post("/users")
def create_user(request, response):
    response.send("User Created", status_code="201 Created")
