import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
import warnings
from .load_aci import dfs

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

dfs = pd.concat(dfs, ignore_index=True)
dfs.columns = dfs.columns.str.strip().str.replace('\n', ' ')

df_mesofilicos = dfs.loc[:, ['Folio', 'Producto', 'Fecha de siembra', 'Mesofilicos <10,000 UFC/g', 'Cta. Total Mesofilicos  <10,000 UFC/g']].copy()
df_coliformes = dfs.loc[:, ['Folio', 'Producto', 'Fecha de siembra', 'Cta. Total Coliformes  <10 UFC/g', 'Coliformes  <10 UFC/g', 'Cta. Total Coliformes  <5000 UFC/g', 'Cta. Total Coliformes  <5,000 UFC/g']].copy()

df_mesofilicos.rename(
    columns={
        'Mesofilicos <10,000 UFC/g': 'Mesofilicos_1', 
        'Cta. Total Mesofilicos  <10,000 UFC/g': 'Mesofilicos_2'
        }, 
    inplace=True
    )
df_coliformes.rename(
    columns={
        'Cta. Total Coliformes  <10 UFC/g': 'coliformes_1', 
        'Coliformes  <10 UFC/g': 'coliformes_2', 
        'Cta. Total Coliformes  <5000 UFC/g': 'coliformes_3', 
        'Cta. Total Coliformes  <5,000 UFC/g': 'coliformes_4'
        }, 
    inplace=True
    )

df_mesofilicos['Mesofilicos (UFC/g)'] = df_mesofilicos['Mesofilicos_1'].combine_first(df_mesofilicos['Mesofilicos_2']).replace('INC', 55500).astype(float)
df_coliformes['Coliformes (<10 UFC/g)'] = df_coliformes['coliformes_1'].combine_first(df_coliformes['coliformes_2']).replace('INC', 220).astype(float)
df_coliformes["Coliformes (<5'000 UFC/g)"] = df_coliformes['coliformes_3'].combine_first(df_coliformes['coliformes_4']).replace('INC', 10000).astype(float)

df_mesofilicos['Fecha de siembra'] = pd.to_datetime(df_mesofilicos['Fecha de siembra'], errors='coerce')
df_coliformes['Fecha de siembra'] = pd.to_datetime(df_coliformes['Fecha de siembra'], errors='coerce')

df_mesofilicos['Producto'] = df_mesofilicos['Producto'].apply(lambda x: x.split('/')[-1] if isinstance(x, str) else x)
df_coliformes['Producto'] = df_coliformes['Producto'].apply(lambda x: x.split('/')[-1] if isinstance(x, str) else x)

productos_unicos = df_mesofilicos['Producto'].dropna().unique()
filtro = [{'label': producto, 'value': producto} for producto in productos_unicos if producto is not None]

indicadores_mb = Dash(__name__)
indicadores_mb.layout = html.Div(
    children=[
        dcc.Dropdown(
            id='producto-filter', 
            options=filtro, 
            # value=
            placeholder="Selecciona productos para filtrar", 
            multi=True, 
            style={'width': '750px', 'backgroundColor': '#1A1A1A'}
        ),
        dcc.Graph(
            id='mesofilicos-graf', 
            style={
                'width': '750px', 
                'height': '300px'
                }
            ),
        dcc.Graph(
            id='coliformes-10-graf', 
            style={
                'width': '750px', 
                'height': '300px'
                }
            ),
        dcc.Graph(
            id='coliformes-5-graf', 
            style={
                'width': '750px', 
                'height': '300px'
                }
            )
        ]
    )
@indicadores_mb.callback(
    [
        Output('mesofilicos-graf', 'figure'), 
        Output('coliformes-10-graf', 'figure'), 
        Output('coliformes-5-graf', 'figure')
    ],
    [
        Input('producto-filter', 'value')
    ]
)
def actualizar_grafico_indicadores(filtro_producto):
    fig_mesofilicos, fig_coliformes_10, fig_coliformes_5 = go.Figure(), go.Figure(), go.Figure()
    
    if not filtro_producto:
        for fig in [fig_mesofilicos, fig_coliformes_10, fig_coliformes_5]:
            fig.add_annotation(
                x=0.5, y=0.5, text="Selecciona productos para filtrar",
                showarrow=False, font=dict(size=20),
                xref="paper", yref="paper"
            )
            fig.update_layout(
                xaxis_title='Fecha', 
                yaxis_title='UFC/g', 
                template='plotly_dark', 
                showlegend=False
            )
        return fig_mesofilicos, fig_coliformes_10, fig_coliformes_5

    df_mesofilicos_filtrado = df_mesofilicos[df_mesofilicos['Producto'].isin(filtro_producto)]
    df_coliformes_filtrado = df_coliformes[df_coliformes['Producto'].isin(filtro_producto)]

    fig_mesofilicos.add_trace(
        go.Scatter(
            x=[df_mesofilicos['Fecha de siembra'].min(), df_mesofilicos['Fecha de siembra'].max()], 
            y=[10000, 10000], mode='lines', line=dict(color='red', width=1, dash='dash'), name="Límite"
            )
        )
    fig_coliformes_10.add_trace(
        go.Scatter(
            x=[df_coliformes['Fecha de siembra'].min(), df_coliformes['Fecha de siembra'].max()], 
            y=[10, 10], mode='lines', line=dict(color='red', width=1, dash='dash'), name="Límite"
            )
        )
    fig_coliformes_5.add_trace(
        go.Scatter(
            x=[df_coliformes['Fecha de siembra'].min(), df_coliformes['Fecha de siembra'].max()], 
            y=[5000, 5000], mode='lines', line=dict(color='red', width=1, dash='dash'), name="Límite"
            )
        )

    for producto in df_mesofilicos_filtrado['Producto'].unique():
        df_producto = df_mesofilicos_filtrado[df_mesofilicos_filtrado['Producto'] == producto]
        fig_mesofilicos.add_trace(
            go.Scatter(
                x=df_producto['Fecha de siembra'], 
                y=df_producto['Mesofilicos (UFC/g)'], 
                mode='markers', 
                name=producto
                )
            )

    for producto in df_coliformes_filtrado['Producto'].unique():
        df_producto = df_coliformes_filtrado[df_coliformes_filtrado['Producto'] == producto]
        fig_coliformes_10.add_trace(
            go.Scatter(
                x=df_producto['Fecha de siembra'], 
                y=df_producto['Coliformes (<10 UFC/g)'], 
                mode='markers', 
                name=producto
                )
            )
        fig_coliformes_5.add_trace(
            go.Scatter(
                x=df_producto['Fecha de siembra'], 
                y=df_producto["Coliformes (<5'000 UFC/g)"], 
                mode='markers', 
                name=producto
                )
            )
    fig_mesofilicos.update_layout(
        title="Mesofílicos (<10'000 UFC/g)", 
        xaxis_title='Fecha', 
        yaxis_title='UFC/g', 
        template='plotly_dark', 
        showlegend=False
    )
    fig_coliformes_10.update_layout(
        title='Coliformes (<10 UFC/g)', 
        xaxis_title='Fecha', 
        yaxis_title='UFC/g', 
        template='plotly_dark', 
        showlegend=False
    )
    fig_coliformes_5.update_layout(
        title="Coliformes (<5'000 UFC/g)", 
        xaxis_title='Fecha', 
        yaxis_title='UFC/g', 
        template='plotly_dark', 
        showlegend=True
    )
    return fig_mesofilicos, fig_coliformes_10, fig_coliformes_5

# if __name__ == '__main__':
#     indicadores_mb.run(debug=True, port='8051')
