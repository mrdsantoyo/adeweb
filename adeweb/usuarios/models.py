from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib import messages    


# Create your models here.
EMPRESA = [
    ('DILUSA', 'Dilusa'),
    ('KRONCHIS', 'Kronchis'),
    ('DILUSAEXPRESS', 'Dilusa Express'),
    ('FRIGORIFICO', 'Frigorífico'),
    ('IGLU', 'Iglu Alimentos'),
    ]

UBICACION = [
    ('CDINDUSTRIAL', 'Cd. Industrial'),
    ('AMERICAS', 'Américas'),
    ('AGROPECUARIO', 'AGROPECUARIO'), 
    ]

DEPARTAMENTO = [
    ('ADMINISTRACION_PUBLICA', 'Administración Pública'),
    ('ADMINISTRACION_LOCAL', 'Administración Local'),
    ('TI', 'Tecnología de la Información'),
    ('CONTABILIDAD', 'Contabilidad'),
    ('CAPITAL_HUMANO', 'Capital Humanos'),
    ('SGIA', 'SGIA'),
    ('GOP', 'Gerencia de Operaciones'),
    ]

class CustomUser(AbstractUser):
    departamento = models.CharField(choices=DEPARTAMENTO, max_length=100)
    jefe_directo = models.ManyToManyField(settings.AUTH_USER_MODEL, max_length=100)
    ubicacion = models.CharField(max_length=100, blank=True)
    empresa = models.CharField(choices=EMPRESA, max_length=100)

    def __str__(self):
        return self.username

