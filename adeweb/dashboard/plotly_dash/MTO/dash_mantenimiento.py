import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, dash_table
from . import eficiencia_mtto, porc_mtto
from .porc_mtto import df1
from .load_mtto import df
import warnings
warnings.filterwarnings('ignore')
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import styles


df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce', format='%d/%b/%Y')#.astype(str)
df_mto=df.sort_values(by='FECHA', ascending=False)
df_mto['FECHA'] = df_mto['FECHA'].dt.strftime('%d/%m/%Y')

mantenimiento_dash_layout = html.Div(
    children=[
        html.Header(id='header', 
            className='', 
            children=[
                html.Img(id='Logo',
                    src="/assets/Dilusa Logo byn.png",
                    alt="Logo",
                    style={
                        'height': '100px',
                        'backgroundColor' : '#2b2b2b',
                        }
                    ),
                html.H2(id='header1', 
                    children="KPI's Mantenimiento", 
                    className='', 
                    style = {
                        'alignItems':'center',
                        "justifyContent": "space-around",
                        'display':'flex',
                        'color':'white',
                        **styles.GRL
                        }
                    )
                ],
            style={
                'backgroundColor': '#2b2b2b',
                'height':'110px',
                'display':'flex',
                "alignItems": "center",
            }
        ),
        html.Div(id='filtros', 
            className='', 
            children=[#FILTROS 
                dcc.Dropdown(id='filtro_equipo', 
                    className='',
                    options = [{'label': x.upper(), 'value': x.upper()} for x in df1['EQUIPO'].dropna().unique()],
                    value='',
                    multi=True,
                    placeholder='Selecciona un equipo.',
                    style = styles.DROPDOWN_100
                ),
                dcc.Dropdown(id='filtro_tecnico', 
                    className='',
                    options = [{'label': x.upper(), 'value': x.upper()} for x in df1['TÉCNICO'].dropna().unique()],
                    value='',
                    multi=True,
                    placeholder='Selecciona un técnico.',
                    style = styles.DROPDOWN_100
                ),
                dcc.Dropdown(id='filtro_area', 
                    className='',
                    options = [{'label': x.upper(), 'value': x.upper()} for x in df1['AREA'].dropna().unique()],
                    value='',
                    multi=True,
                    placeholder='Selecciona un área.',
                    style = styles.DROPDOWN_100
                ),
            ]
        ),
        html.Div(id='graficos',
            className='',
            children = [
                dcc.Graph(id='realizados', 
                    style = styles.GRAF_500x500
                ),
                dcc.Graph(id='eficiencia',
                    style = styles.GRAF_500x500
                ),
                dash_table.DataTable(id='tabla-mttos',
                    columns = [{"name": col, "id": col} for col in df.columns if col in ['FECHA','EQUIPO', 'ÁREA', 'ESTATUS']],
                    data = df.to_dict('records'),
                    filter_action = "native",  # Agrega barra de búsqueda
                    page_action = 'none',
                    filter_query = "{ESTATUS} != REALIZADO",
                    style_table = {
                        'width': '500px',  # 🔹 Ajusta el ancho de la tabla
                        'margin': '0 auto',  # 🔹 Centra la tabla horizontalmente
                        'height': '450px',  # 🔹 Ajusta la altura máxima
                        'overflowY': 'scroll',  # 🔹 Agrega scroll vertical
                    },
                    style_cell = {
                        'minWidth': '100px', 
                        'maxWidth': '200px', 
                        'width': 'auto',
                        'whiteSpace': 'normal',
                        'textAlign': 'center',
                        'fontFamily': 'Arial, sans-serif',
                        'fontSize': '14px',
                    },
                    style_header={
                        'backgroundColor': 'black',
                        'color': 'white',
                        'fontWeight': 'bold',
                        'textAlign': 'center',
                        'backgroundColor': '#2b2b2b'
                    },
                    style_data_conditional=[
                        {
                            'if':{'filter_query':"{ESTATUS} = 'REALIZADO'"},
                            'backgroundColor': 'white',
                            'color': 'black'
                        },
                        {  
                            'if': {'filter_query': "{ESTATUS} = 'FUERA DE SERVICIO'"},
                            'backgroundColor': '#ff9e1c',#'',
                            'color': 'black'
                        },
                        {
                            'if': {'filter_query': "{ESTATUS} = 'REPROGRAMADO'"},
                            'backgroundColor': 'red',#'#9d2626',
                            'color': 'white'
                        },
                        {
                            'if':{'filter_query':"{ESTATUS} = 'PROGRAMADO'"},
                            'backgroundColor': 'white',
                            'color': 'black',
                            'fontWeight':'bold'
                        },
                        {
                            'if': {'filter_query': "{ESTATUS} = 'CANCELADO'"},
                            'backgroundColor': 'gray',
                            'color': 'white'
                        },
                        ]
                    )
                ],
            style = {
                'display': 'flex',
                'alignItems': 'flex-start',
                'template': 'plotly_dark',
                **styles.GRL
            },
            )
        ],
    style=styles.GRL
    )


mantenimiento_dash = Dash(__name__)

@mantenimiento_dash.callback(
    [
        Output('realizados', 'figure')
    ],
    [
        Input('filtro_equipo', 'value'),
        Input('filtro_tecnico', 'value'),
        Input('filtro_area', 'value')
        ]
)
def actualizar_grafico(filtro_equipo, filtro_tecnico, filtro_area):
    return (porc_mtto.update_graphs(filtro_equipo, filtro_tecnico, filtro_area),)

@mantenimiento_dash.callback(
    [
        Output('eficiencia', 'figure')
    ],
    [
        Input('filtro_equipo', 'value'),
        Input('filtro_tecnico', 'value'),
        Input('filtro_area', 'value')
        ]
)
def actualizar_grafico(filtro_equipo, filtro_tecnico, filtro_area):
    return (eficiencia_mtto.actualizar_graficos(filtro_equipo, filtro_tecnico, filtro_area),)

if __name__ == "__main__":
	mantenimiento_dash.run(debug=False, port='1111')



