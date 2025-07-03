import plotly.graph_objects as go
import pandas as pd
from .load_alm import df, semanal


def almacen():

    semana = go.Figure()
    semana.add_trace(
        go.Bar(
            name="Decomiso semanal",
            x=semanal["SEMANA"],
            y=semanal["KILOS"],
            marker_color="royalblue",
            opacity=0.8,
            hovertemplate="Semana %{x}:<extra> %{y} kg.</extra>",  # Corregido

            xaxis='x',
        )
    )
    semana.add_trace(
        go.Scatter(
            name="Decomiso x vale",
            x=df["FECHA DE ENTREGA"],
            y=df["KILOS"],
            mode="markers",
            line=dict(color="red", width=2, dash="dash"),
            hovertemplate="%{x}: <extra>%{y} kg.</extra>",
            opacity=0.8,
            xaxis='x2',
        )
    )
    semana.update_layout(
        template="plotly_white",
        title=f"Decomisos de la semana {semanal['SEMANA'].min()} a la {semanal['SEMANA'].max()}`      Total: {semanal['KILOS'].sum():.2f} kg.",
        xaxis_title="Fecha",
        xaxis=dict(
            showticklabels=False,
            tickmode='linear',
            dtick=1,
            tickfont=dict(size=10),
            tickcolor='white',
            ticklen=5,
            ticktext=semanal['SEMANA'],
        ),
        xaxis2=dict(
            showticklabels=True,
            anchor='y',
            domain=[0, 0.9],
            overlaying='x',
        ),
        yaxis_title="Kilos",
        clickmode='select',
    )
    return semana


