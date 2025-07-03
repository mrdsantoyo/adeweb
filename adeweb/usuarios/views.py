from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from .forms import CustomUserCreationForm, CustomUserChangeForm 
from .models import CustomUser
from django.contrib import messages


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Registro exitoso! Puedes iniciar sesión.')
            return redirect('usuarios:login')
        else:
            pass

    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)

            if remember == 'on':
                request.session.set_expiry(1209600)
            else:
                request.session.set_expiry(0)

            next_url = request.POST.get('next') or 'home'
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'login.html')

@login_required
def home(request):
    context = {
        'fullname': request.user.first_name + ' ' + request.user.last_name,
    }
    return render(request, 'home.html', context)

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('usuarios:login')

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        # Crear copia mutable del POST data
        post_data = request.POST.copy()

        if not post_data.get('jefe_directo'):
            post_data['jefe_directo'] = None

        user_form = CustomUserChangeForm(post_data, instance=request.user)
        password_form = None

        # Verificar si se enviaron datos de contraseña
        if post_data.get('password1') or post_data.get('password2'):
            password_form = PasswordChangeForm(
                user=request.user,
                data={
                    'old_password': post_data.get('old_password', ''),
                    'new_password1': post_data.get('password1', ''),
                    'new_password2': post_data.get('password2', '')
                }
            )

        # Validar formularios
        if user_form.is_valid():
            user = user_form.save(commit=False)
            
            # Validar y guardar contraseña si es necesario
            if password_form:
                if password_form.is_valid():
                    password_form.save()
                    update_session_auth_hash(request, request.user)
                    messages.success(request, 'Perfil y contraseña actualizados correctamente.')
                else:
                    # Agregar errores de contraseña al formulario principal
                    for field, errors in password_form.errors.items():
                        for error in errors:
                            messages.error(request, f"Error en contraseña: {error}")
                    return render(request, 'usuarios:editar_perfil.html', {
                        'form': user_form,
                        'jefes': CustomUser.objects.filter(is_superuser=True)
                    })
            else:
                messages.success(request, 'Perfil actualizado correctamente.')

            user.save()
            return redirect('home')  # Usando namespace

        else:
            # Mostrar errores de validación
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")

    else:
        # Método GET - mostrar formularios
        user_form = CustomUserChangeForm(instance=request.user)

    return render(request, 'editar_perfil.html', {
        'form': user_form,
        'jefes': CustomUser.objects.filter(is_superuser=True)
    })








