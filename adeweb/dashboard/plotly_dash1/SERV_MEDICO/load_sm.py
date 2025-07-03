import pandas as pd
import numpy as np
import re
import plotly.graph_objects as go

with pd.ExcelFile("//192.168.10.2/Compartidos/Servicio Medico/ARCHIVOS P INDICADORES/Consultas SM 2025.xlsx", engine='openpyxl') as workbook:
    try:
        df = pd.read_excel(
            workbook, 
            sheet_name='Consulta EDA',
            usecols = "A:O",
            )
        workbook.close()
    except:
        print(f"Error al cargar el archivo {workbook}")
        workbook.close()


df.columns = df.columns.str.strip()
df = df.drop(columns=['Unnamed: 5', 'Unnamed: 6'])
df['Mes'] = df['Fecha'].dt.month
df = df.dropna(subset='Departamento')
df['Motivo de consulta'] = df['Motivo de consulta'].str.upper()
df['Departamento'] = df['Departamento'].str.upper()
df['Departamento'] = df['Departamento'].replace({
    'MANTENIMIENTO DE PLANTA': 'MANTENIMIENTO',
    'ASEGURAMIENTO DE CALIDAD E INOCUIDAD': 'ACI',
    'CORTE DE CUERO':'CORTE',
    'COCIDOS Y ESTERILIZADOS':'COCIDOS',
    'TALENTO HUMANO':'CH',
    'SISTEMA DE GESTION DE INOCUIDAD ALIMENTARIA':'SGIA',
    'CENTRO DE DISTRIBUCION DE BASICOS':'CDB',
    'FRIGORIFICOS Y LOGISTICA DG': 'FRIGORIFICO',
    'GERENCIA DE OPERACIONES':'GOP',
})

atn_x_area = df.groupby(['Mes', 'Departamento']).size().reset_index(name='COUNT')
atn_x_area['Mes'] = atn_x_area['Mes'].map({1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 
                                        7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'})
atn_x_area = atn_x_area.drop(axis=0, index=0)
atn_x_area = atn_x_area.sort_values(by='COUNT', ascending=False)
df_motivos = df.groupby(['Mes', 'Motivo de consulta']).size().reset_index(name='COUNT')
df_motivos['Mes'] = df_motivos['Mes'].map({1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 
                                        7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'})

with pd.ExcelFile(r"//192.168.10.2/Compartidos/Servicio Medico/ARCHIVOS P INDICADORES/INCAPACIDADES 2025.xlsx", engine='openpyxl') as workbook:
    try:
        df_inc = pd.read_excel(
            workbook, 
            )
        workbook.close()
    except:
        print(f"Error al cargar el archivo {workbook}")
        workbook.close()

df_inc.columns = df_inc.columns.str.strip()
df_inc = df_inc.dropna(subset='#')
df_inc['NSS'] = pd.to_numeric(df_inc['NSS'])
df_st7 = df_inc[df_inc['ST7']=='SI ']


df_inc['EG o RT'] = df_inc['EG o RT'].astype(str)
df_accidentes = df_inc[df_inc['EG o RT'].str.contains(r'\bRT\b', flags=re.IGNORECASE, na=False)]
df_trayectos = df_inc[df_inc['DETERMINACION'].str.contains(r'\bSI\b', flags=re.IGNORECASE, na=False)]

def top_5_atn_area(n_intervals, start_date, end_date):
    global df
    try:
        filtered_df = df.copy()
        if start_date and end_date:
            filtered_df = filtered_df[(filtered_df['Fecha'] >= start_date) & (filtered_df['Fecha'] <= end_date)]
        atn_x_area = (filtered_df['DEPARTAMENTO'].value_counts().reset_index().rename(columns={'index': 'DEPARTAMENTO', 'DEPARTAMENTO': 'Count'}).head(5))  
        atn_x_area.columns = ['DEPARTAMENTO', 'Count']

        atn_x_area = atn_x_area.sort_values(by='Count', ascending=False)
        
    except Exception as e:
        print(f"Error al procesar datos: {e}")
        return go.Figure()  
    
    top5 = go.Figure()
    top5.add_trace(
        go.Pie(
            labels=atn_x_area['DEPARTAMENTO'].head(5),
            values=atn_x_area['Count'].head(5),
            hovertemplate="%{label} <extra>%{value} Atenciones (%{percent})</extra>",
            pull=[0.05 if i == 0 else 0 for i in range(5)],
        )
    )
    top5.update_layout(
        template='plotly_white',
        title='Top 5 Áreas con más atenciones',
        xaxis_title='Área',
        yaxis_title='Cantidad de atenciones',
        margin=dict(l=30, r=30, t=40, b=30),
        showlegend=False,
    )
    return top5

def fig_atn_area(n_intervals):
    # Definir orden cronológico de meses
    meses_orden = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
    # Convertir a categórico ordenado
    atn_x_area['Mes'] = pd.Categorical(atn_x_area['Mes'], 
        categories=meses_orden,
        ordered=True)
    
    # Ordenar el DataFrame
    atn_sorted = atn_x_area.sort_values('Mes')
    
    x_area = go.Figure()
    
    for mes in meses_orden:
        mes_data = atn_sorted[atn_sorted['Mes'] == mes]
        if not mes_data.empty:
            mes_data = mes_data.sort_values(by='COUNT', ascending=False)
            x_area.add_trace(
                go.Bar(
                    name=mes,
                    x=mes_data["DEPARTAMENTO"],
                    y=mes_data["COUNT"],
                    opacity=0.8,
                    hovertemplate=f"{mes}: %{{y}} atenciones"
                )
            )
    
    x_area.update_layout(
        template='plotly_white',
        title='Atenciones por área y mes',
        xaxis_title='DEPARTAMENTO',
        yaxis_title='Total de atenciones',
        barmode='stack',
        margin=dict(l=30, r=30, t=45, b=30),
        xaxis=dict(
            tickangle=-45,
            tickmode='auto',
            tickfont=dict(size=10)
        ),
    )
    return x_area 

def motivos_atn(n_intervals):
    # Definir orden cronológico
    meses_orden = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
    # Convertir a categórico y ordenar
    df_motivos['Mes'] = pd.Categorical(df_motivos['Mes'],
        categories=meses_orden,
        ordered=True)
    df_sorted = df_motivos.sort_values('Mes')
    
    patologias_graf = go.Figure()
    
    for mes in meses_orden:
        mes_data = df_sorted[df_sorted['Mes'] == mes]
        if not mes_data.empty:
            mes_data = mes_data.sort_values(by='COUNT', ascending=False)
            patologias_graf.add_trace(
                go.Bar(
                    name=mes,
                    x=mes_data["Motivo de consulta"],
                    y=mes_data["COUNT"],
                    opacity=0.8,
                    hovertemplate=f"{mes}: %{{y}} atenciones",
                )
            )
    
    patologias_graf.update_layout(
        template='plotly_white',
        title='Motivos de consulta por mes',
        xaxis_title='Motivo',
        yaxis_title='Total de atenciones',
        barmode='stack',
        margin=dict(l=30, r=30, t=45, b=30),
        xaxis=dict(
            tickangle=-45,
            tickmode='auto',
            tickfont=dict(size=10)
        ),
    )
    return patologias_graf

def generadores(n_intervals, start_date, end_date):
    df1 = df_inc[['Termino de Incapacidad', 'Amerito       ST-7', 'SI / NO                                DE TRABAJO', 'SI / NO                             DE TRAYECTO', 'Diagnostico']].copy()
    df1 = df1.dropna(subset=['Diagnostico'])
    df1 = df1[['Termino de Incapacidad', 'Diagnostico']].copy()
    df1['Termino de Incapacidad'] = pd.to_datetime(df1['Termino de Incapacidad'], errors='coerce')
    
    
    df1 = df1.dropna(subset=['Termino de Incapacidad', 'Diagnostico'])
    df1 = df1.drop(index=0)
    df1 = df1[df1['Diagnostico'] != 'PENDIENTE']
    df1 = df1[(df1['Termino de Incapacidad'] >= start_date) & (df1['Termino de Incapacidad'] <= end_date)]

    conteo_diagnosticos = df1['Diagnostico'].value_counts().reset_index()
    conteo_diagnosticos.columns = ['Diagnostico', 'Cantidad']
    top_diagnosticos = conteo_diagnosticos.head(5)

    generadores = go.Figure()
    generadores.add_trace(
        go.Pie(
            labels=top_diagnosticos['Diagnostico'],
            values=top_diagnosticos['Cantidad'],
            opacity=0.8,
            # pull = 0.05,
            hole=0.5,
            hovertemplate="%{label}<br><extra>Cantidad: %{value} (%{percent})</extra>",
        )
    )
    generadores.update_layout(
        template='plotly_white',
        title='Generadores de Incapacidad',
        xaxis_title='Motivo',
        yaxis_title='Cantidad de atenciones',
        margin=dict(l=30, r=30, t=40, b=30),
        showlegend=False,
        )
    return generadores

def areas_generadores(n_intervals, start_date, end_date):
    global df_inc

    df_inc['SI / NO                                DE TRABAJO'] = df_inc['SI / NO                                DE TRABAJO'].astype(str)
    df_accidentes = df_inc[df_inc['SI / NO                                DE TRABAJO'].str.contains(r'\bSI\b', flags=re.IGNORECASE, na=False)]
    df_trayectos = df_inc[df_inc[ 'SI / NO                             DE TRAYECTO'].str.contains(r'\bSI\b', flags=re.IGNORECASE, na=False)]
    df_accidentes = df_accidentes[['Termino de Incapacidad', 'Área']].copy()
    df_accidentes['Termino de Incapacidad'] = pd.to_datetime(df_accidentes['Termino de Incapacidad'], errors='coerce')
    df_accidentes = df_accidentes.dropna()
    df_filtrado = df_accidentes[(df_accidentes['Termino de Incapacidad'] >= start_date) & (df_accidentes['Termino de Incapacidad'] <= end_date)]
    df_filtrado['Área'] = df_filtrado['Área'].str.upper()
    df_filtrado = df_filtrado.head(5)

    areas_generadores = go.Figure()
    areas_generadores.add_trace(
        go.Pie(
            labels=df_filtrado['Área'].value_counts().index,
            values=df_filtrado['Área'].value_counts().values,
            hole=0.5,
            hovertemplate="%{label}<br><extra>Cantidad: %{value} (%{percent})</extra>",
        )
    )
    areas_generadores.update_layout(
        title='Áreas de generación de accidentes',
        title_x=0.5,
        showlegend=False,
        margin=dict(l=30, r=30, t=45, b=30),
        xaxis=dict(
            tickangle=-45,
            tickmode='auto',
        )
    )
    return areas_generadores

