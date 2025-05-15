from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import createcitasform, CreateCustomPublicUser
from django.contrib.auth import get_user_model
from .models import Appointment
from django.contrib.auth.decorators import login_required


User = get_user_model()

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': CreateCustomPublicUser
        })
    else:
        print(request.POST)
        if request.POST['password'] == request.POST['password1']:
            try:
                # registrar usuarios
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password'],
                    email=request.POST['email'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    phone=request.POST['phone'],
                    role=request.POST['role'],)
                user.save()
                return redirect('signin')
            except IntegrityError:
                return render(request, 'signin', {
                    'form': CreateCustomPublicUser,
                    "error": 'Usuario ya existe'
                })

        return render(request, 'signup.html', {
            'form': CreateCustomPublicUser,
            "error": 'Contraseñas no coinciden'
        })


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {  # <- corregido
            'form': AuthenticationForm
        })
    else:
        CustomUser = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if CustomUser is None:
            return render(request, 'signin.html', {  # <- corregido
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña es incorrecta'
            })
        else:
            login(request, CustomUser)
            return redirect('citas')


@login_required
def signout(request):
    logout(request)
    return redirect('home')

@login_required
def citas(request):
    citas = Appointment.objects.filter(
        created_by=request.user, status__isnull=False)
    return render(request, 'citas.html', {'citas': citas})


@login_required
def Citas_completed(request):
    citas = Appointment.objects.filter(
        created_by=request.user, status__isnull=True)
    return render(request, 'citas.html', {'citas': citas})

@login_required
def cita_detalle(request, cita_id):
    cita = get_object_or_404(Appointment, pk=cita_id, created_by=request.user)

    if request.method == 'GET':
        form = createcitasform(instance=cita)
        return render(request, 'cita_detalle.html', {'cita': cita, 'form': form})
    else:
        try:
            form = createcitasform(request.POST, instance=cita)
            if form.is_valid():
                form.save()
            return redirect('citas')
        except ValueError:
            return render(request, 'cita_detalle.html', {
                'cita': cita,
                'form': form,
                'error': 'Error updating Appointment'
            })

@login_required
def my_view(request):
    status_choices = Appointment.STATUS_CHOICES
    return render(request, 'my_template.html', {'status_choices': status_choices})

@login_required
def Complete_cita(request, cita_id):
    cita = get_object_or_404(Appointment, pk=cita_id, created_by=request.user)

    if request.method == 'POST':
        cita.status = 'completed'
        cita.save()
        return redirect('citas')
    
@login_required  
def Delete_cita(request, cita_id):
    cita = get_object_or_404(Appointment, pk=cita_id, created_by=request.user)

    if request.method == 'POST':
        cita.delete()
        return redirect('citas')

@login_required 
def create_citas(request):
    if request.method == 'GET':
        return render(request, 'create_citas.html', {
            'form': createcitasform()
        })
    else:
        try:
            form = createcitasform(request.POST)
            new_cita = form.save(commit=False)
            new_cita.created_by = request.user
            new_cita.save()
            return redirect('citas')
        except ValueError:
            return render(request, 'create_citas.html', {
                'form': createcitasform(),
                'error': 'Plese provide valide data'
            })
