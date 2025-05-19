from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import createcitasform, CreateCustomPublicUser, AppointmentForm
from django.contrib.auth import get_user_model
from .models import Appointment
from django.contrib.auth.decorators import login_required
from .models import Pet
from .forms import PetForm

User = get_user_model()

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
                    "error": 'User already exists'
                })

        return render(request, 'signup.html', {
            'form': CreateCustomPublicUser,
            "error": 'Passwords do not match'
        })

# Ingreso de usuarios
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        # Validacion de Password
        CustomUser = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if CustomUser is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, CustomUser)
            return redirect('citas')


@login_required
# Logout
def signout(request):
    logout(request)
    return redirect('home')


@login_required
# Listar citas credas
def citas(request):
    citas = Appointment.objects.filter(
        created_by=request.user, status__isnull=False)
    return render(request, 'citas.html', {'citas': citas})


@login_required
# Filtra solo las citas que fueron creadas por el usuario
def Citas_completed(request):
    citas = Appointment.objects.filter(
        created_by=request.user, status__isnull=True)
    return render(request, 'citas.html', {'citas': citas})


@login_required
# Asegura que el usuario solo pueda acceder y editar sus propias citas.
def cita_detalle(request, cita_id):
    cita = get_object_or_404(Appointment, pk=cita_id, created_by=request.user)
    # Muestra un formulario con los datos actuales (GET).
    if request.method == 'GET':
        form = createcitasform(instance=cita)
        return render(request, 'cita_detalle.html', {'cita': cita, 'form': form})
    else:
        try:
            #Procesa la actualización cuando se envía el formulario (POST).
            form = createcitasform(request.POST, instance=cita)
            if form.is_valid():
                form.save()
            return redirect('citas')
        except ValueError:
            #Maneja errores mostrando un mensaje si falla la actualización.
            #Redirige a la lista de citas después de actualizar correctamente.
            return render(request, 'cita_detalle.html', {
                'cita': cita,
                'form': form,
                'error': 'Error updating Appointment'
            })


@login_required
# Obtiene las opciones de estado.
def my_view(request):
    status_choices = Appointment.STATUS_CHOICES
    return render(request, 'my_template.html', {'status_choices': status_choices})


@login_required
#vista que permite marcar una cita como completada, y solo si esa cita pertenece al usuario autenticado.
def Complete_cita(request, cita_id):
    cita = get_object_or_404(Appointment, pk=cita_id, created_by=request.user)

    if request.method == 'POST':
        cita.status = 'completed'
        cita.save()
        return redirect('citas')


@login_required
#Vista en Django para eliminar una cita específica que pertenece al usuario
def Delete_cita(request, cita_id):
    cita = get_object_or_404(Appointment, pk=cita_id, created_by=request.user)

    if request.method == 'POST':
        cita.delete()
        return redirect('citas')


@login_required
# Vista para crear una nueva cita (Appointment) vinculada a las mascotas del usuario autenticado.
def create_citas(request):
    pets = Pet.objects.filter(owner=request.user)
    if not pets.exists():
        return render(request, 'create_citas.html', {'no_pets': True})

    if request.method == 'GET':
        form = AppointmentForm()
        form.fields['pet'].queryset = pets
        return render(request, 'create_citas.html', {'form': form})

    form = AppointmentForm(request.POST)
    form.fields['pet'].queryset = pets
    if form.is_valid():
        cita = form.save(commit=False)
        cita.created_by = request.user
        cita.save()
        return redirect('citas')
    return render(request, 'create_citas.html', {'form': form})



@login_required
# Filtra y obtiene todas las mascotas (Pet) que pertenecen al usuario autenticado (request.user)
def pets(request):
    pets = Pet.objects.filter(owner=request.user)
    return render(request, 'pets.html', {'pets': pets})


@login_required
#Es una vista para crear una nueva mascota (Pet) asociada al usuario autenticado:
    #En GET muestra el formulario vacío.
def create_pet(request):
    if request.method == 'GET':
        return render(request, 'create_pet.html', {
            'form': PetForm()
        })
    else:
        try:
           #En POST intenta crear la mascota y asigna el usuario como dueño.
            form = PetForm(request.POST)
            new_pet = form.save(commit=False)
            new_pet.owner = request.user
            new_pet.save()
            return redirect('pets')
        except ValueError:
            # Si falla, vuelve a mostrar el formulario con un error.
            # Redirige a la lista de mascotas tras guardar con éxito.
            return render(request, 'create_pet.html', {
                'form': PetForm(),
                'error': 'Invalid Data'
            })


@login_required
# Es una vista para mostrar y editar los datos de una mascota específica que pertenece al usuario autenticado.
    # Solo permite acceder a la mascota si es del usuario actual.
def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id, owner=request.user)
    # En GET muestra el formulario para editar con datos actuales.
    if request.method == 'GET':
        form = PetForm(instance=pet)
        return render(request, 'pet_detail.html', {'form': form, 'pet': pet})
    else:
        try:
            #En POST intenta actualizar la mascota con los datos enviados.
            form = PetForm(request.POST, instance=pet)
            form.save()
            return redirect('pets')
        except ValueError:
            return render(request, 'pet_detail.html', {
                'form': form,
                'pet': pet,
                # En caso de error, muestra un mensaje.
                'error': 'Error updating pet'
            })


@login_required
# Elimina una mascota que pertenece al usuario autenticado.
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id, owner=request.user)
    if request.method == 'POST':
        pet.delete()
        return redirect('pets')
