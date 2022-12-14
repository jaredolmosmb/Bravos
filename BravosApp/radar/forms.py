from django import forms
#from operadores.models import Operadores, ImageId, ImageDomicilio
#from .models import OperadoresModel, TiposDocOperadoresModel, DocumentosModel
#from .models import Usuario
from django.contrib.auth.models import Group
from django.db.models import Q
import datetime
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

from .models import CustomUser

class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ['file', 'file2']
        labels = {
            'file': _('Selecciona el archivo de jugador comparar'),
            'file2': _('Selecciona el archivo de promedio comparar'),
        }
        
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'name')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'name')
        
"""class RegistroForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input90', 'placeholder':'Password', 'id':'password2'}))
	class Meta:
		model = Usuario
		fields = ['first_name','last_name','email', 'telefono', 'password','groups']#'__all__','celular', 'empresa', 'num_empleados'
		groups = forms.ModelMultipleChoiceField(queryset=Group.objects.filter(~Q(name = "admin")))
		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'input90', 'placeholder':'Nombre', 'id':'nombre'}),
			'last_name': forms.TextInput(attrs={'class': 'input90', 'placeholder':'Apellidos', 'id':'apellidos'}),
			'email': forms.TextInput(attrs={'class':'input90', 'placeholder':'Email/Usuario', 'id':'email2'}),
			'telefono': forms.TextInput(attrs={'class':'input90', 'placeholder':'Celular', 'id':'telefono'}),

			#'groups': forms.ModelMultipleChoiceField(queryset=Group.objects.filter(~Q(name = "admin")))
			'groups' : forms.CheckboxSelectMultiple()
			#'groups' : forms.SelectMultiple()
			}

	def __init__(self, *args, **kwargs):
		super(RegistroForm, self).__init__(*args, **kwargs)
		self.fields['first_name'].label = ''
		self.fields['last_name'].label = ''
		self.fields['email'].label = ''
		self.fields['telefono'].label = ''
		self.fields['password'].label = ''
		self.fields['groups'].label = 'Tipo'
		self.fields['groups'].queryset = Group.objects.filter(~Q(name = "admin") & ~Q(name = "general"))
		self.fields['groups'].help_text = ''
"""
class LoginForm(forms.Form):
	email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Usuario', 'id':'email'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password', 'id':'password'}))

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['email'].label = ''
		self.fields['password'].label = ''
"""
class Registro2Form(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input90', 'id':'password2'}))
	class Meta:
		model = Usuario
		fields = ['first_name','last_name','email', 'telefono', 'password']#
		fields = '__all__'
		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'input90', 'id':'nombre'}),
			'last_name': forms.TextInput(attrs={'class': 'input90', 'id':'apellidos'}),
			'email': forms.TextInput(attrs={'class':'input90', 'id':'email2'}),
			'telefono': forms.TextInput(attrs={'class':'input90', 'id':'telefono'}),
			}

	def __init__(self, *args, **kwargs):
		super(Registro2Form, self).__init__(*args, **kwargs)
		self.fields['first_name'].label = 'Nombre'
		self.fields['last_name'].label = 'Apellidos'
		self.fields['email'].label = 'Email/Usuario'
		self.fields['telefono'].label = 'Telefono'
		self.fields['password'].label = 'Password'
		"""