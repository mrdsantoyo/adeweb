import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from .load_poes import df
from .. import styles

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Preprocesamiento de datos similar a load_mtto.py
df_poes = df.dropna(how='all', axis=1)
df_poes.index = pd.to_datetime(df_poes.index)
# Filtrar solo columnas numéricas antes de calcular promedios
numeric_cols = df_poes.select_dtypes(include=['number']).columns
df_mes = df_poes[numeric_cols].groupby(df_poes.index.month).mean().T

# poes_dash = Dash(__name__)

poes_dash_layout = html.Div(
    children=[
        html.Header(id='header',
            children=[
                html.Img(id='Logo',
                    src="/assets/Dilusa Logo byn.png",
                    alt="Logo",
                    style={
                        'height': '100px', 
                        'backgroundColor': '#2b2b2b'
                        }
                    ),
                html.H2(id='header1',
                    children="KPI's POES",
                    style={
                        'alignItems': 'center',
                        "justifyContent": "space-around",
                        'display': 'flex',
                        'color': 'white',
                        **styles.GRL
                        }
                    ),
                ],
            style={
                'backgroundColor': '#2b2b2b',
                'height': '110px',
                'display': 'flex',
                "alignItems": "center"
                }
            ),
        html.Div(id='filtros',
            children=[
                dcc.Interval(id='intervalo',
                    interval=3600,
                    n_intervals=0,
                    disabled=True
                    ),
                dcc.Dropdown(id='filtro_area',
                    options=[{'label': area, 'value': area} for area in df.columns],    
                    value=[],
                    placeholder='Selecciona un departamento.',
                    multi=True,
                    style=styles.DROPDOWN_100
                    )
                ],
            style={
                'display': 'flex',
                'flexDirection': 'row',
                'flexWrap': 'wrap',
                **styles.GRL
                }
            ),
        html.Div(id='graficos',
            children=[
                dcc.Graph(id='serie-temporal',
                    style={
                        'width': '70%', 
                        'height': '300px', 
                        **styles.GRL
                        }
                    ),
                dcc.Graph(id='promedios-mensuales',
                    style={
                        'width': '70%', 
                        'height': '300px', 
                        **styles.GRL
                        }
                    ),
                ],
            style={
                'display': 'flex', 
                'flexDirection': 'row', 
                'flexWrap': 'wrap', 
                **styles.GRL
                }
            )
        ],
    style={
        'display': 'flex', 
        'flexDirection': 'row', 
        'flexWrap': 'wrap', 
        **styles.GRL
        }
    )

# @poes_dash.callback(
#     Output('serie-temporal', 'figure'),
#     Output('promedios-mensuales', 'figure'),
#     Input('filtro_area', 'value')
# )


def update_graphs(filtro_area):
    
    if not filtro_area:
        fig_serie = go.Figure()
        fig_serie.add_annotation(text="Selecciona un área para visualizar datos", showarrow=False)
        fig_promedios = go.Figure()
        fig_promedios.add_annotation(text="Selecciona un área para visualizar datos", showarrow=False)
        return fig_serie, fig_promedios
    
    # Si filtro_area tiene valores, filtrar las columnas que coincidan
    # Asumiendo que quieres mostrar datos para las áreas seleccionadas
    # Esto podría necesitar ajustes según tu estructura de datos exacta
    df_filtrado = df[filtro_area]
    

    if df_filtrado.empty:
        fig_serie = go.Figure()
        fig_serie.add_annotation(text="No hay datos disponibles", showarrow=False)
        fig_promedios = go.Figure()
        fig_promedios.add_annotation(text="No hay datos disponibles", showarrow=False)
        return fig_serie, fig_promedios


    df_filtrado = df_filtrado[df_filtrado['mes'].astype(str).str.isdigit()]
    df_filtrado['mes'] = df_filtrado['mes'].astype(int)
    df_filtrado = df_filtrado[(df_filtrado['mes'] >= 1) & (df_filtrado['mes'] <= 12)]
    meses_catalogo = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    df_filtrado['mes_nombre'] = df_filtrado['mes'].apply(lambda m: meses_catalogo[m - 1])

    # Ordenar por mes
    df_filtrado = df_filtrado.sort_values(by='mes')

    # Gráfico de serie temporal
    fig_serie = go.Figure()
    fig_serie.add_trace(go.Scatter(
        x=df_filtrado['mes_nombre'],
        y=df_filtrado['valor'],
        mode='lines+markers',
        name=f'Serie temporal - {filtro_area}'
    ))
    fig_serie.update_layout(
        title=f'Serie temporal - {filtro_area}',
        xaxis_title='Mes',
        yaxis_title='Valor',
        template = 'plotly_white'
    )

        # Promedio por mes
    df_promedios = df_filtrado.groupby('mes_nombre', sort=False)['valor'].mean().reset_index()
    fig_promedios = go.Figure()
    fig_promedios.add_trace(go.Bar(
        x=df_promedios['mes_nombre'],
        y=df_promedios['valor'],
        name=f'Promedios mensuales - {filtro_area}'
    ))
    fig_promedios.update_layout(
        title=f'Promedios mensuales - {filtro_area}',
        xaxis_title='Mes',
        yaxis_title='Valor',
        template = 'plotly_white'
    )

    return fig_serie, fig_promedios


# def update_graphs1(filtro_area):
#     df_filtrado = df[df.columns == filtro_area]

#     if df_filtrado.empty:
#         return go.Figure(), go.Figure()

#     df_filtrado = df_filtrado[df_filtrado['mes'].astype(str).str.isdigit()]
#     df_filtrado['mes'] = df_filtrado['mes'].astype(int)
#     df_filtrado = df_filtrado[(df_filtrado['mes'] >= 1) & (df_filtrado['mes'] <= 12)]
#     meses_catalogo = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
#     df_filtrado['mes_nombre'] = df_filtrado['mes'].apply(lambda m: meses_catalogo[m - 1])

    
#     df_filtrado = df_filtrado.sort_values(by='mes')
#     # Promedio por mes
#     df_promedios = df_filtrado.groupby('mes_nombre', sort=False)['valor'].mean().reset_index()
#     fig_promedios = go.Figure()
#     fig_promedios.add_trace(go.Bar(
#         x=df_promedios['mes_nombre'],
#         y=df_promedios['valor'],
#         name=f'Promedios mensuales - {filtro_area}'
#     ))
#     fig_promedios.update_layout(
#         title=f'Promedios mensuales - {filtro_area}',
#         xaxis_title='Mes',
#         yaxis_title='Valor'
#     )
#     return  fig_promedios

