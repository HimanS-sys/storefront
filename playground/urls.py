from django.urls import path
from playground import views

# URLConf
urlpatterns = [
    path(
        "hello/",
        views.say_hello
    )
]