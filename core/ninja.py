from ninja import NinjaAPI

# 實例化為api的變數
api = NinjaAPI()


# 這個api允許使用get方法訪問/hello
@api.get("/hello")
def hello(request):
    return {"message": "Hello, Django Ninja!"}
