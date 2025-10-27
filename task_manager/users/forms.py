from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        min_length=8
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput,
        min_length=8
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Имя пользователя'}
        )
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Имя'}
        )
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Фамилия'}
        )
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Пароль'}
        )
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Подтверждение пароля'}
        )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        help_texts = {
            'username': '',
            'first_name': '',
            'last_name': '',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username)
        if user.exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "Пользователь с таким именем уже существует."
                )
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if not password1 or not password2:
            raise forms.ValidationError(
                "Для подтверждения введите, пожалуйста, пароль ещё раз."
                )
        if password1 != password2:
            raise forms.ValidationError(
                "Введенные пароли не совпадают."
                )
        if len(password1) < 8:
            raise forms.ValidationError(
                "Ваш пароль должен содержать как минимум 8 символа."
                )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        max_length=150,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                    'placeholder': 'Имя пользователя'}
        )
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
            'placeholder': 'Пароль'}
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})