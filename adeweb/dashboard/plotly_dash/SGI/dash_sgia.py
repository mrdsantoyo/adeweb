import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, dash_table, html, Input, Output
from .tif import estatus_general, codigo_entrada
from .load_sgia import load_tif
from .control_documental import control_docs, df_docs
from .ac import eficiencia, requisito_tipo, estatus_grl, df3
from .. import styles

# Cargar y preparar datos
df_tif = load_tif()
df_docs = df_docs.reset_index()
df_docs.rename(columns={"index": "Departamento"}, inplace=True)
df_docs['Eficiencia'] = df_docs['Eficiencia'].apply(lambda x: f"{x}%" if pd.notnull(x) else x)

# sgia_dash = Dash(__name__)

sgia_dash_layout = html.Div(
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
                    children="KPI's SGIA",
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
                dcc.Dropdown(id='filtro_departamento',
                    options=[{"label": str(depto).upper(), "value": str(depto).upper()} for depto in df_tif['Departamento'].unique()],
                    value=[],
                    placeholder='Selecciona un departamento',
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
        html.Div(id='graficos_cd',
            children=[
                dcc.Graph(id='control_documental',
                    figure=go.Figure(),  
                    style={
                        'width': '70%', 
                        'height': '300px', 
                        **styles.GRL
                        }
                ),
                dash_table.DataTable(id='eficiencia_documental',
                    columns=[{"name": col, "id": col} for col in df_docs.columns],
                    data=df_docs.to_dict('records'),
                    filter_action="native",
                    page_action='none',
                    style_table={
                        'width': 'auto',
                        'margin': '0 auto',
                        'height': '300px',
                        'overflowY': 'scroll'
                    },
                    style_cell={
                        'minWidth': '100px',
                        'maxWidth': '200px',
                        'width': 'auto',
                        'whiteSpace': 'normal',
                        'textAlign': 'center',
                        'fontFamily': 'Arial, sans-serif',
                        'fontSize': '14px'
                    },
                    style_header={
                        'backgroundColor': '#2b2b2b',
                        'color': 'white',
                        'fontWeight': 'bold',
                        'textAlign': 'center'
                    },
                    style_data_conditional=[
                        {
                            'if': {'filter_query': "{Eficiencia} < '100'"},
                            'backgroundColor': 'firebrick',
                            'color': 'white'
                        }
                    ]
                )
            ],
            style={
                'display': 'flex', 
                'flexDirection': 'row', 
                'flexWrap': 'wrap', 
                **styles.GRL
                }
        ),
        html.Div(id='graficos_tif',
            children=[
                dcc.Graph(id='tif_pie',
                    figure=go.Figure(),
                    style={
                        'width': '30%', 
                        'height': '300px', 
                        'minHeight': '300px', 
                        **styles.GRL
                        }
                ),
                dcc.Graph(id='codigo_entrada',
                    figure=go.Figure(),
                    style={
                        'width': '70%', 
                        'height': '300px', 
                        'minHeight': '300px', 
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
        html.Div(id='acciones_correctivas',
            children=[
                dcc.Graph(id='estatus_grl',
                    figure=go.Figure(),
                    style={
                        'width': '30%', 
                        'height': '300px',
                        'minHeight': '300px',  
                        **styles.GRL
                    }
                ),
                dcc.Graph(id='eficiencia1',
                    figure=go.Figure(),
                    style={
                        'width': '35%', 
                        'height': '300px', 
                        'minHeight': '300px', 
                        **styles.GRL
                    }
                ),
                dcc.Graph(id='requisito_tipo',
                    figure=go.Figure(),
                    style={
                        'width': '35%', 
                        'height': '300px', 
                        'minHeight': '300px', 
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
    ]
)
