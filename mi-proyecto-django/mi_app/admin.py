from django.contrib import admin
from .models import Article  # Importa tu modelo

# Registra el modelo para que sea visible en el /admin
admin.site.register(Article)