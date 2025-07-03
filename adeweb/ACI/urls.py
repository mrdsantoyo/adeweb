from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.aci_home, name='aci_home'),  # Vista principal de ACI
    path('generar_certificado/', views.generar_certificado, name='generar_certificado'),
    ]

