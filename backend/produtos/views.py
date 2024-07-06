from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.base import View
from django.db.models import Q
from produtos.models import (
    Categoria,
    Ingrediente,
    Marca,
    Produto,
    SubCategoria
)

# Create your views here.

CATEGORIA_QUANTIDADE_POR_PAGINA = 3
SUB_CATEGORIA_QUANTIDADE_POR_PAGINA = 9
COMPRE_POR_CATEGORIA_QUANTIDADE_POR_PAGINA = 9
PRODUTO_QUANTIDADE_POR_PAGINA = 15


class CategoriaListView(ListView):
    template_name = 'produtos/categoria.html'
    paginate_by = CATEGORIA_QUANTIDADE_POR_PAGINA
    context_object_name = "sub_categorias"

    def setup(self, request, *args, **kwargs):
        self.categoria_slug = kwargs.get('categoria_slug', '')
        self.categoria = get_object_or_404(Categoria, slug=self.categoria_slug)
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return self.categoria.sub_categorias.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({
            'categorias': Categoria.objects.all(),
            'categoria_selecionada': self.categoria,
        })
        return context


class SubCategoriaListView(ListView):
    template_name = 'produtos/categoria_detalhe.html'
    paginate_by = SUB_CATEGORIA_QUANTIDADE_POR_PAGINA
    context_object_name = 'produtos'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_filtro = ''
        self.categoria = None
        self.sub_categoria = None
        self.sub_categoria_slug = ''
        self.categoria_slug = ''

    def setup(self, request, *args, **kwargs):
        self.categoria_slug = kwargs.get('categoria_slug', '')
        self.categoria = get_object_or_404(Categoria, slug=self.categoria_slug)
        self.sub_categoria_slug = kwargs.get('sub_categoria_slug', '')
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        self.sub_categoria = get_object_or_404(SubCategoria,
                                               slug=self.sub_categoria_slug)
        return self.sub_categoria.produtos.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        categoria_sub_categorias = self.categoria.sub_categorias.exclude(
            slug=self.sub_categoria.slug)

        ingredientes = Ingrediente.objects.all()
        marcas = Marca.objects.all()
        sub_categorias = SubCategoria.objects.exclude(
            slug=self.sub_categoria.slug)

        context.update({
            'categorias': sub_categorias,
            'sub_categorias': categoria_sub_categorias,
            'ingredientes': ingredientes,
            'marcas': marcas,
            'sub_categoria_selecionada': self.sub_categoria,
            'categoria': self.categoria
        })
        return context

    def get_paramentros_para_juntar_com_a_paginacao(self, **listas):
        """
            Adiciona os parametros de filtro na url para manter o filtro quando
            ouver paginação.
        """
        for key, lista in listas.items():
            for item in lista:
                self.url_filtro += f'&{key}={item}'

    def converter_para_lista_de_inteiros(self, lista: list):
        """
            Converte os elementos de uma lista de strings para inteiros se
            possível caso contrario o elememento é removido.
        """
        if not lista:
            return None

        for pos, item in enumerate(lista):
            try:
                lista[pos] = int(item)
            except ValueError:
                lista.remove(item)

        return lista

    def get(self, request, *args, **kwargs):

        filtro_queryset = None

        # pegando os valores dos checkboxes para filtrar os produtos
        filtro_categorias = request.GET.getlist('categorias', None)
        filtro_ingredientes = request.GET.getlist('ingredientes', None)
        filtro_marcas = request.GET.getlist('marcas', None)

        filtro_categorias = self.converter_para_lista_de_inteiros(
            filtro_categorias)
        if filtro_categorias:
            # adicionando a filtragem por categoria na variável de filtro
            filtro_queryset = Q(categorias__id__in=filtro_categorias)
            self.get_paramentros_para_juntar_com_a_paginacao(
                categorias=filtro_categorias)

        filtro_ingredientes = self.converter_para_lista_de_inteiros(
            filtro_ingredientes)
        if filtro_ingredientes:
            # adicionando a filtragem por ingredientes na variável de filtro
            filtro_queryset &= Q(ingredientes__id__in=filtro_ingredientes)
            self.get_paramentros_para_juntar_com_a_paginacao(
                ingredientes=filtro_ingredientes, )

        filtro_marcas = self.converter_para_lista_de_inteiros(filtro_marcas)
        if filtro_marcas:
            # adicionando a filtragem por marcas na variável de filtro
            filtro_queryset &= Q(marca_id__in=filtro_marcas)
            self.get_paramentros_para_juntar_com_a_paginacao(
                marcas=filtro_marcas)

        if filtro_queryset:
            produtos = self.get_queryset().filter(filtro_queryset)
            context = self.get_context_data(object_list=produtos)

            context.update({
                'filtro_categorias':
                filtro_categorias,
                'filtro_ingredientes':
                filtro_ingredientes,
                'filtro_marcas':
                filtro_marcas,
                'url_filtro_com_paginacao':
                self.url_filtro
            })

        return render(request, self.template_name, context)


class CompraPorCategoriaListView(ListView):
    template_name = 'produtos/compra_por_categoria.html'
    paginate_by = COMPRE_POR_CATEGORIA_QUANTIDADE_POR_PAGINA
    context_object_name = 'categorias'

    def get_queryset(self):
        return Categoria.objects.all()


class HomeView(View):
    template_name = "produtos/index.html"

    def get(self, request, *args, **kwargs):
        categorias = Categoria.objects.all()
        context = {
            'categorias': categorias,
        }

        categoria_destaques = SubCategoria.objects.filter(destaque=True)
        if categoria_destaques.exists():
            categoria_destaque = categoria_destaques.first()
            context['categoria_destaque'] = categoria_destaque
            context['produtos_destaques'] = categoria_destaque.produtos.all()[
                :5]
        else:
            messages.warning(
                request,
                ('A categoria destaque ainda não foi criada a sessâo ficará'
                    'sem produtos até ela ser criada e conter produtos')
            )

        return render(request, self.template_name, context)


class ProdutoListView(ListView):
    template_name = "produtos/produtos.html"
    context_object_name = 'produtos'
    paginate_by = PRODUTO_QUANTIDADE_POR_PAGINA

    def setup(self, request, *args, **kwargs):
        self.search = request.GET.get("search", None)
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return Produto.objects.search(self.search)
