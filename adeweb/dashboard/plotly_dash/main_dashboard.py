# from safety_board.SGIA.load_sgia import load_tif
# from safety_board.MTTO.porc_mtto import df1
# from safety_board.MTTO.load_mtto import df
# from safety_board.ACI.load_aci import bpm_operativo_df, bpm_personales_df
from .SGIA.tif import estatus_general, codigo_entrada
from .SGIA.control_documental import control_documental
from .SGIA.ac import eficiencia, requisito_tipo, estatus_grl, df3
from .MTTO import eficiencia_mtto, porc_mtto
from .ACI.BPM import bpmoperativas, bpmpersonales, filtro_area
from .ACI.mb_indicadores import actualizar_grafico_indicadores, filtro
from .ACI.porc_liberaciones import actualizar_grafico_liberaciones
from dash import Dash, dcc, html, Input, Output
from .dash_sgia import sgia_dash_layout
from .dash_calidad import calidad_dash_layout
from .dash_mantenimiento import mantenimiento_dash_layout
from .POES.dash_poes import poes_dash_layout
from django_plotly_dash import DjangoDash
import styles as styles
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

dashboard_eda = DjangoDash("MiDashboard", suppress_callback_exceptions=True)
dashboard_eda.layout = html.Div(
    style={
        "height": "100%",
        "width": "100%",
        },
    children=[
        dcc.Tabs(id="tabs",
                value="sgia",
            children=[
                dcc.Tab(label="SGIA", 
                    value="sgia",
                    style={
                        "backgroundColor": "#111111",
                        "color":"#888",
                        "border":"none",
                        "fontWeight": "bold",
                        "fontSize": "16px",
                        "padding": "10px"
                        },
                    selected_style={
                        "backgroundColor": "#2b2b2b",
                        "color": "#fff",
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
                dcc.Tab(label="ACI\n(Calidad e Inocuidad)", 
                    value="calidad",
                    style={
                        "backgroundColor": "#111111",
                        "color":"#888",
                        "border":"none",
                        "fontWeight": "bold",
                        "fontSize": "16px",
                        "padding": "10px"
                        },
                    selected_style={
                        "backgroundColor": "#2b2b2b",
                        "color": "#fff",
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
                dcc.Tab(label="POES", 
                    value="poes",
                    style={
                        "backgroundColor": "#111111",
                        "color":"#888",
                        "border":"none",
                        "fontWeight": "bold",
                        "fontSize": "16px",
                        "padding": "10px"
                        },
                    selected_style={
                        "backgroundColor": "#2b2b2b",
                        "color": "#fff",
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
                dcc.Tab(label="Mantenimiento", 
                    value="mantenimiento",
                    style={
                        "backgroundColor": "#111111",
                        "color":"#888",
                        "border":"none",
                        "fontWeight": "bold",
                        "fontSize": "16px",
                        "padding": "10px"
                        },
                    selected_style={
                        "backgroundColor": "#2b2b2b",
                        "color": "#fff",
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
            style={
                'backgroundColor' :'#2b2b2b',
                'border': 'none',
                "height": "50px",
                "width": "100%",
                "fontFamily": "Arial, sans-serif",
                **styles.GRL
                }
            ),
        html.Div(id="tabs-content")
        ]
    )

@dashboard_eda.callback(
    Output("tabs-content", "children"),
    Input("tabs", "value")
    )

def render_tab_content(tab):
    if tab == "sgia":
        return sgia_dash_layout
    elif tab == "calidad":
        return calidad_dash_layout
    elif tab == "mantenimiento":
        return mantenimiento_dash_layout
    elif tab == "poes": #
        return poes_dash_layout #


@dashboard_eda.callback(
    [
        Output('control_documental', 'figure'),
        Output('tif_pie', 'figure'),
        Output('codigo_entrada', 'figure'),
        Output('eficiencia1', 'figure'),
        Output('requisito_tipo', 'figure'),
        Output('estatus_grl', 'figure'),
        ],
    [
        Input('intervalo', 'n_intervals'),
        Input('filtro_departamento', 'value')
        ]
    )
def update_all(n_intervals, filtro_departamento):
    docs = control_documental()
    tif_fig = estatus_general(filtro_departamento)
    ce = codigo_entrada()
    efi = eficiencia(filtro_departamento)
    req_tipo = requisito_tipo()
    estatus_fig = estatus_grl()
    data_efic_doc = df3.to_dict('records')

    return docs, tif_fig, ce, efi, req_tipo, estatus_fig


@dashboard_eda.callback(
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

@dashboard_eda.callback(
    [
        Output('eficiencia', 'figure')
        ],
    [
        Input('filtro_equipo', 'value'),
        Input('filtro_tecnico', 'value'),
        Input('filtro_area', 'value')
        ]
    )
def actualizar_grafico1(filtro_equipo, filtro_tecnico, filtro_area):
    return (eficiencia_mtto.actualizar_graficos(filtro_equipo, filtro_tecnico, filtro_area),)


@dashboard_eda.callback(
    Output('porc_liberaciones', 'figure'),
    Input('filtro_producto', 'value')
    )
def liberados(filtro_producto):
    liberaciones = actualizar_grafico_liberaciones(filtro_producto)
    return liberaciones

@dashboard_eda.callback(
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
    print(f"Filtrando datos desde {start_date} hasta {end_date} para área {filtro_area}")   

    operativas = bpmoperativas(filtro_area, start_date, end_date)
    personales = bpmpersonales(filtro_area, start_date, end_date)

    if operativas is None or personales is None:
        print("❌ Error: No hay datos para mostrar.")

    return operativas, personales

@dashboard_eda.callback(
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


# @dashboard_eda.callback(
#     [
#         Output('serie-temporal', 'figure'),
#         Output('promedios-mensuales', 'figure')
#         ],
#     [
#         Input('filtro_area', 'value')
#         ]
#     )
# def actualizar_poes(filtro_area):
#     serie_temporal, promedios_mensuales = update_graphs(filtro_area)
#     return serie_temporal, promedios_mensuales


if __name__ == '__main__':
    dashboard_eda.run(debug=True, port='1010')




