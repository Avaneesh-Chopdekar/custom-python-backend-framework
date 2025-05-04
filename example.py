from main import PyApi


pyapi = PyApi()


@pyapi.get("/hello")
def hello(request, response):
    response["status_code"] = "200 OK"
    response["headers"] = [("Content-Type", "text/plain")]
    response["text"] = "Hello, World!"
