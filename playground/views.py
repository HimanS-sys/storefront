from django.shortcuts import render
from django.http import HttpResponse

def say_hello(request):
    """
    returns "Hello World!"
    """
    context = {"name" : "Himanshu Kandpal"}
    return render(
        request,
        "hello.html",
        context,
    )