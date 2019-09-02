from django.contrib.auth.forms import AuthenticationForm
from .models import InfoPages
from .forms import SearchForm
from store.models import Category
from store.cart import Cart

def main_app(request):
    context = {}
    context['info_pages'] = InfoPages.objects.all()
    context['categories'] = Category.objects.all()
    context['login_form'] = AuthenticationForm()
    search_keyword = request.GET.get('search',  '')
    context['search_form'] = SearchForm(initial={'search':search_keyword})
    context['cart'] = Cart(request)

    context['search_url'] = ''
    context['back_url'] = ''
    if request.GET.get('search'):
        context['search_url'] = '?search=' + request.GET.get('search')
        context['back_url'] = context.get('search_url')
    if request.GET.get('page', 1) != 1:
        context['back_url'] += '&page=' if context['back_url'] else '?page='
        context['back_url'] += request.GET.get('page')
    return context
