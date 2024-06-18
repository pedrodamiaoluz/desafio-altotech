from django.db.models.manager import Manager


class CategoriaManager(Manager):
    def get_categorias_principais(self):
        return self.get_queryset().filter(principal=True)

    def get_categorias_secundarias(self):
        return self.get_queryset().filter(principal=False)
