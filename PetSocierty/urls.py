"""
URL configuration for PetSocierty project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path ('', views.home, name='home'),
    path ('signup/', views.signup, name='signup' ),
    path ('citas/', views.citas, name='citas'),
    path ('citas/create', views.create_citas, name='create_citas'),
    path ('citas/<int:cita_id>/', views.cita_detalle, name='cita_detalle'),
    path ('citas/<int:cita_id>/complete', views.Complete_cita, name='complete_cita'),
    path ('citas/<int:cita_id>/delete', views.Delete_cita, name='delete_cita'),
    path ('logout/', views.signout , name='logout'),
    path('signin/', views.signin , name='signin'),
]
 