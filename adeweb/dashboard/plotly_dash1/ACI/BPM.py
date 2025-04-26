import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import warnings
warnings.filterwarnings('ignore')
from .load_aci import bpm_operativo_df, bpm_personales_df

def bpmoperativas(filtro_area, start_date, end_date):
    filtro_fecha_inicio = pd.to_datetime(start_date) if start_date else bpm_operativo_df.index.min()
    filtro_fecha_fin = pd.to_datetime(end_date) if end_date else bpm_operativo_df.index.max()
    df_operativo_filtrado = bpm_operativo_df[(bpm_operativo_df.index >= filtro_fecha_inicio) & (bpm_operativo_df.index <= filtro_fecha_fin)]
    operativas_graf = go.Figure()
    
    if not filtro_area:
        operativas_graf.add_trace(
            go.Scatter(
                x=df_operativo_filtrado.index,
                y=df_operativo_filtrado['PROMEDIOS DIARIOS'],
                mode='markers',
                name='Promedios Diarios'
            )
        )
    else:
        for area in filtro_area:
            if area in df_operativo_filtrado.columns:
                operativas_graf.add_trace(
                    go.Scatter(
                        x=df_operativo_filtrado.index,
                        y=df_operativo_filtrado[area],
                        mode='markers',
                        name=area
                    )
                )
    operativas_graf.update_layout(
        title='BPM Operacionales',
        xaxis_title='Fecha',
        yaxis_title='Calificación (%)',
        template='plotly_white',
        showlegend=False,
    )
    return operativas_graf

def bpmpersonales(filtro_area, start_date, end_date):
    filtro_fecha_inicio = pd.to_datetime(start_date) if start_date else bpm_personales_df.index.min()
    filtro_fecha_fin = pd.to_datetime(end_date) if end_date else bpm_personales_df.index.max()
    df_personal_filtrado = bpm_personales_df[(bpm_personales_df.index >= filtro_fecha_inicio) & (bpm_personales_df.index <= filtro_fecha_fin)]
    personales_graf = go.Figure()
    
    if not filtro_area:
        personales_graf.add_trace(
            go.Scatter(
                x=df_personal_filtrado.index,
                y=df_personal_filtrado['PROMEDIOS DIARIOS'],
                mode='markers',
                name='Promedios Diarios'
            )
        )
    else:
        for area in filtro_area:
            if area in df_personal_filtrado.columns:
                personales_graf.add_trace(
                    go.Scatter(
                        x=df_personal_filtrado.index,
                        y=df_personal_filtrado[area],
                        mode='markers',
                        name=area
                    )
                )
    personales_graf.update_layout(
        title='BPM Personal',
        xaxis_title='Fecha',
        yaxis_title='Calificación (%)',
        template='plotly_white'
    )
    return personales_graf

filtro_area = [col for col in bpm_operativo_df.columns if col not in ['PROMEDIOS DIARIOS','FECHA','MES']]

# bpms = Dash(__name__)
# bpms.layout = html.Div(
#     children=[
#         dcc.Dropdown(
#             id='filtro_area',
#             options=[{'label': col, 'value': col} for col in filtro_area],
#             placeholder='Selecciona un área',
#             multi=True,
#             style={'width': '750px'}
#         ),
#         dcc.DatePickerRange(
#             id='filtro_fecha',
#             start_date=bpm_operativo_df['FECHA'].min() if not bpm_operativo_df.empty else None,
#             end_date=bpm_operativo_df['FECHA'].max() if not bpm_operativo_df.empty else None,
#         ),
#         dcc.Graph(id='operativas_graf'),
#         dcc.Graph(id='personales_graf')
#     ]
# )

# @bpms.callback(
#     [Output('operativas_graf', 'figure'), Output('personales_graf', 'figure')],
#     [Input('filtro_area', 'value'), Input('filtro_fecha', 'start_date'), Input('filtro_fecha', 'end_date')]
# )
# def actualizar_graficos(filtro_area, start_date, end_date):
#     return bpmoperativas(filtro_area, start_date, end_date), bpmpersonales(filtro_area, start_date, end_date)

# if __name__ == "__main__":
#     bpms.run(debug=True, port=8052)
