from django.shortcuts import get_list_or_404
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.list import ListView
from django.contrib.auth.views import LogoutView, SuccessURLAllowedHostsMixin
from django.contrib import messages
from django.db.models import Q
from django.utils.http import is_safe_url
from django.http import HttpResponseRedirect
from .models import Product, Category
from .cart import Cart


class ProductsListView(ListView):
    template_name = 'store/products_list.html'
    context_object_name = 'products'
    queryset = Product.show.all()
    paginate_by = 6
    paginate_orphans = 2
    extra_context = {
        'title_name': 'Каталог товаров',
        'headline_name': 'Каталог всех товаров',
    }


class ProductsNewListView(ProductsListView):
    extra_context = {
        'title_name': 'Каталог новинок',
        'headline_name': 'Каталог новинок',
    }

    def get_queryset(self):
        return super().get_queryset().filter(new=True)


class ProductsListByCategoryView(ProductsListView):

    def get_queryset(self):
        slug = self.kwargs.get('category_slug')
        if slug:
            return get_list_or_404(super().get_queryset(), category__slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['category_slug'])
        context.update({
            'title_name': category.name,
            'headline_name': f'Каталог товаров категории "{category.name}"',
        })
        return context


class ProductsSearchListView(ProductsListView):

    def get_queryset(self):
        keyword = self.request.GET['search']
        kw_for_category = keyword.lower().capitalize()
        q = Q(name__icontains=keyword) | Q(description__icontains=keyword) \
            | Q(category__name__istartswith=kw_for_category)
        return super().get_queryset().filter(q) if keyword else []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET['search']
        context.update({
            'title_name': 'Поиск товаров',
            'headline_name': f'Поиск товаров по словосочетанию "{keyword}"',
        })
        return context


class ProductDetailView(SuccessURLAllowedHostsMixin, DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    slug_url_kwarg = 'product_slug'
    redirect_field_name = 'next'

    def get_next_page(self):
        next_page = "/"
        if self.redirect_field_name in self.request.GET:
            next_page = self.request.GET.get(self.redirect_field_name)
            url_is_safe = is_safe_url(
                url=next_page,
                allowed_hosts=self.get_success_url_allowed_hosts(),
                require_https=self.request.is_secure(),
            )
            next_page = next_page if url_is_safe else "/"
        return next_page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_page_url'] = self.get_next_page()
        if self.object:
            context['images'] = self.object.images.all()
        return context


class CartView(TemplateView):
    template_name = 'store/cart.html'


class PutInCartView(SingleObjectMixin, LogoutView):
    """
    Дерзкий способ добавить товар в корзину с помощью CBV.
    Чтобы положить товар в корзину нас устраивает функционал класса LogoutView,
    совмесно в примесью SingleObjectMixin, для получения товара по слагу.
    Переопределяем метод dispatch, в котором получаем товар укладываем его
    в корзину(вместо логаута у предка), далее по согласованиям редиректим по
    пораметру next, либо по LOGOUT_REDIRECT_URL, в этом случае методы get или
    post не вызываются.
    """
    model = Product
    slug_url_kwarg = 'product_slug'

    def dispatch(self, request, *args, **kwargs):
        self.cart = Cart(request)
        self.cart_action()
        next_page = self.get_next_page()
        return HttpResponseRedirect(next_page) if next_page \
            else super().dispatch(request, *args, **kwargs)

    def cart_action(self):
        product = self.get_object()
        quantity = self.request.GET.get('quantity')
        if quantity:
            self.cart.add(
                product=product,
                quantity=int(quantity),
                update=True,
            )
            messages.success(self.request, f"Количество товара \
            \"{product.name}\" изменено на {quantity}")
        else:
            self.cart.add(product)
            messages.success(self.request, f"\"{product.name}\" \
            добавлен в корзину")


class ClearCartView(PutInCartView):

    def cart_action(self):
        self.cart.clear()
        messages.success(self.request, "Корзина очищена")


class RemoveItemCartView(PutInCartView):

    def cart_action(self):
        product = self.get_object()
        self.cart.remove(product)
        messages.success(self.request, f"{product.name} удален из корзины")
