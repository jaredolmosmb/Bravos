from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'radar'

urlpatterns = [
	path('', views.IndexView, name =  "index"),
	path('radar', views.RadarView.as_view(), name =  "radar"),
	path('inicioPlataforma', views.InicioPlataforma.as_view(), name='inicioPlataforma'),
	path('loginJson/', views.LoginJsonView.as_view(), name='loginjson'),
	path('agregarRegistro/', views.AgregarRegistro.as_view(), name='agregarRegistro'),
	path('logout/', auth_views.LogoutView.as_view() , name='logout'),
	path('agregarRegistro2/', views.AgregarRegistro2.as_view(), name='agregarRegistro2'),
	path('cargar_usuario/', views.CreateUsuarioView, name='cargar_usuario'),

	path('listaU', views.ListaUsuariosView, name='listaU'),
	path('actualizarU/<int:pk>/', views.ActualizarUsuarios.as_view(), name='actualizarU'),
	path('eliminarU/<int:pk>/', views.EliminarUsuarios.as_view(), name='eliminarU'),

	]