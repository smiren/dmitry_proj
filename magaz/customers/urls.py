from django.urls import path
from .views import (
    MagazLoginView,
    MagazLogoutView,
    EditProfileView,
    ChangePasswordView,
    RegisterUserView,
    ProfileView,
    OrderDetailView,
    SimpleOrderCreateView,
    UserOrderCreateView,
    UserOrderListView,
)

app_name = 'customers'
urlpatterns = [
    path('login/', MagazLoginView.as_view(), name='login'),
    path('logout/', MagazLogoutView.as_view(), name='logout'),
    path('profile/register/', RegisterUserView.as_view(), name='register'),
    path('profile/edit', EditProfileView.as_view(), name='profile_edit'),
    path('profile/change', ChangePasswordView.as_view(), name='profile_change'),
    path('profile/orders', UserOrderListView.as_view(), name='profile_orders'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('order/<slug:slug>', OrderDetailView.as_view(), name='order'),
    path('simpleorder/', SimpleOrderCreateView.as_view(),
         name='simple_order_create'),
    path('userorder/', UserOrderCreateView.as_view(), name='user_order_create'),
]
