from .ACI.load_aci import bpm_operativo_df
from .ACI.BPM import bpmoperativas, bpmpersonales, filtro_area
from .ACI.mb_indicadores import actualizar_grafico_indicadores, filtro
from .ACI.porc_liberaciones import actualizar_grafico_liberaciones
from .SGI.tif import estatus_general, codigo_entrada
from .SGI.control_documental import control_docs
from .SGI.ac import eficiencia, requisito_tipo, estatus_grl
from .SGI.load_sgia import load_tif, load_control_documental
from .MTO import eficiencia_mtto, porc_mtto
from .MTO.porc_mtto import df, df1, relacion
from .MTO.load_mtto import df0
from .POES.dash_poes import update_graphs, df_poes
from .ALM.dash_alm import almacen
from .SERV_MEDICO.load_sm import fig_atn_area, top_5_atn_area, motivos_atn, generadores, areas_generadores, df_accidentes, df_trayectos, df as df_atencion
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash
from dash import Dash, dcc, html, Input, Output, dash_table
import pandas as pd
import datetime
from . import styles
import sys
import os
from memory_profiler import profile


sys.path.append(os.path.abspath(os.path.dirname(__file__)))

df_docs = load_control_documental().reset_index()
df_docs = df_docs.rename(columns={'index': 'DEPARTAMENTO'})
# df_docs=load_control_documental()
df_docs['Eficiencia'] = ((df_docs['Total de Publicados'] / df_docs['Total'])*100).round(2)
df_docs = df_docs.drop(columns=['Total de Publicados', 'En flujo', 'Ausencia', 'Vigencia v.','Rechazados', 'Total'])

start_date = pd.to_datetime(bpm_operativo_df.index.min(), errors='coerce')
end_date = pd.to_datetime(bpm_operativo_df.index.max(), errors='coerce')
df_tif = load_tif()

dashboard_eda = DjangoDash("Dashboard")
dashboard_eda.layout = html.Div(
    children=[
        dcc.Tabs(
            children=[
                dcc.Tab(label='Calidad', children=[
                    html.Div(id='filtros_aci', children=[
                        dcc.Dropdown(
                            id='filtro_area_aci',
                            options=[{"label": area, "value": area} for area in filtro_area],
                            value=[],
                            placeholder='Selecciona un área',
                            multi=True,
                            style=styles.DROPDOWN_100
                        ),
                        dcc.Dropdown(
                            id='filtro_producto_aci',
                            options=filtro,
                            value=[],
                            placeholder='Selecciona un producto',
                            multi=True,
                            style=styles.DROPDOWN_100
                        ),
                        dcc.DatePickerRange(
                            id='filtro_fecha_aci',
                            start_date=start_date,
                            end_date=end_date,
                            display_format='DD/MM/YYYY',
                            min_date_allowed='2023-01-01',
                            style=styles.DROPDOWN_100
                        )
                    ]),
                    html.Div(id='mesofilicos/porc_liberaciones', children=[
                        dcc.Graph(id='mesofilicos', style={'width': '50%', 'height': '300px', **styles.GRL}),
                        dcc.Graph(id='porc_liberaciones', style={'width': '50%', 'height': '300px', **styles.GRL})
                    ], style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap', **styles.GRL}),
                    html.Div(id='coliformes_5/operativas_graf', children=[
                        dcc.Graph(id='coliformes_5', style={'width': '50%', 'height': '300px', **styles.GRL}),
                        dcc.Graph(id='operativas_graf', style={'width': '50%', 'height': '300px', **styles.GRL})
                    ], style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap', **styles.GRL}),
                    html.Div(id='coliformes_10/personales_graf', children=[
                        dcc.Graph(id='coliformes_10', style={'width': '50%', 'height': '300px', **styles.GRL}),
                        dcc.Graph(id='personales_graf', style={'width': '50%', 'height': '300px', **styles.GRL})
                    ], style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap', **styles.GRL})
                ],                 
                style={
                    "backgroundColor": "#fff",
                    "color":"gray",
                    'fontFamily': 'Arial, sans-serif',
                    "border":"none",
                    "fontWeight": "bold",
                    "fontSize": "16px",
                    "padding": "10px"
                }, 
                selected_style={
                    "backgroundColor": "#f0f0f0",
                    "color": "#000",
                    'fontFamily': 'Arial, sans-serif',
                    "fontWeight": "bold",
                    "fontSize": "16px",
                    "padding": "10px",
                    "borderTop": "2px solid #1f77b4",
                    "borderLeft": "2px solid #1f77b4",
                    "borderRight": "2px solid #1f77b4",
                    "borderBottom": "none",
                    "borderTopLeftRadius": "10px",
                    "borderTopRightRadius": "10px"
                }
                ),
                dcc.Tab(label='Mantenimiento', children=[
                    html.Div(id='filtros_mto', children=[
                        dcc.Dropdown(
                            id='filtro_equipo_mto',
                            options=[{'label': x.upper(), 'value': x.upper()} for x in df1['EQUIPO'].dropna().unique()],
                            value='',
                            multi=True,
                            placeholder='Selecciona un equipo.',
                            style=styles.DROPDOWN_100
                        ),
                        dcc.Dropdown(
                            id='filtro_tecnico_mto',
                            options=[{'label': x.upper(), 'value': x.upper()} for x in df1['TÉCNICO'].dropna().unique()],
                            value='',
                            multi=True,
                            placeholder='Selecciona un técnico.',
                            style=styles.DROPDOWN_100
                        ),
                        dcc.Dropdown(
                            id='filtro_area_mto',
                            options=[{'label': x.upper(), 'value': x.upper()} for x in df1['ÁREA'].dropna().unique()],
                            value='',
                            multi=True,
                            placeholder='Selecciona un área.',
                            style=styles.DROPDOWN_100
                        )
                    ]),
                    html.Div(id='realizados/eficiencia/tabla-mttos', children=[
                        dcc.Graph(id='realizados', style={'width': '30%', **styles.GRL}),
                        dcc.Graph(id='eficiencia', style={'width': '35%', **styles.GRL}),
                        html.Div(dash_table.DataTable(
                            id='tabla-mttos',
                            columns=[{"name": col, "id": col} for col in df0.columns if col in ['FECHA','EQUIPO', 'ÁREA', 'ESTATUS']],
                            data=df.to_dict('records'),
                            filter_action="native",
                            page_action='none',
                            filter_query="{ESTATUS} != REALIZADO",
                            style_table={'width': 'auto', 'margin': '0 auto', 'height': '450px', 'overflowY': 'scroll'},
                            style_cell={'minWidth': '50px', 'width': 'auto', 'whiteSpace': 'normal', 'textAlign': 'center', 'fontFamily': 'Helvetica, sans-serif', 'fontSize': '13px'},
                            style_header={'backgroundColor': '#b3b3b3', 'color': 'black', 'fontWeight': 'bold', 'textAlign': 'center'},
                            style_data_conditional=[
                                {'if': {'filter_query': "{ESTATUS} = 'REALIZADO'"}, 'backgroundColor': 'white', 'color': 'MediumSeaGreen'},
                                {'if': {'filter_query': "{ESTATUS} = 'FUERA DE SERVICIO'"}, 'backgroundColor': '#ff9e1c', 'color': 'black'},
                                {'if': {'filter_query': "{ESTATUS} = 'REPROGRAMADO'"}, 'backgroundColor': 'firebrick', 'color': 'white'},
                                {'if': {'filter_query': "{ESTATUS} = 'PROGRAMADO'"}, 'backgroundColor': 'white', 'color': 'black', 'fontWeight': 'bold'},
                                {'if': {'filter_query': "{ESTATUS} = 'CANCELADO'"}, 'backgroundColor': 'gray', 'color': 'white'}
                            ]
                        ), style={'width': '35%', 'display': 'inline-block'})
                    ], style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'nowrap', 'width': '100%', **styles.GRL}),
                    html.Div(id='correctivos', children=[
                        dcc.Graph(id='relacion',
                            style={'width': '30%', **styles.GRL}
                        )
                    ])
                ],                 
                style={
                    "backgroundColor": "#fff",
                    "color":"gray",
                    'fontFamily': 'Arial, sans-serif',
                    "border":"none",
                    "fontWeight": "bold",
                    "fontSize": "16px",
                    "padding": "10px"
                }, 
                selected_style={
                    "backgroundColor": "#f0f0f0",
                    "color": "#000",
                    'fontFamily': 'Arial, sans-serif',
                    "fontWeight": "bold",
                    "fontSize": "16px",
                    "padding": "10px",
                    "borderTop": "2px solid #1f77b4",
                    "borderLeft": "2px solid #1f77b4",
                    "borderRight": "2px solid #1f77b4",
                    "borderBottom": "none",
                    "borderTopLeftRadius": "10px",
                    "borderTopRightRadius": "10px"
                }
                ),
                dcc.Tab(label='Almacén', children=[
                    html.Div(id='filtros_alm', children=[
                        dcc.Interval(id='intervalo_alm', interval=3600, n_intervals=0, disabled=True)
                    ]),
                    html.Div(id='almacen-graphs', children=[
                        dcc.Graph(id='almacen', style={'width': '100%', 'height': '300px', **styles.GRL})
                    ], style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap', **styles.GRL})
                ],                 
                style={
                    "backgroundColor": "#fff",
                    "color":"gray",
                    'fontFamily': 'Arial, sans-serif',
                    "border":"none",
                    "fontWeight": "bold",
                    "fontSize": "16px",
                    "padding": "10px"
                }, 
                selected_style={
                    "backgroundColor": "#f0f0f0",
                    "color": "#000",
                    'fontFamily': 'Arial, sans-serif',
                    "fontWeight": "bold",
                    "fontSize": "16px",
                    "padding": "10px",
                    "borderTop": "2px solid #1f77b4",
                    "borderLeft": "2px solid #1f77b4",
                    "borderRight": "2px solid #1f77b4",
                    "borderBottom": "none",
                    "borderTopLeftRadius": "10px",
                    "borderTopRightRadius": "10px"
                }
                ),
                dcc.Tab(label='SGIA', children=[
                    html.Div(id='filtros_sgi', children=[
                        dcc.Interval(id='intervalo_sgi', interval=3600, n_intervals=0, disabled=True),
                        dcc.Dropdown(
                            id='filtro_departamento_sgi',
                            options=[{"label": str(depto).upper(), "value": str(depto).upper()} for depto in df_tif['Departamento'].unique()],
                            value=[],
                            placeholder='Selecciona un departamento',
                            multi=True,
                            style=styles.DROPDOWN_100
                        )
                    ]),
                    html.Div(id='control_documental/eficiencia_documental', children=[
                        dcc.Graph(id='control_documental', figure=go.Figure(), style={'width': '70%', 'height': '300px', **styles.GRL}),
                        html.Div(dash_table.DataTable(
                            id='eficiencia_documental',
                            columns=[{"name": col, "id": col} for col in df_docs],
                            data=df_docs.to_dict('records'),
                            filter_action="native",
                            page_action='none',
                            style_table={'width': 'auto', 'margin': '0 auto', 'height': '300px', 'overflowY': 'scroll'},
                            style_cell={'minWidth': '80px', 'maxWidth': '165px', 'width': 'auto', 'whiteSpace': 'normal', 'textAlign': 'center', 'fontFamily': 'Helvetica, sans-serif', 'fontSize': '14px'},
                            style_header={'backgroundColor': '#b3b3b3', 'color': 'black', 'fontWeight': 'bold', 'textAlign': 'center'},
                            style_data_conditional=[
                                {'if': {'filter_query': "{Eficiencia} <= '50'"}, 'backgroundColor': 'firebrick', 'color': 'white'},
                                {'if': {'filter_query': "{Eficiencia} >='99'"}, 'backgroundColor': '#8af49a', 'color': 'black'}
                                ]
                        ), style={'width': '30%', 'display': 'inline-block'})
                    ], style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap', **styles.GRL}),
                    html.Div(id='tif_pie/codigo_entrada', children=[
                        dcc.Graph(id='tif_pie', figure=go.Figure(), style={'width': '30%', 'height': '300px', 'minHeight': '300px', **styles.GRL}),
                        dcc.Graph(id='codigo_entrada', figure=go.Figure(), style={'width': '70%', 'height': '300px', 'minHeight': '300px', **styles.GRL})
                    ], style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap', **styles.GRL}),
                    html.Div(id='acciones_correctivas', children=[
                        dcc.Graph(id='estatus_grl', figure=go.Figure(), style={'width': '30%', 'height': '300px', 'minHeight': '300px', **styles.GRL}),
                        dcc.Graph(id='eficiencia1', figure=go.Figure(), style={'width': '35%', 'height': '300px', 'minHeight': '300px', **styles.GRL}),
                        dcc.Graph(id='requisito_tipo', figure=go.Figure(), style={'width': '35%', 'height': '300px', 'minHeight': '300px', **styles.GRL})
                    ], style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap', **styles.GRL})
                ],                 
                style={
                    "backgroundColor": "#fff",
                    "color":"gray",
                    'fontFamily': 'Arial, sans-serif',
                    "border":"none",
                    "fontWeight": "bold",
                    "fontSize": "16px",
                    "padding": "10px"
                }, 
                selected_style={
                    "backgroundColor": "#f0f0f0",
                    "color": "#000",
                    'fontFamily': 'Arial, sans-serif',
                    "fontWeight": "bold",
                    "fontSize": "16px",
                    "padding": "10px",
                    "borderTop": "2px solid #1f77b4",
                    "borderLeft": "2px solid #1f77b4",
                    "borderRight": "2px solid #1f77b4",
                    "borderBottom": "none",
                    "borderTopLeftRadius": "10px",
                    "borderTopRightRadius": "10px"
                }
                ),
                dcc.Tab(label='POES', children=[
                    html.Div(id='filtros_poes', children=[
                        dcc.Interval(id='intervalo_poes', interval=3600, n_intervals=0, disabled=True),
                        dcc.Dropdown(
                            id='filtro_area_poes',
                            options=[{'label': area.strip(), 'value': area.strip()} for area in df_poes.columns if area not in ['Promedios Diarios']], value=[],
                            placeholder='Selecciona un departamento.',
                            multi=True,
                            style=styles.DROPDOWN_100
                        )
                    ]),
                    html.Div(id='serie-temporal/promedios-mensuales/', children=[
                        dcc.Graph(id='tendencias', style={'width': '100%','height': '300px', **styles.GRL}),
                        dcc.Graph(id='serie-temporal', style={'width': '50%', 'height': '300px', **styles.GRL}),
                        dcc.Graph(id='promedios-mensuales', style={'width': '50%', 'height': '300px', **styles.GRL}),
                    ], style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap', **styles.GRL})
                ],                 
                style={
                    "backgroundColor": "#fff",
                    "color":"gray",
                    'fontFamily': 'Arial, sans-serif',
                    "border":"none",
                    "fontWeight": "bold",
                    "fontSize": "16px",
                    "padding": "10px"
                }, 
                selected_style={
                    "backgroundColor": "#f0f0f0",
                    "color": "#000",
                    'fontFamily': 'Arial, sans-serif',
                    "fontWeight": "bold",
                    "fontSize": "16px",
                    "padding": "10px",
                    "borderTop": "2px solid #1f77b4",
                    "borderLeft": "2px solid #1f77b4",
                    "borderRight": "2px solid #1f77b4",
                    "borderBottom": "none",
                    "borderTopLeftRadius": "10px",
                    "borderTopRightRadius": "10px"
                }
                ),
                dcc.Tab(label='Servicio médico', children=[
                    html.Div(id='filtros_sm', children=[
                        dcc.Interval(id='intervalo_sm', interval=3600, n_intervals=0, disabled=True),
                        dcc.DatePickerRange(
                            id='filtro_fecha',
                            start_date = df_atencion['Fecha'].min(),
                            end_date = df_atencion['Fecha'].max(),
                            display_format='DD/MM/YYYY',
                            style=styles.DROPDOWN_100

                        ),
                    ]),
                    html.Div(id='row1', children=[
                        dcc.Graph(id='top_5_atn_area', 
                            style={
                                'width':'35%',
                                'height': '300px', 
                                **styles.GRL
                                }
                            ),
                        html.Div(id='card-valor',
                            style={
                                'border': '1px solid #ddd',
                                'borderRadius': '5px',
                                'padding': '20px',
                                'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
                                'width': '25%',
                                'margin': '10px',
                                'textAlign': 'center',
                                'backgroundColor': '#ffffff',
                                'display': 'flex',
                                'flexDirection': 'column',
                                'gap': '15px'  # Espacio entre elementos
                            },                            
                            children=[
                                html.H3("ST-7: Accidentes", 
                                    style={'margin': '0', 'color': '#c0392b'}),
                                html.Hr(style={'margin': '8px 0', 'borderColor': '#f5b7b1'}),
                                html.P("Dictaminados como de trabajo", 
                                    style={'margin': '5px 0', 'fontStyle': 'italic'}),
                                html.H2(f"{len(df_accidentes)}", 
                                    style={'margin': '10px 0', 'color': '#e74c3c', 'fontSize': '28px'}),                                
                                html.Hr(style={'margin': '8px 0', 'borderColor': '#f5b7b1'}),
                                html.P("Dictaminados como de trayecto", 
                                    style={'margin': '5px 0', 'fontStyle': 'italic'}),
                                html.H2(f"{len(df_trayectos)}", 
                                    style={'margin': '10px 0', 'color': '#e74c3c', 'fontSize': '28px'}),
                                html.P(f"Actualizado al {df_accidentes['TERMINA INC'].max().strftime('%d/%m/%Y')} ", 
                                    style={'align':'bottom','margin': '0', 'fontSize': '12px', 'alignSelf': 'flex-start'}),
                            ]
                        )
                    ], style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap', **styles.GRL}),
                    html.Div(id='row2', children=[
                        dcc.Graph(id='fig_atn_area', style={'width': '50%', 'height': '300px',  **styles.GRL}),
                        dcc.Graph(id='motivos_atn', style={'width': '50%', 'height': '300px', **styles.GRL}),
                    ], style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap', **styles.GRL}),
                    html.Div(id='row3', children=[
                        dcc.Graph(id='generadores_accidentes', style={'width': '30%', 'height': '300px',  **styles.GRL}),
                        dcc.Graph(id='areas_generadores', style={'width': '30%', 'height': '300px',  **styles.GRL}),
                    ], style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap', **styles.GRL})                ],                 
                style={
                    "backgroundColor": "#fff",
                    "color":"gray",
                    'fontFamily': 'Arial, sans-serif',
                    "border":"none",
                    "fontWeight": "bold",
                    "fontSize": "16px",
                    "padding": "10px"
                }, 
                selected_style={
                    "backgroundColor": "#f0f0f0",
                    "color": "#000",
                    'fontFamily': 'Arial, sans-serif',
                    "fontWeight": "bold",
                    "fontSize": "16px",
                    "padding": "10px",
                    "borderTop": "2px solid #1f77b4",
                    "borderLeft": "2px solid #1f77b4",
                    "borderRight": "2px solid #1f77b4",
                    "borderBottom": "none",
                    "borderTopLeftRadius": "10px",
                    "borderTopRightRadius": "10px"
                }
                ),
            ],
            style={'backgroundColor': '#ffffff'}
        )
    ],
    style={'width': '100%', 'height': '100%', 'margin': '0', 'padding': '0'}
)

##ACI CALLBACK
@dashboard_eda.callback(
    [
        Output("mesofilicos","figure"),
        Output("porc_liberaciones","figure"),
        Output("coliformes_5","figure"),
        Output("operativas_graf","figure"),
        Output("coliformes_10","figure"),
        Output("personales_graf","figure"),
        ],
    [
        Input("filtro_area_aci","value"),
        Input("filtro_producto_aci","value"),
        Input('filtro_fecha_aci', 'start_date'),
        Input('filtro_fecha_aci', 'end_date')

        ]
)

def graficos_aci(filtro_area, filtro_producto, start_date, end_date, **kwargs):
    liberaciones = actualizar_grafico_liberaciones(filtro_producto)
    
    print(f"Filtrando datos desde {start_date} hasta {end_date} para área {filtro_area}")   

    operativas = bpmoperativas(filtro_area, start_date, end_date)
    personales = bpmpersonales(filtro_area, start_date, end_date)

    if operativas is None or personales is None:
        print("❌ Error: No hay datos para mostrar.")
        
    fig_mesofilicos, fig_coliformes_10, fig_coliformes_5 = actualizar_grafico_indicadores(filtro_producto)

    
    return fig_mesofilicos, liberaciones, fig_coliformes_5, operativas, fig_coliformes_10, personales

##MTTO CALLBACK
@dashboard_eda.callback(
    [
        Output("realizados","figure"),
        Output("eficiencia","figure"),
        Output("relacion","figure"),
        ],
    [
        Input("filtro_equipo_mto","value"),
        Input("filtro_tecnico_mto","value"),
        Input("filtro_area_mto", "value"),

        ]
)

def graficos_mto(filtro_equipo, filtro_tecnico, filtro_area, **kwargs):
    return (porc_mtto.update_graphs(filtro_equipo, filtro_tecnico, filtro_area),
            eficiencia_mtto.actualizar_graficos(filtro_equipo, filtro_tecnico, filtro_area),
            porc_mtto.relacion(),
            )

##SGIA CALLBACK
@dashboard_eda.callback(
    [
        Output("control_documental","figure"),
        Output("eficiencia_documental","data"),
        Output("tif_pie","figure"),
        Output("codigo_entrada","figure"),
        Output("eficiencia1","figure"),  # Cambiado de acciones_correctivas a eficiencia1
        Output("estatus_grl","figure"),
        Output("requisito_tipo","figure"),
        
        # Output("control_documental","figure"),
        # Output("eficiencia_documental","data"),
        # Output("tif_pie","figure"),
        # Output("codigo_entrada","figure"),
        # Output("acciones_correctivas","figure"),
        # Output("estatus_grl","figure"),
        ],
    [
        Input("intervalo_sgi","n_intervals"),
        Input("filtro_departamento_sgi","value"),
        ]
    )


def graficos_sgi(n_intervals, filtro_departamento, **kwargs ):
    docs = control_docs()
    # from SGI.control_documental import df_docs
    df_docs_reset = df_docs.reset_index().rename(columns={'index': 'DEPARTAMENTO'})
    eficiencia_datos = df_docs_reset.to_dict('records')
    tif_fig = estatus_general(filtro_departamento)
    ce = codigo_entrada()
    efi = eficiencia(filtro_departamento)
    req_tipo = requisito_tipo()
    estatus_fig = estatus_grl()

    return (docs, eficiencia_datos, tif_fig, ce, efi, estatus_fig, req_tipo)

##POES CALLBACK
@dashboard_eda.callback(
    [
        Output('tendencias', 'figure'),
        Output('serie-temporal', 'figure'),
        Output('promedios-mensuales', 'figure'),
    ],
    [
        Input("filtro_area_poes","value"),
    ]
    )


def graficos_poes(areas_a_mostrar, **kwargs):
    fig_tendencias, fig_serie, fig_promedios = update_graphs(areas_a_mostrar)
    return fig_tendencias, fig_serie, fig_promedios

###ALMACEN CALLBACK
@dashboard_eda.callback(
    Output("almacen","figure"),
    Input("intervalo_alm","n_intervals"),
    )


def almacen1(n_intervals):
    decomisos_alm = almacen()
    return decomisos_alm

### SERVICIO MEDICO CALLBACK
@dashboard_eda.callback(
    [
        Output("top_5_atn_area","figure"),    
        Output("fig_atn_area","figure"),
        Output("motivos_atn","figure"),
        Output("generadores_accidentes","figure"),
        Output("areas_generadores","figure"),
    ],
    [
        Input("intervalo_sm","n_intervals"),
        Input("filtro_fecha","start_date"),
        Input("filtro_fecha","end_date"),
    ]
)


def serv_med(n_intervals, start_date, end_date):
    return top_5_atn_area(n_intervals, start_date, end_date), fig_atn_area(n_intervals), motivos_atn(n_intervals), generadores(n_intervals, start_date, end_date), areas_generadores(n_intervals, start_date, end_date)

# if __name__ == '__main__':
#     dashboard_eda.run(debug=True)  # Set use_reloader=False to avoid duplicate callbacks during development
#     # dashboard_eda


