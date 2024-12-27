from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['first_name'].label = 'Имя'
        self.fields['email'].label = 'Электронная почта'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Повтор пароля'

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })


class EmailLoginForm(forms.Form):
    email = forms.EmailField(label='Электронная почта')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_cache = None  # здесь будем хранить найденного пользователя

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            UserModel = User
            try:
                # Ищем пользователя по email
                user_obj = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist:
                raise forms.ValidationError("Неверные учетные данные (email).")
            else:
                # Аутентифицируем, подставляя username из найденного объекта
                user = authenticate(
                    username=user_obj.username,
                    password=password
                )
                if user is None:
                    raise forms.ValidationError("Неверный пароль.")
                self.user_cache = user
        return cleaned_data

    def get_user(self):
        return self.user_cache
