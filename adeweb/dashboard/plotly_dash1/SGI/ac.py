import pandas as pd
from datetime import datetime as dt
import plotly.graph_objects as go
from .load_sgia import load_ac

df_ac = load_ac()
df = df_ac[df_ac['Sucursal'] == 'DILUSA']

df.columns = df.columns.str.strip()
df = df.copy()
df.index = df['Código']
df = df.drop(columns=['Código'])
df['Fecha compromiso'] = pd.to_datetime(df['Fecha compromiso'])
df['Fecha de cierre real'] = pd.to_datetime(df['Fecha de cierre real'])
df.loc[~pd.isna(df['Fecha de cierre real']), 'Estatus'] = 'Cerrada'

df['Comentario'] = df.apply(lambda x: 'Falta plan de acción' if pd.isna(x['Fecha compromiso'])
                            else f"Tarea con {(pd.Timestamp.today()-x['Fecha compromiso']).days} días de retraso" if (pd.Timestamp.today() > x['Fecha compromiso'] and pd.isna(x['Fecha de cierre real']))
                            else f"Tarea cerrada con retraso de {(x['Fecha de cierre real']-x['Fecha compromiso']).days} días" if x['Fecha de cierre real'] > x['Fecha compromiso']
                            else 'Cierre a tiempo' if x['Fecha de cierre real']<= x['Fecha compromiso']
                            else 'En tiempo' if (x['Estatus'] == 'Abierta' and pd.Timestamp.today()<=x['Fecha compromiso'])
                            else '',  
                            axis=1
                            )

pivo = pd.pivot_table(data=df, columns='Tipo de NC', index='Requisito', aggfunc='size', fill_value=0)
pivo['Totales'] = pivo.sum(axis=1)
pivo = pivo.sort_values('Totales', ascending=False)
pivo =pivo.head(10)
pivo = pivo.reset_index()

df1 = df[['Requisito', 'Departamento', 'Fecha de la NC', 'Fecha compromiso', 'Fecha de cierre real', 'Estatus']]
df1['Fecha de la NC'] = pd.to_datetime(df1['Fecha de la NC'], errors='coerce')
df1['Mes'] = df1['Fecha de la NC'].dt.to_period('M')
eficiencia_mensual = df1.groupby('Mes')['Estatus'].apply(lambda x: ((x=='Abierta').sum() / x.count())*100)

df2 = df[['Requisito', 'Departamento', 'Fecha de la NC', 'Fecha compromiso', 'Fecha de cierre real', 'Tipo de NC', 'Estatus']]
df2['Fecha compromiso'] = pd.to_datetime(df2['Fecha compromiso'], errors='coerce')
df2 = df2.sort_values('Fecha compromiso', ascending=False)
df2['Mes'] = df2['Fecha compromiso'].dt.to_period('M')
df2 = df2.sort_values('Mes', ascending=False)
df2 = df2[df2['Estatus'] != 'Cerradas']
df2 = pd.pivot_table(data=df2, index='Mes', columns='Tipo de NC', aggfunc='size', fill_value=0)

df3 = df[['Departamento', 'Fecha compromiso', 'Tipo de NC', 'Comentario', 'Estatus']]
df3['Fecha compromiso'] = pd.to_datetime(df3['Fecha compromiso'], errors='coerce')
df3 = df3.sort_values('Fecha compromiso', ascending=False)
df3['Mes'] = df3['Fecha compromiso'].dt.to_period('M')
df3 = df3.sort_values('Mes', ascending=False)
df3 = df3[df3['Estatus'] != 'Cerradas']


def eficiencia(filtro_departamento):
    
    if filtro_departamento:
        df_filtrado = df1[df1['Departamento'] == filtro_departamento]
        eficiencia_mensual = df_filtrado.groupby('Mes')['Estatus'] \
            .apply(lambda x: ((x=='Abierta').sum() / x.count())*100)
    else:
        eficiencia_mensual = df1.groupby('Mes')['Estatus'] \
            .apply(lambda x: ((x=='Abierta').sum() / x.count())*100)


    ac2=go.Figure()
    ac2.add_trace(
        go.Scatter(name='Eficiencia (%)',
            x=eficiencia_mensual.index.astype(str),  
            y=eficiencia_mensual.values.round(2),
            yaxis='y2',
            mode='markers',
            hoverinfo='name+y',
            marker=dict(
                size=7,
                color='red'
                ),
            )
        )
    ac2.add_trace(go.Bar(name='NC Críticas',
        x=df2.index.astype(str),  
        y=df2['NCC'],
        )
    )
    ac2.add_trace(go.Bar(name='NC Mayores ',
        x=df2.index.astype(str),  
        y=df2['NCM'],
        )
    )
    ac2.add_trace(go.Bar(name='NC Menores',
        x=df2.index.astype(str),  
        y=df2['NC m'],
        )
    )

    ac2.update_layout(
        yaxis=dict(
            title=r'NC objetivo del mes',
            ),
        yaxis2=dict(
            title=r'Eficiencia \(%\)',
            overlaying='y',
            side='right',
            gridcolor='white'
            ),
        barmode='stack',
        template='plotly_white',
        showlegend=False,
        xaxis=dict(
            tickangle=-45
            ),
        margin=dict(l=30, r=30, t=40, b=30), 
        legend=dict(
            orientation="h", 
            yanchor="bottom",
            y=-0.3,  
            xanchor="right",
            x=0.5
        )
        )
    return ac2

def requisito_tipo():
    original_labels =pivo['Requisito']
    truncated_labels = [label[:15] + '...' if len(label) > 15 else label for label in original_labels]

    ac1 = go.Figure()
    ac1.add_trace(go.Bar(name='NCC',
            x=pivo['Requisito'],
            y=pivo['NCC'],
            text=pivo['NCC'],
            # textposition='auto',
            # marker_color=,
            # hoverinfo='', 
            )
        )
    ac1.add_trace(go.Bar(name='NCM',
            x=pivo['Requisito'],
            y=pivo['NCM'],
            text=pivo['NCM'],
            # textposition='auto',
            # marker_color=,
            # hoverinfo='',  
            )
        )
    ac1.add_trace(go.Bar(name='NCm',
            x=pivo['Requisito'],
            y=pivo['NC m'],
            text=pivo['NC m'],
            # textposition='auto',
            # marker_color=,   
            )
        )

    ac1.update_layout(title='Requisitos con mayor incidencia de NC',
        barmode='stack',
        template='plotly_white',
        showlegend=False,
        xaxis=dict(
        tickmode='array',
        tickvals=original_labels,  # O los valores correspondientes
        ticktext=truncated_labels,
        tickangle=-45  # opcional, para rotarlas
        ),
        margin=dict(l=30, r=30, t=40, b=30), 
        legend=dict(
            orientation="h", 
            yanchor="bottom",
            y=-0.3,  
            xanchor="right",
            x=0.5
        )
        )

    return ac1

def estatus_grl():
    df_cuenta = df.groupby('Estatus')['Fecha de la NC'].count()
    df_cuenta = df_cuenta.reset_index()

    estatus_grl = go.Figure()

    estatus_grl.add_trace(go.Pie(name='Estatus AC',
            labels=df_cuenta['Estatus'],
            values=df_cuenta['Fecha de la NC'],
            textinfo='label',
            insidetextorientation='radial',
            hoverinfo='label+value+percent',
            pull=0.05,
        )
    )
    estatus_grl.update_layout(title='Acciones correctivas',
            template='plotly_white',
            showlegend=False,
            margin=dict(l=30, r=30, t=40, b=30), 
            legend=dict(
                orientation="h", 
                yanchor="bottom",
                y=-0.3,  
                xanchor="right",
                x=0.5
            )
            )

    return estatus_grl

