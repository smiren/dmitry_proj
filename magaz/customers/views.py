from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView,
)
from django.contrib.auth import login
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from main.utils import CREATE_ORDER_MSG
from .models import (
    ExtUser, BaseOrder, SimpleOrder, OrderPosition, StaffComment, UserOrder
)
from .forms import EditProfileForm, RegisterUserForm, UserOrderForm
from store.cart import Cart


class MagazLoginView(LoginView):
    template_name = 'accounts/login.html'


class MagazLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/logout.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/detail.html'


class EditProfileView(SuccessMessageMixin, LoginRequiredMixin,
                      UpdateView):
    model = ExtUser
    template_name = 'profile/edit.html'
    extra_context = {'headline': 'Редактирование профиля'}
    form_class = EditProfileForm
    success_url = reverse_lazy('customers:profile')
    success_message = "Данные %(username)s профиля успешно изменены"

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class ChangePasswordView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'profile/edit.html'
    extra_context = {'headline': 'Сменить пароль'}
    success_url = reverse_lazy('customers:profile')
    success_message = 'Пароль успешно изменён'


class RegisterUserView(SuccessMessageMixin, CreateView):
    model = ExtUser
    template_name = 'accounts/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('customers:profile')
    success_message = "Пользователь %(username)s успешно зарегистрирован"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        # Флаг для будующей email валидации учетной записи
        user.is_activated = False
        user.save()
        login(self.request, user)
        return super().form_valid(form)


class OrderDetailView(DetailView):
    model = BaseOrder
    context_object_name = 'order'
    template_name = 'orders/order_detail.html'

    def get_object(self, **kwargs):
        obj = super().get_object(**kwargs)
        if obj.is_simple():
            return obj.simpleorder
        return obj.userorder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['positions'] = self.object.positions.all()
            context['comments'] = self.object.staffcomments.all()
        return context


class SimpleOrderCreateView(SuccessMessageMixin, CreateView):
    model = SimpleOrder
    fields = ('name', 'email', 'phone', 'address', 'comment')
    template_name = 'orders/order_create.html'
    success_message = "%(order)s успешно сформирован, наш менеждер свяжится с \
						вами в ближайшее время."

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, order=self.object)

    def form_valid(self, form):
        cart = Cart(self.request)
        self.object = form.save()
        cart_positions = []
        for position in cart.objects_iter():
            cart_positions.append(OrderPosition(order=self.object, **position))
        self.object.positions.bulk_create(cart_positions)
        self.object.save(update_fields=['total_cost'], set_total_cost=True)
        self.object.staffcomments.create(comment=CREATE_ORDER_MSG)
        cart.clear()
        return super().form_valid(form)


class UserOrderCreateView(LoginRequiredMixin, SimpleOrderCreateView):
    model = UserOrder
    form_class = UserOrderForm
    fields = None

    def get_initial(self):
        initial = self.initial.copy()
        initial.update({
            'user': self.request.user.id,
            'phone': self.request.user.phone,
            'address': self.request.user.address,
        })
        return initial


class UserOrderListView(LoginRequiredMixin, ListView):
    template_name = 'profile/orders.html'
    model = UserOrder
    context_object_name = 'orders'
    paginate_by = 5
    paginate_orphans = 1

    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user.id)
