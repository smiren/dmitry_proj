from django.urls import path
from .views import (
    ProductsListView,
    ProductsNewListView,
    ProductsListByCategoryView,
    ProductsSearchListView,
    ProductDetailView,
    PutInCartView,
    ClearCartView,
    RemoveItemCartView,
    CartView,
)

app_name = 'store'
urlpatterns = [
    path('newest/', ProductsNewListView.as_view(), name='products_new'),
    path('everything/', ProductsListView.as_view(), name='products_all'),
    path('search/', ProductsSearchListView.as_view(), name='products_search'),
    path('categories/<slug:category_slug>', ProductsListByCategoryView.as_view(),
         name='products_cat'),
    path('detail/<slug:product_slug>', ProductDetailView.as_view(),
         name='product_detail'),
    path('add/<slug:product_slug>', PutInCartView.as_view(), name='put_in_cart'),
    path('clearcart/', ClearCartView.as_view(), name='clear_cart'),
    path('remove/<slug:product_slug>', RemoveItemCartView.as_view(),
         name='remove_cart'),
    path('cart/', CartView.as_view(), name='cart'),
]
