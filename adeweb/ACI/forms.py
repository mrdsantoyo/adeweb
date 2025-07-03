from django import forms
from .models import CertificadoCalidad


class DateInput(forms.DateInput):
    input_type = 'date'

class CertificadoCalidadForm(forms.ModelForm):
    class Meta:
        model = CertificadoCalidad
        exclude = ['producto', 'mesofilicos', 'coliformes', 'e_coli', 'hongos', 'levaduras', 
                'salmonella_spp', 'listeria_mono' ,'staphylococcus', 'acidez', 'peroxidos', 
                'humedad', 'materia_extraña', 'olor', 'sabor', 'color', 'textura', 'aspecto']

    widgets = {
        'fecha': DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Fecha de elaboración',
        }),
        'cliente': forms.TextInput(attrs={              
            'class': 'form-control',
            'placeholder': 'Nombre del cliente',
        }),
        'lote': forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de lote',
            'id':'id_lote'
        }),
        'clave': forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Clave',
            'id':'id_clave',
        }),
        'cantidad': forms.NumberInput(attrs={   
            'class': 'form-control',
            'placeholder': 'Cantidad',
            'step': '0.01', 
        }),
        'observaciones': forms.Textarea(attrs={        
            'class': 'form-control',
            'placeholder': 'Observaciones',
            'rows': 5,
        }),
        'documento_word': forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.doc,.docx',
        }),
        'documento_pdf': forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf',
        }),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadir etiquetas más descriptivas
        self.fields['documento_word'].label = 'Documento Word'
        self.fields['documento_pdf'].label = 'Documento PDF'






