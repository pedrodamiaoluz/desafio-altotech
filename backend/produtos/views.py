from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse
from django.views.generic import ListView
from django.views.generic.base import View

from produtos.models import Categoria, Ingrediente, Marca, Produto

# Create your views here.


class CategoriaListView(ListView):
    template_name = 'produtos/categoria.html'
    paginate_by = 9
    context_object_name = 'produtos'

    def setup(self, request, *args, **kwargs):
        self.categoria_id = kwargs.get(
            'categoria_id'
        )  # da pra pega a categoria ja aqui e lança not found
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return get_object_or_404(
            Categoria, id=self.categoria_id).produtos.all().order_by("nome")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        categorias = Categoria.objects.get_categorias_secundarias()
        ingredientes = Ingrediente.objects.all()
        marcas = Marca.objects.all()

        context.update({
            'categorias': categorias,
            'ingredientes': ingredientes,
            'marcas': marcas,
            'categoria_id': self.categoria_id,
        })
        return context

    def get_paramentros_para_juntar_com_a_paginacao(self, **listas):
        for key, lista in listas.items():
            for item in lista:
                self.url_filtro += f'&{key}={item}'


    def converter_para_lista_de_inteiros(self, lista: list):
        if not lista:
            return None

        for pos, item in enumerate(lista):
            try:
                lista[pos] = int(item)
            except ValueError:
                lista.remove(item)

        return lista

    def get(self, request, *args, **kwargs):
        produtos = self.get_queryset()
        self.url_filtro = ''

        filtro_categorias = request.GET.getlist('categorias', None)
        filtro_ingredientes = request.GET.getlist('ingredientes', None)
        filtro_marcas = request.GET.getlist('marcas', None)

        filtro_categorias = self.converter_para_lista_de_inteiros(
            filtro_categorias)
        if filtro_categorias:
            produtos = produtos.filter(
                categorias__id__in=filtro_categorias).distinct()
            self.get_paramentros_para_juntar_com_a_paginacao(
                categorias=filtro_categorias,
            )

        filtro_ingredientes = self.converter_para_lista_de_inteiros(
            filtro_ingredientes)
        if filtro_ingredientes:
            produtos = produtos.filter(
                ingredientes__id__in=filtro_ingredientes).distinct()
            self.get_paramentros_para_juntar_com_a_paginacao(
                ingredientes=filtro_ingredientes,
            )

        filtro_marcas = self.converter_para_lista_de_inteiros(filtro_marcas)
        if filtro_marcas:
            produtos = produtos.filter(marca_id__in=filtro_marcas).distinct()
            self.get_paramentros_para_juntar_com_a_paginacao(
                marcas=filtro_marcas,
            )

        context = self.get_context_data(object_list=produtos)
   
        context.update({
            'filtro_categorias': filtro_categorias,
            'filtro_ingredientes': filtro_ingredientes,
            'filtro_marcas': filtro_marcas,
            'url_filtro_com_paginacao':self.url_filtro if self.url_filtro else ''
        })

        return render(request, self.template_name, context)


class CompraPorCategoriaListView(ListView):
    template_name = 'produtos/compra_por_categoria.html'
    paginate_by = 9
    context_object_name = 'categorias'

    def get_queryset(self):
        return Categoria.objects.get_categorias_principais().order_by('nome')


class HomeView(View):
    template_name = "produtos/index.html"

    def get(self, request, *args, **kwargs):
        categorias = Categoria.objects.get_categorias_principais().order_by('nome')
        context = {
            'categorias': categorias,
        }

        try:
            categoria_destaque = Categoria.objects.get(
                nome__iexact='Integrais veganas')
            context['categoria_destaque'] = categoria_destaque
            context['produtos_destaques'] = categoria_destaque.produtos.all(
            )[:5]

        except Categoria.DoesNotExist:
            messages.warning(
                request,
                'A categoria Integrais veganas ainda não foi criada a sessâo ficará sem produtos até ela ser criada e conter produtos'
            )

        return render(request, self.template_name, context)
