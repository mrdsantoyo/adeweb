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
        title='Estatus de liberación',
        template='plotly_white',
        margin=dict(l=30, r=30, t=40, b=30), 
        legend=dict(
            orientation="h", 
            yanchor="bottom",
            y=-0.3,  
            xanchor="right",
            x=0.5
        )
    )

    return pt_estatus

# if __name__ == '__main__':
#     liberaciones.run(debug=True)
