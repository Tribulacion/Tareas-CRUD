"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tareas import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('admin/', admin.site.urls),
    path('registro/', views.registro, name='registro'),
    path('tareas/', views.tareas, name='tareas'),
    path('tareas_completas/', views.tareas_completas, name='tareas_completas'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('crear_tarea/', views.crear_tarea, name='crear_tarea'),
    path('tarea/<int:tarea_id>', views.detalles_tarea, name='detalles_tarea'),
    path('tarea/<int:tarea_id>/completar', views.tarea_completa, name='completar_tarea'),
    path('tarea/<int:tarea_id>/eliminar', views.eliminar_tarea, name='eliminar_tarea'),
]
