from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login
from mi_app.models import Product,Article
from .forms import RegisterForm, ArticleForm

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
def practica_permisos(request):
    return render(request, "practica_permisos.html")

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
@login_required
def article_list(request):
    """Cualquier usuario autenticado puede ver la lista."""
    articles = Article.objects.filter(published=True)
    return render(request, 'practica_permisos.html', {'articles': articles})


# --- Requiere permiso específico ---
@permission_required('mi_app.add_article', raise_exception=True)
def article_create(request):
    """Solo usuarios con permiso 'add_article' pueden crear."""
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Artículo creado.')
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'article_form.html', {'form': form})


# --- Requiere login + permiso (combinados) ---
@login_required
@permission_required('mi_app.delete_article', raise_exception=True)
def article_delete(request, pk):
    """Solo usuarios con permiso 'delete_article' pueden eliminar."""
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Artículo eliminado.')
        return redirect('article_list')
    return render(request, 'article_confirm_delete.html', {'article': article})


# --- Permiso personalizado ---
@permission_required('mi_app.publish_article', raise_exception=True)
def article_publish(request, pk):
    """Solo Editores pueden publicar artículos."""
    article = get_object_or_404(Article, pk=pk)
    article.published = True
    article.save()
    messages.success(request, f'"{article.title}" ha sido publicado.')
    return redirect('article_list')
@login_required
@permission_required('mi_app.change_article', raise_exception=True)
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'article_form.html', {'form': form, 'article': article})