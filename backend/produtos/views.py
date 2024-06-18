from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.base import View

from produtos.models import Categoria, Ingrediente, Marca

# Create your views here.

class CategoriaListView(ListView):
    template_name = 'produtos/categoria.html'
    paginate_by = 1
    context_object_name = 'produtos'

    def setup(self, request, *args, **kwargs):
        self.categoria_id = kwargs.get('categoria_id')
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return get_object_or_404(Categoria, id=self.categoria_id).produtos.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        categorias = Categoria.objects.get_categorias_secundarias()
        ingredientes = Ingrediente.objects.all()
        marcas = Marca.objects.all()

        context.update({
            'categorias': categorias,
            'ingredientes': ingredientes,
            'marcas': marcas,
        })
        return context


class CompraPorCategoriaListView(ListView):
    template_name = 'produtos/compra_por_categoria.html'
    paginate_by = 6
    context_object_name = 'categorias'

    def get_queryset(self):
        return Categoria.objects.get_categorias_principais()


class HomeView(View):
    template_name = "produtos/index.html"

    def get(self, request, *args, **kwargs):
        categorias = Categoria.objects.get_categorias_principais()
        categoria_destaque = None

        try:
            categoria_destaque = Categoria.objects.get(nome__iexact='Integrais veganas')
        except Categoria.DoesNotExist:
            messages.warning(request, 'A categoria Integrais veganas ainda não foi criada a sessâo ficará sem produtos até ela ser criada e conter produtos')

        context = {
            'categorias': categorias,
        }
        if categoria_destaque:
            context['categoria_destaque'] = categoria_destaque

        return render(request, self.template_name, context)
