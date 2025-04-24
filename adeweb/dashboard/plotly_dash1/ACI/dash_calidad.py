import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from .. import styles
from .load_aci import bpm_operativo_df, bpm_personales_df
from .BPM import bpmoperativas, bpmpersonales, filtro_area
from .mb_indicadores import actualizar_grafico_indicadores, filtro
from .porc_liberaciones import actualizar_grafico_liberaciones

import warnings
warnings.filterwarnings('ignore')

import sys
sys.path.append('..')

start_date = pd.to_datetime(bpm_operativo_df.index.min(), errors='coerce')
end_date = pd.to_datetime(bpm_operativo_df.index.max(), errors='coerce')

start_date = start_date.strftime('%Y-%m-%d') if pd.notna(start_date) else '2023-01-01'
end_date = end_date.strftime('%Y-%m-%d') if pd.notna(end_date) else pd.Timestamp.today().strftime('%Y-%m-%d')

calidad_dash_layout = html.Div(
    children=[
        html.Header(id='header',
            children=[
                html.Img(id='Logo',
                    src="/assets/Dilusa Logo byn.png",
                    alt="Logo",
                    style={
                        'height': '100px',
                        'backgroundColor': '#2b2b2b',
                    }
                ),
                html.H2(id='header1',
                    children="KPI's Aseguramiento de Calidad e Inocuidad",
                    className='',
                    style={
                        'alignItems': 'center',
                        "justifyContent": "space-around",
                        'display': 'flex',
                        'color': 'white',
                        **styles.GRL
                    }
                )
            ],
            style={
                'backgroundColor': '#2b2b2b',
                'height': '110px',
                'display': 'flex',
                "alignItems": "center",
                }
            ),
        html.Div(id='filtros',
            children=[
                dcc.Dropdown(id='filtro_area',
                    options=[{"label": area, "value": area} for area in filtro_area],
                    value=[],
                    placeholder='Selecciona un área',
                    multi=True,
                    style=styles.DROPDOWN_100
                ),
                dcc.Dropdown(id='filtro_producto',
                    options=filtro,
                    value=[],
                    placeholder='Selecciona un producto',
                    multi=True,
                    style=styles.DROPDOWN_100
                ),
                dcc.DatePickerRange(id='filtro_fecha',
                    start_date=start_date,
                    end_date=end_date,
                    display_format='DD/MM/YYYY',
                    min_date_allowed='2023-01-01',
                    style=styles.DROPDOWN_100
                )
            ]
        ),
        html.Div(id='coliformes57coliformes10',
            children=[
                dcc.Graph(id='coliformes_10',
                    style={
                        'width': '50%',
                        'height': '300px',
                        **styles.GRL
                    }
                ),
                dcc.Graph(id='coliformes_5',
                    style={
                        'width': '50%',
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
        ),
        html.Div(id='mesofilicos/porc_liberaciones',
            children=[
                dcc.Graph(id='mesofilicos',
                    style={
                        'width': '50%',
                        'height': '300px',
                        **styles.GRL
                    }
                ),
                dcc.Graph(id='porc_liberaciones',
                    style={
                        'width': '50%',
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
        ),
        html.Div(id='bpms',
            children=[
                dcc.Graph(id='operativas_graf',
                    style={
                        'width': '50%',
                        'height': '300px',
                        **styles.GRL
                    }
                ),
                dcc.Graph(id='personales_graf',
                    style={
                        'width': '50%',
                        'height': '300px',
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
        ),
    ],
    style=styles.GRL
)


calidad_dash = Dash(__name__)

@calidad_dash.callback(
    Output('porc_liberaciones', 'figure'),
    Input('filtro_producto', 'value')
)
def liberados(filtro_producto):
    liberaciones = actualizar_grafico_liberaciones(filtro_producto)
    return liberaciones

@calidad_dash.callback(
    [
        Output('operativas_graf', 'figure'),
        Output('personales_graf', 'figure')
    ],
    [
        Input('filtro_area', 'value'),
        Input('filtro_fecha', 'start_date'),
        Input('filtro_fecha', 'end_date')
    ]
)
def actualizar_graficos(filtro_area, start_date, end_date):
    print(f"Filtrando datos desde {start_date} hasta {end_date} para área {filtro_area}")  # Debug

    operativas = bpmoperativas(filtro_area, start_date, end_date)
    personales = bpmpersonales(filtro_area, start_date, end_date)

    if operativas is None or personales is None:
        print("❌ Error: No hay datos para mostrar.")

    return operativas, personales

@calidad_dash.callback(
    [
        Output('mesofilicos', 'figure'),
        Output('coliformes_10', 'figure'),
        Output('coliformes_5', 'figure')
        ],
    [
        Input('filtro_producto', 'value')
    ]
)
def actualizar_graficos1(filtro_producto):
    fig_mesofilicos, fig_coliformes_10, fig_coliformes_5 = actualizar_grafico_indicadores(filtro_producto)
    return fig_mesofilicos, fig_coliformes_10, fig_coliformes_5


if __name__ == "__main__":
	calidad_dash.run(debug=False, port='1112')