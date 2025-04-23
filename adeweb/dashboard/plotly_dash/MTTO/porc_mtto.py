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

df = df.dropna(subset=['FECHA'])
df= df.drop(columns=['TIEMPO_RAW', 'SEMANA', 'TIEMPO'])
df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y').dt.strftime('%d/%m/%Y')
df['ESTATUS'] = df['ESTATUS'].astype(str).str.strip().str.upper()
df1 = df.sort_values(by='FECHA', ascending=False)
df1['FECHA'] = pd.to_datetime(df1['FECHA'], format='%d/%m/%Y')
eficiencia = df1.groupby(df1['FECHA'].dt.month)['ESTATUS']

def update_graphs(filtro_equipo, filtro_tecnico, filtro_area):
    df_filtrado = df.copy()
    if filtro_equipo:
        df_filtrado = df_filtrado[df_filtrado['EQUIPO'].str.upper().isin(filtro_equipo)]
    if filtro_area:
        df_filtrado = df_filtrado[df_filtrado['ÁREA'].str.upper().isin(filtro_area)]
    if filtro_tecnico:
        df_filtrado = df_filtrado[df_filtrado['TÉCNICO'].str.upper().isin(filtro_tecnico)]

    # Contar los valores de ESTATUS
    estatus_counts = df_filtrado['ESTATUS'].value_counts()

    graf_realizados = go.Figure(
        data=[
            go.Pie(
                labels=estatus_counts.index,
                values=estatus_counts.values,
                hoverinfo='label+value+percent',
                pull=[0.1 if i == 0 else 0 for i in range(len(estatus_counts))]
            )
        ]
    )
    graf_realizados.update_layout(
        title='Total de Preventivos Realizados',
        template='plotly_dark',
        showlegend=True
    )

    return graf_realizados

