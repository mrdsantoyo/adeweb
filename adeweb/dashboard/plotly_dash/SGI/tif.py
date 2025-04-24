import pandas as pd
import plotly.graph_objects as go
from .load_sgia import load_tif

def codigo_entrada():
    df_tif = load_tif()
    df_tif['No. CE'] = df_tif['No. CE'].fillna('SIN CLASIFICAR')
    df_tif = df_tif[df_tif['Estatus']!='Completado']    
    df_eficiencia_mensual = df_tif[['Departamento', 'No. CE']].copy()
    df_eficiencia_mensual = df_eficiencia_mensual.groupby(['Departamento', 'No. CE']).size().reset_index(name='Cuenta')
    df_eficiencia_mensual = df_eficiencia_mensual.pivot(index='Departamento', columns='No. CE', values='Cuenta').fillna(0)

    colors = {
        'POES': '#1b1a89',
        'HACCP': '#12b43a',
        'ETIQUETADO': '#ff732d',
        'PROG. MICROBIOLÓGICO': '#20201e',
        'PRE-REQUISITO': '#a00000',
        'SIN CLASIFICAR': '#999999'  # ← Añadido
        }

    codigo_entrada = go.Figure()
    for key in df_eficiencia_mensual.columns:
        color = colors.get(key, 'gray')
        codigo_entrada.add_trace(
            go.Bar(name=key,
                x=df_eficiencia_mensual.index,
                y=df_eficiencia_mensual[key],
                marker_color=color
            )
        )
    codigo_entrada.update_layout(
        barmode='stack',
        xaxis_title='Departamento',
        yaxis_title='Conteo',
        title='Conteo de registros por Departamento y código de entrada (SIS)',
        template='plotly_dark',
        showlegend=False
    )
    return codigo_entrada

def estatus_general(filtro_departamento):
    df_tif = load_tif()
    df_tif['Departamento'] = df_tif['Departamento'].astype(str).str.strip().str.upper() 
    
    if filtro_departamento:
        filtro_departamento = [d.upper() for d in filtro_departamento] 
        df_tif = df_tif[df_tif['Departamento'].isin(filtro_departamento)]
    
    estatus_data = df_tif['Estatus'].value_counts()
    
    estatus_tif = go.Figure()
    estatus_tif.add_trace(
        go.Pie(name='',
            labels=estatus_data.index,
            values=estatus_data.values,
            textinfo='label',
            insidetextorientation='radial',
            pull=0.05,
            hoverinfo='label+value+percent'
        )
    )
    estatus_tif.update_layout(
        title='Estatus de desviaciones TIF',
        template='plotly_dark',
        showlegend=False
    )
    return estatus_tif

def eficiencia_mensual():
    df_tif = load_tif()
    df_eficiencia_mensual = df_tif[['Fecha', 'No. CE', 'Departamento','Estatus']].copy()
    df_eficiencia_mensual = df_eficiencia_mensual.sort_values('Fecha')
    df_eficiencia_mensual['Fecha'] = pd.to_datetime(df_eficiencia_mensual['Fecha'], errors='coerce', format="%d/%b/%Y").astype(str)
        
    graf_eficiencia= go.Bar(
            x=df_eficiencia_mensual['Fecha'],
            y=df_eficiencia_mensual['Departamento']
        )
    
    graf_eficiencia.update_layout(
        title='Código de entrada',
        template='plotly_dark',
        showlegend=True
    )
    return graf_eficiencia



