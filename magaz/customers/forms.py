from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import ExtUser, UserOrder

class EditProfileForm(forms.ModelForm):
	email = forms.EmailField(required=True,
		label='Адрес электронной почты')

	class Meta:
		model = ExtUser
		fields = ('username', 'email', 'first_name', 'last_name',
				  'phone', 'address')

class RegisterUserForm(forms.ModelForm):
	email= forms.EmailField(required=True,
		label='Адрес электронной почты')
	password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
		help_text = password_validation.password_validators_help_text_html())
	password2 = forms.CharField(label='Пароль(повторно)',
		widget=forms.PasswordInput,
		help_text = 'Введите пароль еще раз для проверки')

	def clean_password1(self):
		password = self.cleaned_data['password1']
		if password:
			password_validation.validate_password(password)
		return password


	def clean(self):
		pass1 = self.cleaned_data.get('password1', '')
		pass2 = self.cleaned_data.get('password2', '')
		email = self.cleaned_data.get('email', '')
		not_unique_email = ExtUser.objects.filter(email=email)
		super().clean()
		if pass1 and pass2 and pass1 != pass2:
			error = ValidationError(
				'Введенные пароли не совпадают', code='password_mismatch')
			self.add_error('password2', error)
		if email and not_unique_email:
			error = ValidationError(
				'Адрес почты %(email)s уже используется другим пользователем',
				code='email_not_uniq', params = {'email':email})
			self.add_error('email', error)

	class Meta:
		model = ExtUser
		fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name',
				  'phone', 'address')

UserOrderForm = forms.modelform_factory(UserOrder,
	fields=('phone', 'address', 'comment', 'user',),
	widgets={'user': forms.HiddenInput},
)
