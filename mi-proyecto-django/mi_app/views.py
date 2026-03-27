from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from mi_app.models import Product
from .forms import RegisterForm

# Create your views here.
def get_user(request):
    return HttpResponse("Hello World")
def index(request):
    return HttpResponse("<h1>Hello, world.</h1>")


def inicio(request):
    context = {
        "name": "Mario Garcia",
        "message": "Hello, world.",
        "age": 45,
        "example_list": [23, 5, 6, 7, 8, 9]
    }
    return render(request, "base.html", context=context)

def acerca_de(request):
    return render(request, "acerca_de.html")

def list_products(request):
    products = Product.objects.all()
    return render(request, "products.html",context={"products":products})
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
# Create your views here.
