from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import Post, TTUser, Comment
from .apps import user_registered


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {'author': forms.HiddenInput, 'post': forms.HiddenInput}


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    class Meta:
        model = TTUser
        fields = ['username', 'email', 'first_name', 'last_name', 'send_message']


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Электронная почта')
    password1 = forms.CharField(label='Пароль',
                widget=forms.PasswordInput,
                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль',
                widget=forms.PasswordInput,
                help_text='Введите второй раз для проверки')
    
    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1
    
    def clean(self):
        super(RegisterUserForm, self).clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
              'Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = TTUser
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'send_message')



