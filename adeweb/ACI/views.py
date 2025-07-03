from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import JsonResponse
from .models import CertificadoCalidad
from .forms import CertificadoCalidadForm
from dashboard.plotly_dash1.ACI.load_aci import dfs
import pandas as pd
import os
from django.conf import settings
from docxtpl import DocxTemplate
from docx2pdf import convert
import datetime

def global_df():
    df_concat = pd.concat(dfs)
    df_concat.columns = df_concat.columns.str.strip(' ')
    df_filtrado = df_concat.dropna(subset='Clave')
    return df_filtrado

GLOBAL_DF = global_df()

@login_required
def generar_certificado(request):
    # Obtener clave y lote desde los parámetros de la solicitud
    clave = request.GET.get('clave')
    lote = request.GET.get('lote')
    
    if not clave or not lote:
        return JsonResponse({
            "encontrado": False,
            "mensaje": "Debe proporcionar clave y lote"
        })
    
    try:
        # Convertir a enteros
        clave = int(float(clave))
        lote = int(float(lote))
    except (ValueError, TypeError):
        return JsonResponse({
            "encontrado": False,
            "mensaje": "La clave y el lote deben ser valores numéricos"
        })

    try:
        # Filtrar por clave y lote
        resultado = GLOBAL_DF[(GLOBAL_DF['Clave'] == clave) & (GLOBAL_DF['Lote'] == lote)]
        
        if resultado.empty:
            return JsonResponse({
                "encontrado": False,
                "mensaje": f"No se encuentra Lote {lote} o Clave {clave} del producto. Revisa que estén escritos correctamente."
            })
        
        df = resultado.iloc[0, :].copy()  # Usamos .copy() para evitar problemas de vista
        tipo_producto = df['Hoja']
        
        certificado_data = {
            'cliente': request.GET.get('cliente', ''),  # Valor del formulario o vacío
            'producto': df.get('Producto', ''),
            'lote': lote,
            'fecha_reporte': datetime.date.today(),
            'clave': clave,
            'cantidad': float(request.GET.get('cantidad', 0)),  # Valor del formulario o 0
            'fecha_elaboracion': datetime.datetime.strptime(request.GET.get('fecha_elaboracion', '2025-01-01'), '%Y-%m-%d').date(),
            'fecha_caducidad': datetime.datetime.strptime(request.GET.get('fecha_caducidad', '2025-12-31'), '%Y-%m-%d').date(),
            'mesofilicos': 0,
            'coliformes': 0,
            'e_coli': 0,
            'hongos': 0,
            'levaduras': 0,
            'salmonella_spp': "AUSENTE",
            'listeria_mono': "AUSENTE",
            'staphylococcus': "AUSENTE",
            'acidez': 0,
            'peroxidos': 0,
            'humedad': 0,
            'materia_extraña': "CUMPLE",
            'olor': "CUMPLE",
            'sabor': "CUMPLE",
            'color': "CUMPLE",
            'textura': "CUMPLE",
            'aspecto': "CUMPLE",
            'observaciones': "Producto que cumple con los parámetros establecidos en la NOM-213-SSA1-2018.",
        }
        
        # Seleccionar la plantilla según el tipo de producto
        template_name = f"certificado_{tipo_producto.lower().replace(' ', '_')}.docx"
        template_path = os.path.join(settings.BASE_DIR, 'plantillas', template_name)
        
        # Si no existe la plantilla específica, usar la plantilla general
        if not os.path.exists(template_path):
            template_path = os.path.join(settings.BASE_DIR, 'plantillas/certificado.docx')
        
        # Procesar datos específicos según el tipo de producto
        if tipo_producto == "CHICHARRÓN PRENSADO":
            certificado_data.update({
                'mesofilicos': float(df.get('Mesofilicos\n<10,000 UFC/g', 0)) if pd.notna(df.get('Mesofilicos\n<10,000 UFC/g')) else 0,
                'coliformes': float(df.get('Coliformes \n<10 UFC/g', 0)) if pd.notna(df.get('Coliformes \n<10 UFC/g')) else 0,
                'e_coli': float(df.get('E. coli \n<10 UFC/g', 0)) if pd.notna(df.get('E. coli \n<10 UFC/g')) else 0,
                'hongos': float(df.get('Hongos\n<10 UFC/g', 0)) if pd.notna(df.get('Hongos\n<10 UFC/g')) else 0,
                'levaduras': float(df.get('Levaduras\n<10 UFC/g', 0)) if pd.notna(df.get('Levaduras\n<10 UFC/g')) else 0,
                'humedad': float(df.get('% Humedad', 0)) if pd.notna(df.get('% Humedad')) else 0,

                'olor': "Característico a carne de cerdo frita, exento de olores extraños, rancidez y/o de descomposición." if df.get('Olor') == "CUMPLE" else str(df.get('Olor', '')),
                'sabor': "Característico a carne de cerdo frita, exento de sabores extraños y/o descomposición." if df.get('Sabor') == "CUMPLE" else str(df.get('Sabor', '')),
                'color': "Café rojizo, característico del producto." if df.get('Color') == "CUMPLE" else str(df.get('Color', '')),
                'aspecto': "Rugosa, firme al tacto." if df.get('Aspecto') == "CUMPLE" else str(df.get('Aspecto', ''))
            })

        elif tipo_producto == "PELLET":
            certificado_data.update({
                'mesofilicos': float(df.get('Mesofilicos\n<10,000 UFC/g', 0)) if pd.notna(df.get('Mesofilicos\n<10,000 UFC/g')) else 0,
                'coliformes': float(df.get('Coliformes \n<10 UFC/g', 0)) if pd.notna(df.get('Coliformes \n<10 UFC/g')) else 0,
                'e_coli': float(df.get('E. coli \n<10 UFC/g', 0)) if pd.notna(df.get('E. coli \n<10 UFC/g')) else 0,
                'humedad': float(df.get('% Humedad', 0)) if pd.notna(df.get('% Humedad')) else 0,
                
                'olor': "Característico a manteca y condimentos." if df.get('Olor') == "CUMPLE" else str(df.get('Olor', '')),
                'sabor': "Característico a cuero de cerdo condimentado." if df.get('Sabor') == "CUMPLE" else str(df.get('Sabor', '')),
                'color': "Tonalidades marrón claro a obscuro." if df.get('Color') == "CUMPLE" else str(df.get('Color', '')),
                'aspecto': "Aceitoso y firme al tacto." if df.get('Aspecto') == "CUMPLE" else str(df.get('Aspecto', ''))
            })

        elif tipo_producto == "MANTECA":
            certificado_data.update({
                'mesofilicos': float(df.get('Cta. Total Mesofilicos \n<10,000 UFC/g', 0)) if pd.notna(df.get('Cta. Total Mesofilicos \n<10,000 UFC/g')) else 0,
                'coliformes': float(df.get('Cta. Total Coliformes \n<10 UFC/g', 0)) if pd.notna(df.get('Cta. Total Coliformes \n<10 UFC/g')) else 0,
                'e_coli': float(df.get('Cta. Total E. coli \n<10 UFC/g', 0)) if pd.notna(df.get('Cta. Total E. coli \n<10 UFC/g')) else 0,
                'hongos': float(df.get('Cta. Total Hongos\n<10 UFC/g', 0)) if pd.notna(df.get('Cta. Total Hongos\n<10 UFC/g')) else 0,
                'levaduras': float(df.get('Cta. Total Levaduras\n<10 UFC/g', 0)) if pd.notna(df.get('Cta. Total Levaduras\n<10 UFC/g')) else 0,
                'salmonella_spp': "AUSENTE" if pd.notna(df.get('Salmonella spp.\nAUSENTE/25g')) and df.get('Salmonella spp.\nAUSENTE/25g') == "AUSENTE" else "PRESENTE",
                'listeria_mono': "AUSENTE" if pd.notna(df.get('Listeria monocytogenes\nAUSENTE/25g')) and df.get('Listeria monocytogenes\nAUSENTE/25g') == "AUSENTE" else "PRESENTE",
                'staphylococcus': "AUSENTE" if df.get('Staphylococcus aureus\n<10 UFC/g', 0) == 0 else str(df.get('Staphylococcus aureus\n<10 UFC/g')),
                
                'acidez': float(df.get('Indice de acidez (%)', 0)) if pd.notna(df.get('Indice de acidez (%)')) else 0,
                'peroxidos': float(df.get('Indice de peróxidos', 0)) if pd.notna(df.get('Indice de peróxidos')) else 0,
                
                'olor': "Característico a grasa de cerdo frita." if df.get('Olor') == "CUMPLE" else str(df.get('Olor', '')),
                'sabor': "Característico a grasa de cerdo frita." if df.get('Sabor') == "CUMPLE" else str(df.get('Sabor', '')),
                'color': "Blanco marfil a beige, característica del producto." if df.get('Color') == "CUMPLE" else str(df.get('Color', '')),
                'aspecto': "Cremosa, homogénea, suave y viscosa." if df.get('Aspecto') == "CUMPLE" else str(df.get('Aspecto', '')),
            })

        elif tipo_producto == "AHUMADOS":
            certificado_data.update({
                'mesofilicos': float(df.get('Cta. Total Mesofilicos \n<10,000 UFC/g', 0)) if pd.notna(df.get('Cta. Total Mesofilicos \n<10,000 UFC/g')) else 0,
                'coliformes': float(df.get('Cta. Total Coliformes \n<10 UFC/g', 0)) if pd.notna(df.get('Cta. Total Coliformes \n<10 UFC/g')) else 0,
                'e_coli': float(df.get('Cta. Total E. coli \n<10 UFC/g', 0)) if pd.notna(df.get('Cta. Total E. coli \n<10 UFC/g')) else 0,
                
                'olor': "Característico a carne de cerdo ahumada y cocida." if df.get('Olor') == "CUMPLE" else str(df.get('Olor', '')),
                'sabor': "Característico a carne de cerdo ahumada." if df.get('Sabor') == "CUMPLE" else str(df.get('Sabor', '')),
                'color': "Café del exterior y rosa del interior, característico del producto." if df.get('Color') == "CUMPLE" else str(df.get('Color', '')),
                'aspecto': "Suave y carnosa." if df.get('Aspecto') == "CUMPLE" else str(df.get('Aspecto', '')),
            })

        elif tipo_producto == "CARNE PARA HAMBURGUESA Y MOLIDA":
            certificado_data.update({
                'coliformes': float(df.get('Cta. Total Coliformes \n<5000 UFC/g', 0)) if pd.notna(df.get('Cta. Total Coliformes \n<5000 UFC/g')) else 0,
                'e_coli': float(df.get('Cta. Total E. coli \n<5000 UFC/g', 0)) if pd.notna(df.get('Cta. Total E. coli \n<5000 UFC/g')) else 0,
                'salmonella_spp': "AUSENTE" if pd.notna(df.get('Salmonella spp.\nAUSENTE/25g')) and df.get('Salmonella spp.\nAUSENTE/25g') == "AUSENTE" else "PRESENTE",
                
                'olor': "Característico a carne de res." if df.get('Olor') == "CUMPLE" else str(df.get('Olor', '')),
                'sabor': "Característico libre de sabores extraños." if df.get('Sabor') == "CUMPLE" else str(df.get('Sabor', '')),
                'color': "Característico, rosado con betas de grasa." if df.get('Color') == "CUMPLE" else str(df.get('Color', '')),
                'aspecto': "Característico suave. Liso y brillante" if df.get('Aspecto') == "CUMPLE" else str(df.get('Aspecto', '')),
            })

        elif tipo_producto == "PORCIONADOS":
            certificado_data.update({
                'coliformes': float(df.get('Cta. Total Coliformes \n<5000 UFC/g', 0)) if pd.notna(df.get('Cta. Total Coliformes \n<5000 UFC/g')) else 0,
                'e_coli': float(df.get('Cta. Total E. coli \n<5000 UFC/g', 0)) if pd.notna(df.get('Cta. Total E. coli \n<5000 UFC/g')) else 0,
                'humedad': float(df.get('% Humedad', 0)) if pd.notna(df.get('% Humedad')) else 0,
                
                'sabor': "Característico a carne de cerdo." if df.get('Sabor') == "CUMPLE" else str(df.get('Sabor', '')),
                'color': "Rosa pálido con vetas blancas de grasa característico a cerdo." if df.get('Color') == "CUMPLE" else str(df.get('Color', '')),
                'aspecto': "Carne rosa característico del cerdo." if df.get('Aspecto') == "CUMPLE" else str(df.get('Aspecto', ''))
            })

        elif tipo_producto == "EMBUTIDOS":
            certificado_data.update({
                'coliformes': float(df.get('Cta. Total Coliformes \n<5,000 UFC/g', 0)) if pd.notna(df.get('Cta. Total Coliformes \n<5,000 UFC/g')) else 0,
                'e_coli': float(df.get('Cta. Total E. coli \n<5000 UFC/g', 0)) if pd.notna(df.get('Cta. Total E. coli \n<5000 UFC/g')) else 0,
                'humedad': float(df.get('% Humedad', 0)) if pd.notna(df.get('% Humedad')) else 0,
                
                'materia_extraña': "CUMPLE" if df.get('Materia Extraña') == "CUMPLE" else str(df.get('Materia Extraña', '')),
                'olor': "Característico a producto cárnico." if df.get('Olor') == "CUMPLE" else str(df.get('Olor', '')),
                'sabor': "Característico a producto cárnico." if df.get('Sabor') == "CUMPLE" else str(df.get('Sabor', '')),
                'color': "Característico a producto cárnico." if df.get('Color') == "CUMPLE" else str(df.get('Color', '')),
                'textura': "Característico a producto cárnico." if df.get('Textura') == "CUMPLE" else str(df.get('Textura', ''))
            })

        elif tipo_producto == "ARRACHERA":
            certificado_data.update({
                'coliformes': float(df.get('Cta. Total Coliformes \n<5000 UFC/g', 0)) if pd.notna(df.get('Cta. Total Coliformes \n<5000 UFC/g')) else 0,
                'e_coli': float(df.get('Cta. Total E. coli \n<5000 UFC/g', 0)) if pd.notna(df.get('Cta. Total E. coli \n<5000 UFC/g')) else 0,
                
                'olor': "Característico a carne de res." if df.get('Olor') == "CUMPLE" else str(df.get('Olor', '')),
                'sabor': "Característico libre de sabores extraños." if df.get('Sabor') == "CUMPLE" else str(df.get('Sabor', '')),
                'color': "Característico, rosado con betas de grasa." if df.get('Color') == "CUMPLE" else str(df.get('Color', '')),
                'aspecto': "Característico suave. Liso y brillante" if df.get('Aspecto') == "CUMPLE" else str(df.get('Aspecto', '')),
            })

        elif tipo_producto == "COCIDOS Y ESTERILIZADOS":
            certificado_data.update({
                'coliformes': float(df.get('Cta. Total Coliformes \n<10 UFC/g', 0)) if pd.notna(df.get('Cta. Total Coliformes \n<10 UFC/g')) else 0,
                'e_coli': float(df.get('Cta. Total E. coli \n<10 UFC/g', 0)) if pd.notna(df.get('Cta. Total E. coli \n<10 UFC/g')) else 0,
                'hongos': float(df.get('Hongos\n<10 UFC/g', 0)) if pd.notna(df.get('Hongos\n<10 UFC/g')) else 0,
                'levaduras': float(df.get('Levaduras\n<10 UFC/g', 0)) if pd.notna(df.get('Levaduras\n<10 UFC/g')) else 0,
                'salmonella_spp': "AUSENTE" if pd.notna(df.get('Salmonella spp.\nAUSENTE/25g')) and df.get('Salmonella spp.\nAUSENTE/25g') == "AUSENTE" else "PRESENTE",
                'listeria_mono': "AUSENTE" if pd.notna(df.get('Listeria monocytogenes\nAUSENTE/25g')) and df.get('Listeria monocytogenes\nAUSENTE/25g') == "AUSENTE" else "PRESENTE",
                'humedad': float(df.get('% Humedad', 0)) if pd.notna(df.get('% Humedad')) else 0,

                'materia_extraña': "CUMPLE" if df.get('Materia Extraña') == "CUMPLE" else str(df.get('Materia Extraña', '')),
                'olor': "Característico a carne de res." if df.get('Olor') == "CUMPLE" else str(df.get('Olor', '')),
                'sabor': "Característico libre de sabores extraños." if df.get('Sabor') == "CUMPLE" else str(df.get('Sabor', '')),
                'color': "Característico, rosado con betas de grasa." if df.get('Color') == "CUMPLE" else str(df.get('Color', '')),
                'textura': "Característico suave. Liso y brillante" if df.get('Textura') == "CUMPLE" else str(df.get('Textura', '')),
            })

        certificado = CertificadoCalidad.objects.create(**certificado_data)

        certificado = CertificadoCalidad(
            cliente=certificado_data['cliente'],
            producto=certificado_data['producto'],
            lote=certificado_data['lote'],
            clave=certificado_data['clave'],
            cantidad=certificado_data['cantidad'],
            fecha_elaboracion=certificado_data['fecha_elaboracion'],
            fecha_caducidad=certificado_data['fecha_caducidad'],
            
            # Campos microbiológicos (usando 0 si no es numérico)
            mesofilicos=float(certificado_data.get('mesofilicos', 0)) if isinstance(certificado_data.get('mesofilicos'), (int, float)) else 0,
            coliformes=float(certificado_data.get('coliformes', 0)) if isinstance(certificado_data.get('coliformes'), (int, float)) else 0,
            e_coli=float(certificado_data.get('e_coli', 0)) if isinstance(certificado_data.get('e_coli'), (int, float)) else 0,
            hongos=float(certificado_data.get('hongos', 0)) if isinstance(certificado_data.get('hongos'), (int, float)) else 0,
            levaduras=float(certificado_data.get('levaduras', 0)) if isinstance(certificado_data.get('levaduras'), (int, float)) else 0,
            salmonella_spp="AUSENTE", 
            listeria_mono="AUSENTE", 
            staphylococcus="AUSENTE",
            
            # Campos fisicoquímicos
            acidez=float(certificado_data.get('acidez', 0)) if isinstance(certificado_data.get('acidez'), (int, float)) else 0,
            peroxidos=float(certificado_data.get('peroxidos', 0)) if isinstance(certificado_data.get('peroxidos'), (int, float)) else 0,
            humedad=float(certificado_data.get('humedad', 0)) if isinstance(certificado_data.get('humedad'), (int, float)) else 0,
            
            # Campos organolépticos
            materia_extraña=str(certificado_data.get('materia_extraña', '')),
            olor=str(certificado_data.get('olor', '')),
            sabor=str(certificado_data.get('sabor', '')),
            color=str(certificado_data.get('color', '')),
            textura=str(certificado_data.get('textura', '')),
            aspecto=str(certificado_data.get('aspecto', '')),
            
            # Observaciones
            observaciones=str(certificado_data.get('observaciones', ''))
        )
        
        # Generar documentos Word y PDF
        certificado.save()  # Guardar primero para asignar un ID
        
        # Generar los documentos usando DocxTemplate
        doc = DocxTemplate(template_path)
        doc.render(certificado_data)
        
        # Crear directorios si no existen
        word_dir = os.path.join(settings.MEDIA_ROOT, 'certificados/word/')
        pdf_dir = os.path.join(settings.MEDIA_ROOT, 'certificados/pdf/')
        os.makedirs(word_dir, exist_ok=True)
        os.makedirs(pdf_dir, exist_ok=True)
        
        # Guardar documento Word
        word_filename = f'Certificado_{tipo_producto.replace(" ", "_")}_{certificado.lote}_{certificado.clave}.docx'
        word_path = os.path.join(word_dir, word_filename)
        doc.save(word_path)
        certificado.documento_word.name = f'certificados/word/{word_filename}'
        
        # Generar PDF
        pdf_filename = f'Certificado_{tipo_producto.replace(" ", "_")}_{certificado.lote}_{certificado.clave}.pdf'
        pdf_path = os.path.join(pdf_dir, pdf_filename)
        
        # Convertir Word a PDF
        convert(word_path, pdf_path)
        certificado.documento_pdf.name = f'certificados/pdf/{pdf_filename}'
        
        # Guardar rutas en la base de datos
        certificado.save()
        
        # Preparar respuesta
        respuesta = {
            "encontrado": True,
            "tipo_producto": tipo_producto,
            "certificado_id": certificado.id,
            "documento_word_url": certificado.documento_word.url if certificado.documento_word else None,
            "documento_pdf_url": certificado.documento_pdf.url if certificado.documento_pdf else None,
            "datos": certificado_data
        }
        
        return JsonResponse(respuesta)

    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        return JsonResponse({
            "encontrado": False,
            "mensaje": f"Error al procesar la solicitud: {str(e)}",
            "detalles": traceback_str
        })


def aci_home(request):
    return render(request, 'ACI.html')





