import pandas as pd
import plotly.graph_objects as go
from .load_sgia import load_control_documental

def control_docs():
    df_docs = load_control_documental()
    docs = go.Figure()
    docs.add_trace(
        go.Bar(name='Publicados',
            x=df_docs.index,
            y=df_docs['Total de Publicados'],
            marker_color='green'
            )
        )
    docs.add_trace(
        go.Bar(name='En flujo',
            x=df_docs.index,
            y=df_docs['En flujo'],
            marker_color='yellow'
            )
        )
    docs.add_trace(
        go.Bar(name='Rechazados',
            x=df_docs.index,
            y=df_docs['Rechazados'],
            marker_color='brown'
            )
        )
    docs.add_trace(
        go.Bar(name='Ausencia',
            x=df_docs.index,
            y=df_docs['Ausencia'],
            marker_color='red'
            )
        )
    docs.update_layout(title='Estatus de Documentación',
        barmode='stack',
        template='plotly_white',
        showlegend=True
    )
    return docs

def eficiencia_documental():
    df_docs=load_control_documental().reset_index()
    df_docs['Eficiencia'] = ((df_docs['Total de Publicados'] / df_docs['Total'])*100).round(2)
    df_docs = df_docs.drop(columns=['Total de Publicados', 'En flujo', 'Ausencia', 'Vigencia v.','Rechazados', 'Total'])
    return df_docs

# docs = eficiencia_documental()
# print(docs)









