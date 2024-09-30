from django.shortcuts import render, redirect, get_object_or_404  # Funciones para renderizar plantillas, redirigir URL
# y obtener objetos o devolver un 404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # Formularios de creación de usuario
# y autenticación
from django.contrib.auth import login, logout, authenticate  # Funciones para manejar el inicio y cierre de sesión,
# y la autenticación de usuarios
from django.contrib.auth.models import User  # Modelo de usuario proporcionado por Django
from django.db import IntegrityError  # Excepción para manejar errores de integridad en la base de datos
from django.utils import timezone  # Utilidades para manejar fechas y horas
from django.contrib.auth.decorators import login_required  # Decorador para requerir que un usuario esté autenticado
from .models import Task  # Modelo de tareas definido en la aplicación actual
from .forms import TareaForm  # Formulario de tareas definido en la aplicación actual


# Create your views here.
# Usuario =========================================================================================
def registro(request):
    """
    Muestra el formulario de registro
    """

    if request.method == 'GET':
        # Si el método es GET, se muestra el formulario
        return render(request, 'registro.html', {"form": UserCreationForm})
    else:
        if not request.POST['password1'] or not request.POST['password2']:
            # Si las contraseñas están vacías, muestra un error
            return render(request, 'registro.html', {'form': UserCreationForm,
                                                     'error': 'La contraseña no puede estar vacía'})

        if request.POST['password1'] != request.POST['password2']:
            # Si las contraseñas no coinciden, se muestra un mensaje de error
            return render(request, 'registro.html', {"form": UserCreationForm, "error": "Las contraseñas no coinciden"})

        else:
            try:
                # Si las contraseñas son iguales, se crea un nuevo usuario
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tareas')
            except IntegrityError:
                return render(request, 'registro.html', {"form": UserCreationForm,
                                                         "error": "El nombre de usuario ya existe"})


@login_required
def cerrar_sesion(request):
    """
    Cierra sesion del usuario
    """

    logout(request)
    return redirect('inicio')


def inicio(request):
    """
    Muestra la página de inicio
    """

    return render(request, 'inicio.html')


def inicio_sesion(request):
    """
    Inicia sesión
    """

    if request.method == 'GET':
        # Si el método es GET, se muestra el formulario
        return render(request, 'inicio_sesion.html', {'form': AuthenticationForm})

    else:
        # Si el método es POST, se inicia sesión
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'inicio_sesion.html',
                          {'form': AuthenticationForm, 'error': 'Nombre de usuario y/o contraseña incorrectos'})
        login(request, user)
        return redirect('tareas')


# TAREAS ==========================================================================================
@login_required
def tareas(request):
    """
    Muestra las tareas del usuario
    """

    tareas_ = Task.objects.filter(usuario=request.user, fecha_completa__isnull=True)
    return render(request, 'tareas.html', {'tareas': tareas_})


@login_required
def tareas_completas(request):
    """
    Muestra las tareas completadas
    """

    tareas_ = Task.objects.filter(usuario=request.user, fecha_completa__isnull=False).order_by('-fecha_completa')
    return render(request, 'tareas.html', {'tareas': tareas_})


@login_required
def crear_tarea(request):
    """
    Crea una nueva tarea
    """

    if request.method == 'GET':
        # Si el método es GET, se muestra el formulario
        return render(request, 'crear_tarea.html', {'form': TareaForm})
    else:
        # Si el método es POST, se crea la tarea
        try:
            form = TareaForm(request.POST)
            nueva_tarea = form.save(commit=False)
            nueva_tarea.usuario = request.user  # Corregido a 'user'
            nueva_tarea.save()
            return redirect('tareas')
        except ValueError:
            return render(request, 'crear_tarea.html', {'form': TareaForm, 'error': 'Error al crear la tarea'})


@login_required
def detalles_tarea(request, tarea_id):
    """
    Muestra los detalles de una tarea
    """
    if request.method == 'GET':
        tarea = get_object_or_404(Task, pk=tarea_id, usuario=request.user)
        form = TareaForm(instance=tarea)
        return render(request, 'detalles_tarea.html', {'tarea': tarea, 'form': form})
    else:
        try:
            tarea = get_object_or_404(Task, pk=tarea_id, usuario=request.user)
            form = TareaForm(request.POST, instance=tarea)
            form.save()
            return redirect('tareas')
        except ValueError:
            return render(request, 'detalles_tarea.html', {
                'tarea': tarea,
                'form': form,
                'error': 'Error al actualizar la tarea'})


@login_required
def tarea_completa(request, tarea_id):
    """
    Completa una tarea
    """
    tarea = get_object_or_404(Task, pk=tarea_id, usuario=request.user)
    if request.method == 'POST':
        tarea.fecha_completa = timezone.now()
        tarea.save()
        return redirect('tareas')


@login_required
def eliminar_tarea(request, tarea_id):
    """
    Elimina una tarea
    """
    tarea = get_object_or_404(Task, pk=tarea_id, usuario=request.user)
    if request.method == 'POST':
        tarea.delete()
        return redirect('tareas')
