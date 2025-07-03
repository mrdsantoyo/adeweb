from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from .models import DEPARTAMENTO

def validar_contraseña(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

# Formulario para crear usuarios personalizados
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    departamento = forms.ChoiceField(choices=DEPARTAMENTO, required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    jefe_directo = forms.ChoiceField(choices=DEPARTAMENTO, required=False, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'departamento', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email
    
# Formulario para actualizar usuarios personalizados
from django.contrib.auth.forms import UserChangeForm
from django import forms
from .models import CustomUser

class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    departamento = forms.ChoiceField(choices=DEPARTAMENTO, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    jefe_directo = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_superuser=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Seleccione un jefe directo"  # Añade esto
    )
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 
                'departamento', 'jefe_directo', 'ubicacion')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)
        # Asegúrate de que el queryset esté actualizado
        self.fields['jefe_directo'].queryset = CustomUser.objects.filter(is_superuser=True)


