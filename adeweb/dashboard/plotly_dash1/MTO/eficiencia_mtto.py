import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from .load_mtto import df
import warnings
warnings.filterwarnings('ignore')
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import styles

df = df
df = df.dropna(subset=['FECHA'])
df = df.drop(columns=['TIEMPO_RAW', 'SEMANA', 'TIEMPO'])

df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y')

df = df.sort_values(by='FECHA', ascending=True)

df['ESTATUS'] = df['ESTATUS'].astype(str).str.strip().str.upper()

df1 = df.copy()

df1['MES'] = df1['FECHA'].dt.month
df1['MES'].replace(
    {
        1: 'Enero',
        2: 'Febrero',
        3: 'Marzo',
        4: 'Abril',
        5: 'Mayo',
        6: 'Junio',
        7: 'Julio',
        8: 'Agosto',
        9: 'Septiembre',
        10: 'Octubre',
        11: 'Noviembre',
        12: 'Diciembre'
    },
    inplace=True
)

def actualizar_graficos(filtro_equipo, filtro_tecnico, filtro_area):
    df_filtrado = df1.copy()
    
    if filtro_equipo:
        df_filtrado = df_filtrado[df_filtrado['EQUIPO'].str.upper().isin(filtro_equipo)]
    if filtro_area:
        df_filtrado = df_filtrado[df_filtrado['ÁREA'].str.upper().isin(filtro_area)]
    if filtro_tecnico:
        df_filtrado = df_filtrado[df_filtrado['TÉCNICO'].str.upper().isin(filtro_tecnico)]
    
    total_mes = df_filtrado.groupby('FECHA')['ESTATUS'].count()
    realizados_mes = df_filtrado[df_filtrado['ESTATUS'] == 'REALIZADO'].groupby('FECHA')['ESTATUS'].count()
    eficiencia = (realizados_mes / total_mes).fillna(0) * 100
    eficiencia = eficiencia.reset_index(name='PorcentajeRealizados')
    
    graf_eficiencia = go.Figure()
    graf_eficiencia.add_trace(
        go.Scatter(
            x=eficiencia['FECHA'],
            y=eficiencia['PorcentajeRealizados'],
            mode='markers',
            hoverlabel=dict(namelength=0),
            name='Eficiencia %'
        )
    )
    graf_eficiencia.update_layout(
        title='Eficiencia de Mantenimientos',
        xaxis_title='Mes',
        yaxis_title='Porcentaje (%)',
        template='plotly_dark'
    )
    
    return graf_eficiencia

