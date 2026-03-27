from django.conf import settings
from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Título')
    content = models.TextField(verbose_name='Contenido')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='Autor'
    )
    published = models.BooleanField(default=False, verbose_name='Publicado')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'
        # Permisos personalizados (además de los 4 automáticos)
        permissions = [
            ('publish_article', 'Puede publicar artículos'),
            ('feature_article', 'Puede destacar artículos'),
        ]

    def __str__(self):
        return self.title
