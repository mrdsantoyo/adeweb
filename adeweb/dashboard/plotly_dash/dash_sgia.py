import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, dash_table, html, Input, Output
from SGIA.tif import estatus_general, codigo_entrada
from SGIA.load_sgia import load_tif
from SGIA.control_documental import control_documental, eficiencia_documental
from SGIA.ac import eficiencia, requisito_tipo, estatus_grl, df3
import styles

# Cargar y preparar datos
df_tif = load_tif()
df = eficiencia_documental().reset_index()
df.rename(columns={"index": "Departamento"}, inplace=True)
df['Eficiencia'] = df['Eficiencia'].apply(lambda x: f"{x}%" if pd.notnull(x) else x)

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
                    columns=[{"name": col, "id": col} for col in df.columns],
                    data=df.to_dict('records'),
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

                # dash_table.DataTable(id='acciones_atrasadas',
                #     columns=[{"name": col, "id": col} for col in df3.columns if col in ['Fecha compromiso', 'Departamento', 'Comentario']],
                #     data=df3.to_dict('records'),
                #     filter_action="native",
                #     page_action='none',
                #     style_table={
                #         'width': '20%',
                #         'margin': '0 auto',
                #         'overflowY': 'scroll'
                #     },
                #     style_cell={
                #         'width': 'auto',
                #         'whiteSpace': 'normal',
                #         'textAlign': 'center',
                #         'fontFamily': 'Arial, sans-serif',
                #         'fontSize': '14px'
                #     },
                #     style_header={
                #         'color': 'white',
                #         'fontWeight': 'bold',
                #         'textAlign': 'center',
                #         'backgroundColor': '#2b2b2b'
                #     },
                #     style_data_conditional=[
                #         {
                #             'if': {'filter_query': "{Estatus} = 'REALIZADO'"},
                #             'backgroundColor': 'white',
                #             'color': 'black'
                #         }
                #     ]
                # )
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

# @sgia_dash.callback(
#     [
#         Output('control_documental', 'figure'),
#         # Output('eficiencia_documental', 'data'),   # <-- si quisieras actualizar data
#         Output('tif_pie', 'figure'),
#         Output('codigo_entrada', 'figure'),
#         Output('eficiencia', 'figure'),
#         Output('requisito_tipo', 'figure'),
#         Output('estatus_grl', 'figure'),
#         # Output('acciones_atrasadas', 'data'),    # <-- idem, si quisieras
#     ],
#     [
#         Input('intervalo', 'n_intervals'),
#         Input('filtro_departamento', 'value')
#     ]
# )
# def update_all(n_intervals, filtro_departamento):
#     docs = control_documental()
#     tif_fig = estatus_general(filtro_departamento)
#     ce = codigo_entrada()
#     efi = eficiencia(filtro_departamento)
#     req_tipo = requisito_tipo()
#     estatus_fig = estatus_grl()
#     data_efic_doc = df3.to_dict('records')

#     return docs, tif_fig, ce, efi, req_tipo, estatus_fig#, data_efic_doc

# if __name__ == '__main__':
#     sgia_dash.run(debug=False, port='1113')




