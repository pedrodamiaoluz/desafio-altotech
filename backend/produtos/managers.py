from django.db.models.manager import Manager
from django.db.models import Q


class ProdutoManager(Manager):
    def search(self, value):
        """ busca produtos por nome, marca, ingrediente ou categoria """
        queryset = self.get_queryset()
        if value:
            return queryset.filter(
                Q(nome__icontains=value) |
                Q(marca__nome__icontains=value) |
                Q(ingredientes__nome__icontains=value) |
                Q(categorias__nome__icontains=value))
        return queryset
