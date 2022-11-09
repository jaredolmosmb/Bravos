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
import numpy as np # Allow us to work with arrays
import warnings
warnings.filterwarnings('ignore') # Allow to disable Python warnings
import math # Allow us to perform mathematical tasks
from datetime import datetime # Allow us to get the current date and current time
import matplotlib.pyplot as plt # Allow us to customize scatterplots
from soccerplots.radar_chart import Radar
import matplotlib.font_manager
import textwrap
from soccerplots.utils import add_image
import matplotlib.colors as mcolors # Allow us create colormap objects from a list of colors
from io import StringIO
import chardet
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.

@authenticated_user
def IndexView(request):
	return render (request, 'radar/index.html')

@authenticated_user
def ListaUsuariosView(request):
    todos_u=CustomUser.objects.all()
    return render(request, 'radar/listaUsuarios.html', {'todos_u': todos_u})

class ActualizarUsuarios(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'radar/modU.html'
    success_url = reverse_lazy('radar:listaU')

class EliminarUsuarios(DeleteView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'radar/u_confirm_delete.html'
    success_url = reverse_lazy('radar:listaU')

class RadarView(View):

    """
    funcion para probar el radar utilizando el paso de variables segun la seleccion de jugadores
    """
    """
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
    """

    def post(self, request):
        players = Player.objects.all()
        form = ReaderForm(request.POST or None, request.FILES or None)

        if form.is_valid():

            file = form.cleaned_data.get('file')
            file2 = form.cleaned_data.get('file2')
            #print('file: ', file)
            #print("type(file): ", type(file))

            obj = form.save(commit=False)
            obj.file = file
            obj.file2 = file2
            obj.save()

            try:
                with open(obj.file.path, 'rb') as f:
                    result = chardet.detect(f.read())
                with open(obj.file2.path, 'rb') as f:
                    result = chardet.detect(f.read())
            except:
                return render(request, 'radar/radar.html', {'form': form, 'players': players})

            #Here is the google colab script
            # change display to print so it can work properly

            # 1.1 Define the Variables
            v_position = "Centerbacks" # <-- Please edit this value according to the position of the soccer player to be analized (e.g. Goalkeeper, Midfielder, striker, etc)
            v_soccerplayer = "Chema Rodriguez" # <-- Please edit this value according to the soccer player full name

            # 1.2 Loading the dataset of all the players of Liga MX
            df_allplayers_ligamx = pd.read_excel(open(obj.file2.path,'rb'))
            #df_allplayers_ligamx = pd.read_excel('https://github.com/julioe-perezlara/FC_Juarez/blob/master/Datasets/promedioligamx_centrales_11_5_21.xlsx?raw=True') # Read an excel file from internet (Github) 
            #print('Liga MX %s dataset' %(v_position)) 
            #print(df_allplayers_ligamx) # Display the dataset of al players of Liga MX

            # 1.3 Loading the dataset of the soccer player to be compared
            df_player = pd.read_excel(open(obj.file.path,'rb'))
            #df_player = pd.read_excel('https://github.com/julioe-perezlara/FC_Juarez/blob/master/Datasets/jonas_ramalho_11_5_21.xlsx?raw=True') # Read an excel file from internet (Github)
            #print('\n%s dataset' %(v_soccerplayer))
            #print(df_player) # Display the dataset of a single player

            # 1.4 Get the name of all the columns
            ls_allplayers_ligamx_columnsname = df_allplayers_ligamx.columns.to_list() # Get the names of all the columns in "All-soccer players dataset"
            #print('\nVariables de intéres:\n')
            #for x in ls_allplayers_ligamx_columnsname:   # For-loop iterates over all the column names
              #print(x) 

            # %s     This operator lets Python add a String value into a string. In this case, %s stores the name and role of the soccer player

            #---------------------------STEP 2------------------------------
            #This is step 2 Calculate the mean of each variable for the "All-soccer players dataset" and merge dataframes
            # Change of display to print so the app works properly 
            # Change directory to save tabla comparativa.xlsx

            # 2.1 Calculate the average/mean of each colum
            df_allplayers_ligamx_mean = pd.DataFrame(df_allplayers_ligamx.mean().tolist())  # Calculate the mean of each column in "All-soccer players dataset" and Transform the values into a Dataframe

            # 2.2 Transpose the dataframe
            df_allplayers_ligamx_mean = df_allplayers_ligamx_mean.T # Swap rows by columns

            # 2.3 Rename automatically the name of the columns 
            col_rename_dict = {i:j for i, j in zip(df_allplayers_ligamx_mean.columns.tolist(),ls_allplayers_ligamx_columnsname[1:])} 
            # |--Create a Python dictionary to equal the column names of the "All-soccer players mean data" and the column names of soccer player dataset
            df_allplayers_ligamx_mean.rename(columns=col_rename_dict, inplace=True) # Replace the column names value 

            # 2.4 Add a column to the "All-soccer players mean dataset"
            df_allplayers_ligamx_mean.insert(0, "Jugador", ["Promedio Liga Mx"]) #add column
            #print('\nAverage of all %s in Liga MX:\n' %(v_position))
            #print(df_allplayers_ligamx_mean) # Display the dataset that contains the mean of each variable for all soccer players

            # 2.5 Concatenate the dataframes
            df_radarchart = df_player.append(df_allplayers_ligamx_mean, ignore_index=True) # Merge ""All-soccer players mean dataframe" with "Single soccer player dataframe"
            #print('\n\nRadar chart dataframe (Comparative):\n')
            #print(df_radarchart)
            df_radarchart.to_excel(r'C:\Users\artur\prueba\Bravos\tabla comparativa.xlsx',index=False)

            #--------------------------------------STEP 3---------------------------------
            # change display to prints to a proper functionality
            # Get parameters
            list_param = list(df_radarchart.columns)
            list_param = list_param[1:]

            # Wrap the values of the columns
            rg_param = []
            for x in list_param:
              a = textwrap.fill(x, 20)
              rg_param.append(a)

            #print(rg_param)

            # Get variables
            player1 = df_radarchart.iloc[0, 0]
            player2 = df_radarchart.iloc[1, 0]
            #print('\n\n')
            #print(player1)
            #print(player2)

            # Step 3: Visualizing the data and looking for outliers (part 1)

            # Plotting a Histogram for each feature
            n_row = 4                                              # Define the number of rows that will be displaying in the final output, which in this case is 3
            n_col = 4                                              # Define the number of columns that will be displaying in the final output, which in this case is 3.
            fig, axes = plt.subplots(n_row, n_col, figsize=(15,14))    # This function allows to customize the X-axis, Y-axis and size of the figure 
            for i in range(df_allplayers_ligamx.shape[1]-1):                     # For-loop iterates over all columns found in the 'Country' dataframe with the exception of feature "Country"
              df_allplayers_ligamx.iloc[:,i+1].plot.hist(bins=20, ax=axes[math.floor(i/n_row), i-n_col*math.floor(i/n_row)], title=df_allplayers_ligamx.columns.values[i+1])
              # Plot a Histogram with the specified parameters for each attribute starting by column 1 and including all rows (country feature is ignored)

              #df_allplayers_ligamx.iloc[:,i+1].plot(kind='kde', ax=axes[math.floor(i/n_row), i-n_col*math.floor(i/n_row)], secondary_y=True)

            plt.tight_layout()   # Adjust the histograms to avoid misplacings or pairing.
            #plt.show()           # Display the current figure that you are working on

            # df.Shape[1]               This function is used to get the total number of columns in a dataframe
            # df.iloc[row>,<column>]    This function is used to select a particular cell of a dataframe. (Selecting rows and columns by number)
            # df.plt.hist()             This function is used to plot a histogram
            # math.floor()              This function is used to round numbers down to the nearest integer (e.g. 20.6 -> 20)
            # df.columns.values         This function is used to get all columns name as an array


            #---------------------------------STEP 4 ----------------------------------
            # Find the Minimum a Maximum value

            # add ranges to list of tuple pairs
            ranges = [] # define an empty list
            a_values = []
            b_values = []

            # For-loop over parameters
            for x in list_param:
              a = df_allplayers_ligamx[list_param][x].quantile(0.05)  # Get minimum value of our parameter list.
              #b = min(df_allplayers_ligamx[list_param][x])  # Get maximum value of our parameter list.
              #a = a - (a*.25) # Substracting 25% of the minum value

              b = df_allplayers_ligamx[list_param][x].quantile(0.95)
              #b = max(df_allplayers_ligamx[list_param][x])  # Get maximum value of our parameter list.
              #b = b + (b*.25) # Substracting 25% of the minum value

              ranges.append((a,b)) # Add all values in our ranges lists 

            for y in range(len(df_radarchart['Jugador'])):
              if df_radarchart['Jugador'][y] == player1:
                a_values = df_radarchart.iloc[y].values.tolist() # Get all values of Diego Rolan and put them in a list
              if df_radarchart['Jugador'][y] == player2:
                b_values = df_radarchart.iloc[y].values.tolist() # Get all values of the average of strikers and put them in a list

            a_values = a_values[1:]
            b_values = b_values[1:]

            values = [a_values, b_values]

            # Print the values
            #print(values)
            #print(ranges)

            # Get the Current Date
            today_date = str(datetime.today().strftime('%m-%d-%Y'))

            # Set the parameter of the Radar Chart

            title = dict(
                title_name = player1,
                title_color ='green',
                subtitle_name ='Ultimo Año',
                subtitle_color ='green',
                title_name_2 = player2,
                subtitle_name_2 ='Ultimo añ0',
                subtitle_color_2 ='red',
                title_color_2 = 'red',
                title_fontsize = 20,
                subtitle_fontsize = 15
            )

            #notas = '\nVisualization made by: Joel Burrola\nAll units are in per90'

            #-----------------------------LAST STEP--------------------------------------
            ## instantiate object -- changing fontsize
            ## make a subplot

            import matplotlib.font_manager
            fig, ax = plt.subplots(figsize=(15, 11))

            radar = Radar(label_fontsize=10, range_fontsize=8, fontfamily="Arial", label_color="#030000")
            fig, ax = radar.plot_radar(ranges=ranges, params=rg_param, values=values,
                                      radar_color=['green','red'],
                                      alphas=[.7,.4],
                                      figax=(fig,ax),
                                      title=title,
                                      #endnote=notas,
                                      end_size=12,
                                      end_color="#121212",
                                      compare=True,
                                      filename="C:/Users/artur/prueba/Bravos/%s_%s_radarchart_%s.pdf" %(player1,player2, today_date) # Replace this value with your Google Drive path
                                      )

            #plt.show()                                                                  # Display the current figure that you are working on
            ## add image 
            #fig = add_image(image="/content/drive/MyDrive/Colab_Notebooks/fcjuarez.png", fig=fig, left=0.464, bottom=2, width=0.1, height=1)
            imgdata = StringIO()
            #fig.set_size_inches(8, 6)
            fig.savefig(imgdata, format='svg')
            imgdata.seek(0)
            data = imgdata.getvalue()

            return render(request, 'radar/radar.html', {'form': form, 'players': players, 'graph': data})

    def get(self, request):
        players = Player.objects.all()
        form = ReaderForm(request.POST or None, request.FILES or None)
        return render(request, 'radar/radar.html', {'form':form, 'players': players})

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