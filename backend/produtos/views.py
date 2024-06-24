from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.base import View

from produtos.models import Categoria, Ingrediente, Marca, SubCategoria

# Create your views here.


class CategoriaListView(ListView):
    template_name = 'produtos/categoria.html'
    paginate_by = 3
    context_object_name ="sub_categorias"

    def setup(self, request, *args, **kwargs):
        self.categoria_slug = kwargs.get(
            'categoria_slug'
        )       
        self.categoria = get_object_or_404(Categoria,slug=self.categoria_slug)
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return self.categoria.sub_categorias.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({
            'categorias': Categoria.objects.all().order_by("nome"),
            'categoria_selecionada': self.categoria,
            
        })
        return context

# falta exibir as subcategorias que estão na mesma categoria
class SubCategoriaListView(ListView):
    template_name = 'produtos/categoria_detalhe.html'
    paginate_by = 1
    context_object_name = 'produtos'

    def setup(self, request, *args, **kwargs):
        self.categoria_slug = kwargs.get(
            'categoria_slug'
        )  # da pra pega a categoria ja aqui e lança not found
        self.categoria = get_object_or_404(Categoria, slug=self.categoria_slug)
        self.sub_categoria_slug = kwargs.get(
            'sub_categoria_slug'
        )
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        self.sub_categoria =  get_object_or_404(
            SubCategoria, slug=self.sub_categoria_slug)
        return self.sub_categoria.produtos.all().order_by("nome")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        sub_categorias = SubCategoria.objects.all()
        ingredientes = Ingrediente.objects.all()
        marcas = Marca.objects.all()

        context.update({
            'sub_categorias': sub_categorias,
            'ingredientes': ingredientes,
            'marcas': marcas,
            'sub_categoria_selecionada': self.sub_categoria,
            'categoria': self.categoria
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
        return Categoria.objects.all().order_by('nome')


class HomeView(View):
    template_name = "produtos/index.html"

    def get(self, request, *args, **kwargs):
        categorias = Categoria.objects.all().order_by('nome')
        context = {
            'categorias': categorias,
        }

        categoria_destaques = SubCategoria.objects.filter(destaque=True).order_by('nome')
        if categoria_destaques.exists():
            categoria_destaque = categoria_destaques.first()
            context['categoria_destaque'] = categoria_destaque
            context['produtos_destaques'] = categoria_destaque.produtos.all(
            )[:5]
        else:
            messages.warning(
                request,
                'A categoria destaque ainda não foi criada a sessâo ficará sem produtos até ela ser criada e conter produtos'
            )

        return render(request, self.template_name, context)