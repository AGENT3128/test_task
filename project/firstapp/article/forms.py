from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
#from django.core.exceptions import ValidationError
from . models import Author
from django.core.exceptions import ValidationError

'''
Класс CustomUserCreationForm описывает форму представления страницы регистрации
'''
class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(label='Введите логин', min_length=4, max_length=150)
    email = forms.EmailField(label='Введите email')
    age = forms.IntegerField(label='Введите возраст')
    password1 = forms.CharField(label='Введите пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)
    list = [(gen, gen) for gen in ['Man', 'Woman']]
    gender = forms.CharField(label='Выберете пол', widget=forms.Select(attrs=None, choices=list))
    class Meta:
        model = Author
        fields = ['username', 'email', 'age', 'password1', 'password2', 'gender']
    def clean_username(self):
        username = self.cleaned_data['username']
        r = Author.objects.filter(username=username)
        if r.count():
            raise  forms.ValidationError("Username already exists")

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        r = Author.objects.filter(email=email)
        if r.count():
            raise  forms.ValidationError("Email already exists")
        return email

    def clean_gender(self):
        gender = self.cleaned_data['gender']
        r = Author.objects.filter(gender=gender)

        return gender

    def clean_age(self):
        age = self.cleaned_data['age']
        r = Author.objects.filter(age=age)
        #r = User.objects.filter(age=age)

        return age

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = Author(

            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['age'],
            self.cleaned_data['password1'],

        )


        return user


class CustomUserCreationFormTest(forms.Form):
    locations = forms.ModelChoiceField(
        queryset=Author.objects.values_list("username", flat=True).distinct(),
        empty_label=None, label='username'
    )