from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from .models import InfoPages


class IndexView(TemplateView):
    template_name = 'main/index.html'


class InfoPageView(DetailView):
    template_name = 'main/infopage.html'
    model = InfoPages
    slug_url_kwarg = 'page_slug'
    context_object_name = 'page'
