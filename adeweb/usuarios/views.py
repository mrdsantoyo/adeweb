from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import CustomUserCreationForm, CustomUserChangeForm 
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
    return redirect('usuarios:logout') 

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('home') 
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'editar_perfil.html', {'form': form})


