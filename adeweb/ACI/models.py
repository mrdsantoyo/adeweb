from django.db import models
from docxtpl import DocxTemplate
from docx2pdf import convert
import subprocess
from django.conf import settings
import os

class CertificadoCalidad(models.Model):
    fecha = models.DateField(auto_now_add=True)
    cliente = models.CharField(max_length=50)
    producto = models.CharField(max_length=50)
    lote = models.IntegerField()
    clave = models.IntegerField()
    cantidad = models.FloatField()
    fecha_elaboracion = models.DateField()
    fecha_caducidad = models.DateField()
    
    mesofilicos = models.FloatField(blank=True)
    coliformes = models.FloatField(blank=True)
    e_coli = models.FloatField(blank=True)
    hongos = models.FloatField(blank=True)
    levaduras = models.FloatField(blank=True)
    salmonella_spp = models.CharField(max_length=50, blank=True)
    listeria_mono = models.CharField(max_length=50, blank=True)
    staphylococcus = models.CharField(max_length=50, blank=True)

    acidez = models.FloatField(blank=True)
    peroxidos =models.FloatField(blank=True)
    humedad = models.FloatField(blank=True)
    
    materia_extraña = models.CharField(max_length=50)
    olor = models.CharField(max_length=50)
    sabor = models.CharField(max_length=50)    
    color = models.CharField(max_length=50)
    textura = models.CharField(max_length=50)
    aspecto  = models.CharField(max_length=50)
    
    observaciones = models.TextField(blank=True)
    
    documento_word = models.FileField(upload_to='certificados/word/', blank=True)
    documento_pdf = models.FileField(upload_to='certificados/pdf/', blank=True)
    
    def __str__(self):
        return f"Certificado {self.clave} - {self.producto}"    

    
    def registrar_evento(self):
        context = {
            'cliente': self.cliente,
            'producto': self.producto,
            'lote': self.lote,
            'fecha_reporte': self.fecha,
            'clave': self.clave,
            'cantidad': self.cantidad,
            'fecha_elaboracion': self.fecha_elaboracion,
            'fecha_caducidad': self.fecha_caducidad,
            'mesofilicos': self.mesofilicos,
            'coliformes': self.coliformes,
            'e_coli': self.e_coli,
            'humedad': self.humedad,
            'materia_extraña': self.materia_extraña,
            'olor': self.olor,
            'sabor': self.sabor,
            'color': self.color,
            'textura': self.textura,
            'observaciones': self.observaciones,
        }

    def generar_y_guardar_documentos(self, context, template_path):
        """Genera y guarda los documentos Word y PDF 
        a partir de la plantilla y el contexto proporcionados."""

        try:
            doc = DocxTemplate(template_path)
            doc.render(context)
            
            word_dir = os.path.join(settings.MEDIA_ROOT, 'certificados/word/')
            pdf_dir = os.path.join(settings.MEDIA_ROOT, 'certificados/pdf/')
            os.makedirs(word_dir, exist_ok=True)
            os.makedirs(pdf_dir, exist_ok=True)
            
            base_filename = f'Certificado_{self.producto.replace(" ", "_")}_{self.lote}_{self.clave}'
            word_filename = f'{base_filename}.docx'
            pdf_filename = f'{base_filename}.pdf'
            
            word_path = os.path.join(word_dir, word_filename)
            pdf_path = os.path.join(pdf_dir, pdf_filename)
            
            doc.save(word_path)
            convert(word_path, pdf_path)
            
            self.documento_word.name = f'certificados/word/{word_filename}'
            self.documento_pdf.name = f'certificados/pdf/{pdf_filename}'
            self.save(update_fields=['documento_word', 'documento_pdf'])
            return True
        
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error generando documentos para Certificado {self.pk}: {e}")
            return False







