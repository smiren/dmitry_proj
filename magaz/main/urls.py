from django.urls import path
from .views import IndexView, InfoPageView

app_name = 'main'
urlpatterns = [
	path('', IndexView.as_view(), name='index'),
	path('<slug:page_slug>/', InfoPageView.as_view(), name='infopage'),
]
