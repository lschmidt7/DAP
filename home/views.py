from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from random import shuffle
import random

from .models import User, Vacancy

def login_context(request):
    context = {'logged' : False}
    if request.session.has_key('login'):
        username = request.session['username']
        login = request.session['login']
        logged = True
        context = {
            'login' : login,
            'username' : username,
            'logged' : logged,
        }
    return context

def isLogged(request):
    if request.session.has_key('login'):
        return True
    return False

def cities_name():
    f = open('cities/cities.txt','r')
    cities = f.readlines()
    for i in range(len(cities)):
        cities[i] = cities[i].replace('\n','')
    return cities

def bairros_name(city_name):
    bairros = []
    city_file = 'cities/'+city_name.replace(' ','').lower()+".txt"
    if(city_name!='default' and Path(city_file).is_file()):
        f = open(city_file,'r')
        bairros = f.readlines()
        for i in range(len(bairros)):
            bairros[i] = bairros[i].replace('\n','')
    return bairros

def index(request):
    context = login_context(request)
    page = 'home/login.html'
    if(context['logged']):
        page = 'home/home.html'
        cont = {
            'page_name' : 'home',
        }
        context.update(cont)
    return render(request, page, context=context)

def login(request):
    email = request.POST.get('email')
    password = request.POST.get('pass')
    reg = User.objects.filter(user_mail=email,user_password=password)
    if(len(reg)==1):
        request.session['login'] = email
        request.session['username'] = reg[0].user_first_name
        request.session.modified = True
    else:
        context={
            'aviso' : 'Email ou senha incorretos',
        }
        return render(request, 'home/login.html', context=context)
    return redirect("/home")

def logoff(request):
    if request.session.has_key('login'):
        del request.session['login']
    return redirect("/home")

def planes(request):
    context = login_context(request)
    cont = {
        'page_name' : 'planes',
    }
    context.update(cont)
    return render(request, 'home/planes.html', context=context)

def signup(request):
    context = login_context(request)
    page = 'home/signup.html'
    if(context['logged']):
        page = 'home/home.html'
    years = [x for x in range(1930,2019)] 
    cont = {
        'years' : years,
    }
    context.update(cont)
    return render(request, page, context=context)

def profile(request):
    if(isLogged(request)):
        context = login_context(request)
        infos = login_context(request)
        user_reg = User.objects.filter(user_mail=infos['login'])
        photoname = user_reg[0].user_photo
        if(photoname==""):
            photoname = "profile-photo.jpg"
        user_info = {
            'email' : user_reg[0].user_mail,
            'first_name' : user_reg[0].user_first_name,
            'last_name' : user_reg[0].user_last_name,
            'photo_name' : photoname,
            'born_year' : user_reg[0].user_born,
            'student' : user_reg[0].user_student,
            'worker' : user_reg[0].user_worker,
        }
        context.update(user_info)
        return render(request, 'home/profile.html', context=context)
    context = login_context(request)
    return render(request, 'home/login.html', context=context)

def edit_profile(request):
    context = login_context(request)
    return render(request, 'home/edit_profile.html', context=context)

def delete_profile(request):
    context = login_context(request)
    return render(request, 'home/delete_profile.html', context=context)

def deleted_profile(request):
    context = login_context(request)
    User.objects.filter(user_mail=context['login']).delete()
    if request.session.has_key('login'):
        del request.session['login']
    context = login_context(request)
    return render(request, 'home/home.html', context=context)

def register(request,city_name):
    context = login_context(request)
    if(isLogged(request)):
        cont = {
            'cities' : cities_name(),
            'city_name' : city_name,
            'bairros' : bairros_name(city_name),
        }
        context.update(cont)
        return render(request, 'home/register_immobile.html', context=context)
    return render(request, 'home/login.html', context=context)
    

def search_page(request):
    context = login_context(request)
    if(isLogged(request)):
        return render(request, 'home/search_page.html', context=context)
    return render(request, 'home/login.html', context=context)

def services(request):
    context = login_context(request)
    cont = {
        'page_name' : 'services',
    }
    context.update(cont)
    return render(request, 'home/services.html', context=context)

def about(request):
    context = login_context(request)
    cont = {
        'page_name' : 'about',
    }
    context.update(cont)
    return render(request, 'home/about.html', context=context)

def contact(request):
    context = login_context(request)
    cont = {
        'page_name' : 'contact',
    }
    context.update(cont)
    return render(request, 'home/contact.html', context=context)

def insert_user(request):
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    emailc = request.POST.get('emailc')
    senha = request.POST.get('senha')
    senhac = request.POST.get('senhac')
    born_year = request.POST.get('nascimento')
    student = request.POST.get('student')
    worker = request.POST.get('worker')
    photo = request.FILES['photo']
    fs = FileSystemStorage()
    photoname = email.replace('.','')
    photoname = photoname.replace('@','')
    photoname += "."+(photo.name.split('.')[1])
    filename = fs.save("C:/Users/Leonardo/Python/DAP/dap/home/static/images/profile-photos/"+photoname, photo)
    uploaded_file_url = fs.url(filename)
    print(uploaded_file_url)
    if(email!=emailc or senha!=senhac):
        context={
            'aviso' : 'Diferentes emails ou senhas informados',
        }
        return render(request, 'home/alert.html', context=context)
    if(not valid_email(email)):
        context={
            'aviso' : 'Email ja cadastrado',
        }
        return render(request, 'home/alert.html', context=context)
    u = User(user_mail=email,user_password=senha,user_first_name=nome,user_last_name=sobrenome,user_born=born_year,user_student=student,user_worker=worker,user_photo=photoname)
    u.save()
    return redirect("/home")

def insert_vacancy(request,id):
    tipo = request.POST.get('type')
    city = request.POST.get('city')
    bairro = request.POST.get('bairro')
    endereco = request.POST.get('endereco')
    moradores_atualmente = request.POST.get('moradores_atualmente')
    fumantes = request.POST.get('fumantes')
    estudantes = request.POST.get('estudantes')
    trabalhadores = request.POST.get('trabalhadores')
    animais = request.POST.get('animais')
    dog = request.POST.get('dog')
    cat = request.POST.get('cat')
    other = request.POST.get('other')
    v = Vacancy(vacancy_type=tipo,vacancy_city=city,vacancy_neighborhood=moradores_atualmente,user_last_name=sobrenome,user_born=born_year,user_student=student,user_worker=worker,user_photo=photoname)
    v.save()
    return redirect("/home")

def custom_search(request):
    context = login_context(request)
    cont = {
        'page_name' : 'Custom Search',
    }
    context.update(cont)
    return render(request, 'home/custom_search.html', context=context)

def list_search(request):
    context = login_context(request)
    cont = {
        'page_name' : 'List Search',
    }
    context.update(cont)
    return render(request, 'home/list_search.html', context=context)

def insert_vacancy(request):
    return redirect("/home")

def valid_email(email):
    reg = User.objects.filter(user_mail=email)
    if(len(reg))==0:
        return True
    else:
        return False


########################################################################################
##                                                                                    ##
##                                   BEGIN TEST                                       ##
##                                                                                    ##
########################################################################################


def insert_random_users(request,quantity):
    nomes = open("teste/nomes.txt").readlines()
    sobrenomes = open("teste/sobrenomes.txt").readlines()
    shuffle(nomes)
    shuffle(sobrenomes)
    email_list = [u.user_mail for u in User.objects.all()]
    for y in range(quantity):
        nome = nomes[y]
        nome = nome[0].upper()+nome[1:len(nome)]
        sobrenome = sobrenomes[y]
        senha = "1234"
        student = [False,True][random.randint(0,1)]
        worker = [False,True][random.randint(0,1)]
        years = [x for x in range(1930,2019)] 
        born_year = years[random.randint(0,len(years)-1)]
        email = nome[0].lower()+sobrenome.lower()+"@gmail.com"
        if(email not in email_list):
            email_list.append(email)
            u = User(user_mail=email,user_password=senha,user_first_name=nome,user_last_name=sobrenome,user_born=born_year,user_student=student,user_worker=worker,user_photo="")
            u.save()
    return redirect("/home")

def delete_all_users(request):
    User.objects.exclude(user_mail = 'lschmidt@inf.ufsm.br').delete()

def insert_random_properties(request,quantity):
    pass


########################################################################################
##                                                                                    ##
##                                     END TEST                                       ##
##                                                                                    ##
########################################################################################