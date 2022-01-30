import http.client

import django.views.generic
from django.utils import timezone
from django.shortcuts import render
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
#from article.models import Article
from django.views.generic import ListView
import sqlite3

from django.contrib.auth.models import User
from django.conf import settings
from django import db
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.db.models import Q

from . forms import CustomUserCreationForm,CustomUserCreationFormTest
from . models import Author

# Create your views here.
def home(request):
    return render(request,"home.html")

class SignUp(CreateView):

    form_class = CustomUserCreationForm
    #success_url = reverse_lazy("login")


    template_name = 'registration/signup.html'

def search(request):
    try:
        sqlite_connection = sqlite3.connect('my_db.sqlite3')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT * from auth_user"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Всего строк:  ", len(records))
        print("Вывод каждой строки")
        for row in records:
            print("ID:", row[0])
            print("Имя:", row[4])
            print("Email:", row[6])
            print("Возраст:", row[11])
            print("Гендер:", row[12])

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


    return render(request, "search.html")



def userlistview(request):

    test = Author.objects.all()
    return render(request, "search.html", {'test': test})

'''
Функция register подкючена к к форме CustomUserCreationForm, в которой происходит запись в таблцу Author 
и обрабатывается ошибка неправильной формы ответа, ошибка обрабатывается скриптом в html форме
'''

def register(request):
    form = CustomUserCreationForm(request.POST or None)

    if request.method == 'GET':
        context = {'form': form}
        return render(request, 'register.html', context)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            u = Author(
                request.POST['username'],
                request.POST['email'],
                request.POST['age'],
                request.POST['password1'],
                request.POST['gender'],


            )
            u.save()

            return redirect('home')
        else:

            #ValidationError(('Invalid value'))


            print("Unable to save. Form is not valid")
            print(form.errors)


    else:
        form = ErrForm()


    return render(request, "register.html", {"form": form})






class test(ListView):
    model = Author
    template_name = 'test.html'

    def get_queryset(self): # новый
        query = self.request.GET.get('q')
        if query is None:

            redirect('test')

        else:
            object_list = Author.objects.filter(
                Q(username__icontains=query) | Q(email__icontains=query)
            )
            # print(query)
            # print('########')
            # print(object_list)
            return object_list