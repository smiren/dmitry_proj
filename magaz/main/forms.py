from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(
        required=False, max_length=20, label='Поиск товаров')
