import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import sys
import os
from POES.load_poes import df 
try:
    import styles
except ModuleNotFoundError:
    styles = None 
import sys
import os

df_poes = df
df_poes.columns = df_poes.columns.str.strip(' ')
df_poes.index = pd.to_datetime(df_poes.index, errors='coerce')
df_poes['Promedios Diarios'] = df_poes.mean(axis=1).round(2)
df_poes = df_poes.dropna(subset=['Promedios Diarios'])
df_poes = df_poes.fillna(df_poes.mean()).round(2)
df_poes = df_poes.sort_index(ascending=False)

mensual = df_poes.groupby(df_poes.index.month).mean().round(2).drop(columns=['Promedios Diarios'])
mensual.index = mensual.index.map({1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
                                5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
                                9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'})
mensual['Promedios Diarios'] = mensual.mean(axis=1).round(2)

df_distribucion = pd.DataFrame()
df_distribucion['valores'] = df_poes.values.flatten()

def update_graphs(areas_a_mostrar):                 #########################
    mensual_filtrado = mensual.copy()
    
    columnas_a_mostrar = [col for col in mensual_filtrado.columns 
                        if col in areas_a_mostrar or col == 'Promedios Diarios']
    
    poes_fig = go.Figure()
    
    for area in areas_a_mostrar:

        if area != 'Promedios Diarios':
            poes_fig.add_trace(
                go.Box(
                    y=mensual_filtrado[area],
                    name=area.split(' y ')[0],
                    boxmean=True,
                )
            )
        else:
            poes_fig.add_annotation(
                text="Selecciona un área para visualizar datos",
                xref="paper",
                yref="paper",
                # x=0.5,
                # y=0.5,
                showarrow=False,
                font=dict(size=16, color='gray'),
                bgcolor='white',  
                opacity=0.9
            )


    poes_fig.update_layout(
        title_text="Distribución de calificaciones por Área",
        height=350,
        yaxis_title="%",
        xaxis_title="Área",
        showlegend=False,
        template='plotly_white',
        xaxis=dict(
            tickangle=45,  
        ),
        margin=dict(l=20, r=20, t=40, b=20), 
        legend=dict(
            orientation="h", 
            yanchor="bottom",
            y=-0.3,  
            xanchor="right",
            x=0.5
        )
    )

    distribucion = go.Figure()
    df_filtrado = df_poes[[col for col in df_poes.columns.str.strip(' ') 
                        if col in areas_a_mostrar and col != 'Promedios Diarios']]
    
    valores_filtrados = df_filtrado.values.flatten()
    
    if valores_filtrados.size == 0:
        valores_filtrados = df_poes['Promedios Diarios'].values.flatten()  ##########
    
    distribucion.add_trace(
        go.Histogram(
            x=valores_filtrados,
            nbinsx=20,
            xbins=dict(start=1, end=100, size=.2),
            marker_color='indianred',
            marker_line_color='black',
        )
    )

    distribucion.update_layout(
        title_text="Tendencia de calificación de POES",
        height=350,
        yaxis_title="Calificacion",
        xaxis_title="Resultados",
        showlegend=False,
        template='plotly_white',
        barmode='overlay',
        xaxis=dict(
            tickangle=45,  
            tickmode='auto',
        ),
        margin=dict(l=30, r=30, t=50, b=30), 
        legend=dict(
            orientation="h", 
            yanchor="bottom",
            y=-0.3,  
            xanchor="right",
            x=0.5
        )
    )
    poes_tendencia = df
    poes_tendencia.columns = poes_tendencia.columns.str.strip(' ')
    poes_tendencia['Promedios Diarios'] = poes_tendencia.mean(axis=1).round(2)
    poes_tendencia = poes_tendencia.dropna(subset=['Promedios Diarios'])
    
    tendencia = go.Figure()
    
    if areas_a_mostrar:
        for departamento in areas_a_mostrar:
            if departamento != 'Promedios Diarios':
                tendencia.add_trace(
                    go.Scatter(
                        x=poes_tendencia.index,
                        y=poes_tendencia[departamento],
                        mode='markers',
                        hovertemplate=f'{departamento}<br>%{{x}}<br>%{{y}}%<extra></extra>',
                        name=departamento,
                    )
                )
        tendencia.update_layout(
            title_text="Calificación de POES",
            height=350,
            yaxis_title="Calificacion",
            xaxis_title="Fecha",
            showlegend=True,
            template='plotly_white',
        )
    else:
        tendencia.add_trace(
            go.Scatter(
                x=poes_tendencia.index,
                y=poes_tendencia['Promedios Diarios'],
                mode='markers',
                marker=dict(color='blue', size=5),
                hovertemplate='%{x}<br><extra>%{y}</extra>',
                name='Promedios Diarios',
            )
        )
        tendencia.update_layout(
            title_text="Promedios Diarios POES",
            height=350,
            yaxis_title="Calificación",
            xaxis_title="Fecha",
            showlegend=False,
            template='plotly_white',
        )

    return tendencia, poes_fig, distribucion
