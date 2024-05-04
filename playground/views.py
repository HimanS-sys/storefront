from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product

def say_hello(request):
    """
    returns "Hello World!"
    """
    product_20_to_30 = Product.objects.filter(unit_price__range = (20, 32))
    context = {"name" : "Himanshu Kandpal", "products" : product_20_to_30}
    return render(
        request,
        "hello.html",
        context,
    )