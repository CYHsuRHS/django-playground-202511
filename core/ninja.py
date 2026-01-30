from ninja import NinjaAPI

from blog.ninja import router as blog_router

# 實例化為api的變數
api = NinjaAPI()
api.add_router("/blog", blog_router, tags=["文章"])


# 這個api允許使用get方法訪問/hello
@api.get("/hello")
def hello(request):
    return {"message": "Hello, Django Ninja!"}
