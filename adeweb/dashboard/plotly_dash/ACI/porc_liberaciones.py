import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
import warnings
from .load_aci import dfs

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

df_liberaciones = pd.concat(dfs, ignore_index=True)

df_liberaciones.columns = df_liberaciones.columns.str.strip().str.replace('\n', ' ')
df_liberaciones['Producto'] = df_liberaciones['Producto'].apply(lambda x: x.split('/')[-1] if isinstance(x, str) else x)
df_liberaciones['Fecha de siembra'] = pd.to_datetime(df_liberaciones['Fecha de siembra'], errors='coerce')

productos_unicos = df_liberaciones['Producto'].dropna().unique()
productos_unicos = [producto for producto in productos_unicos if producto is not None]

filtro = [{'label': producto, 'value': producto} for producto in productos_unicos]

# liberaciones = Dash(__name__)

# liberaciones.layout = html.Div(
#     children=[
#         dcc.Dropdown(
#             id='producto-filter-liberaciones',
#             options=filtro,
#             value=None,
#             placeholder="Selecciona un producto",
#             multi=True,
#             style={
#                 'width': '500px',
#                 'backgroundColor': '#2A2A2A'
#             },
#         ),
#         dcc.Interval(
#             id='interval-component-liberaciones',
#             interval=3600 * 1000,  # 1 hora en milisegundos
#             n_intervals=0
#         ),
#         dcc.Graph(
#             id='liberaciones-graf',
#             style={
#                 'width': '500px',
#                 'height': '500px'
#             }
#         )
#     ]
# )
# @liberaciones.callback(
#     Output('liberaciones-graf', 'figure'),
#     Input('producto-filter-liberaciones', 'value'))

def actualizar_grafico_liberaciones(filtro_producto):
    # Asegurar que filtro_producto sea una lista
    if filtro_producto is None or len(filtro_producto) == 0:
        df_filtrado = df_liberaciones  # Mostrar todos los datos si no hay selección
    elif isinstance(filtro_producto, str):
        df_filtrado = df_liberaciones[df_liberaciones['Producto'] == filtro_producto]
    else:
        df_filtrado = df_liberaciones[df_liberaciones['Producto'].isin(filtro_producto)]

    total_registros = len(df_filtrado)
    df_agrupado = df_filtrado.groupby('Estatus del producto (Liberado, Retenido, Rechazado)').size().reset_index(name='Conteo')
    df_agrupado['Porcentaje'] = (df_agrupado['Conteo'] / total_registros) * 100

    pt_estatus = go.Figure(
        data=[
            go.Pie(
                labels=df_agrupado['Estatus del producto (Liberado, Retenido, Rechazado)'],
                values=df_agrupado['Porcentaje'],
                textinfo='label+percent',
                insidetextorientation='radial',
                pull=0.05,
                hoverinfo='label+percent')
            ]
        )

    pt_estatus.update_layout(
        title='Porcentaje de Liberación por Estatus',
        template='plotly_dark',
        showlegend=True
    )

    return pt_estatus

# if __name__ == '__main__':
#     liberaciones.run(debug=True)
