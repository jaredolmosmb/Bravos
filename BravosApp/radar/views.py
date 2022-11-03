from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import *
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import messages 
from .decorators import authenticated_user
import pandas as pd
from .utils import get_plot, get_radar, get_radar2

# Create your views here.

@authenticated_user
def IndexView(request):
	return render (request, 'radar/index.html')

class RadarView(View):
    def post(self, request):
        value_1 = request.POST.get("seleccion1")
        value_2 = request.POST.get("seleccion2")
        p1 = Player.objects.get(id = int(value_1))
        p2 = Player.objects.get(id = int(value_2))
        players = Player.objects.all()
        categories = []
        for indx, field in enumerate(Player._meta.fields):
            if indx>2:
                categories.append(str(field.name))
        categories.append('')

        player1 = [p1.games_played, p1.minutes_played, p1.yellow_cards]
        player2 = [p2.games_played, p2.minutes_played, p2.yellow_cards]

        print('categories', categories)
        print('player1', player1)
        print('player2', player2)
        x= [x.name for x in players]
        y= [y.games_played for y in players]

        name1 = p1.name
        name2 = p2.name

        chart = get_radar2(categories, player1, player2, name1, name2)
        ronaldo = 'Ronaldo'

        return render(request, 'radar/radar.html', {'players': players, 'p1': p1, 'p2': p2, 'chart': chart})

    def get(self, request):
        players = Player.objects.all()
        return render(request, 'radar/radar.html', {'players': players})

class InicioPlataforma(View):
    def get(self, request):
        #registroForm = RegistroForm()
        loginForm = LoginForm()
        return render(request, 'radar/inicioPlataforma.html', {  'loginForm': loginForm})

class LoginJsonView(View):
    def post(self, request):

        loginForm = LoginForm(request.POST)
        json_stuff = {"success": 0}
        if loginForm.is_valid():
            user = authenticate(username=loginForm.cleaned_data.get(
                'email'), password=loginForm.cleaned_data.get('password'))
        if user:
            login(request, user)
            request.session['usuario'] = None
            json_stuff["success"] = 1
        json_stuff = JsonResponse(json_stuff, safe=False)
        return HttpResponse(json_stuff, content_type='application/json')

class AgregarRegistro(View):
    def post(self, request):
        registroForm = RegistroForm(request.POST)
        if registroForm.is_valid():
            usuario = registroForm.save()
            usuario.set_password(registroForm.cleaned_data.get('password'))
            usuario.username = usuario.email
            #grupo = Group.objects.get(name=registroForm.cleaned_data.get('grupo'))
            # usuario.groups.add(grupo)
            usuario.save()
            json_stuff = JsonResponse({"success": 1}, safe=False)
            return HttpResponse(json_stuff, content_type='application/json')
        else:
            json_stuff = JsonResponse({"success": 0}, safe=False)
        return HttpResponse(json_stuff, content_type='application/json')

@authenticated_user
def CreateUsuarioView(request):
    
    if request.method == 'POST':
        registroForm = CustomUserCreationForm(request.POST) 
        if registroForm.is_valid():
            usuario = registroForm.save()
            usuario.save()
            registroForm.save()
            return(redirect('radar:index2'))
        else:
        
            return render(request, 'radar/cargarUsuario.html', {'registroForm':registroForm})
            #return HttpResponse("""El formulario está mal, favor verifica que los datos esten correctos o que la imagen no pese mas de 10MB recarga en <a href = "javascript:history.back()"> Recargar </a>""")
    else:
        registroForm = CustomUserCreationForm()
        return render(request, 'radar/cargarUsuario.html', {'registroForm':registroForm})

class AgregarRegistro2(View):
    def post(self, request):
        registroForm = CustomUserCreationForm(request.POST)
        if registroForm.is_valid():
            usuario = registroForm.save()
            #grupo = Group.objects.get(name=registroForm.cleaned_data.get('grupo'))
            # usuario.groups.add(grupo)
            usuario.save()
            json_stuff = JsonResponse({"success": 1}, safe=False)
            return HttpResponse(json_stuff, content_type='application/json')
        else:
            print("entre en el else de agregarregistro")
            json_stuff = JsonResponse({"success": 0}, safe=False)
        return HttpResponse(json_stuff, content_type='application/json')