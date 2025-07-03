import numpy as np
import pandas as pd
import plotly.graph_objects as go
# from dash import Dash, dcc, html, Input, Output

with pd.ExcelFile(r"//192.168.10.2/Compartidos/Almacen/DECOMISO PLANTA ALM004/2025/CONTROL DE VALES 2025.xlsx", engine='openpyxl') as workbook:
    try:
        dfs = []
        for sheet in workbook.sheet_names:
            if sheet == "ENERO 2025":    
                df = pd.read_excel(
                    workbook,
                    sheet_name=sheet,
                    header=None,
                    skiprows=8,
                    names=["FECHA DE ENTREGA", "KILOS", "AREA", "FOLIO VALE"],
                )
            else:
                df = pd.read_excel(
                    workbook,
                    sheet_name=sheet,
                    header=0,
                )
            dfs.append(df)
        print(f"Se cargaron ({dfs.shape[0]} filas y {dfs.shape[1]}) registros de decomiso.")

        workbook.close()
    except Exception as e:
        print(f"No se encontró la hoja del mes {sheet} de decomisos.")
        workbook.close()
    df = pd.concat(dfs)
    
    df_preventivos = df.copy()
    df_preventivos["FECHA DE ENTREGA"] = pd.to_datetime(df["FECHA DE ENTREGA"], dayfirst=True, errors="coerce") 
    df_preventivos = df_preventivos.sort_values(by='FECHA DE ENTREGA', ascending=True)
    df_preventivos["FOLIO VALE"] = df_preventivos["FOLIO VALE"].replace("FOLIO VALE", np.nan)
    df_preventivos['FOLIO VALE'] = pd.to_numeric(df_preventivos['FOLIO VALE'], errors='coerce')
    df_preventivos = df_preventivos.dropna(subset="FOLIO VALE", axis=0)

df_preventivos['SEMANA'] = df_preventivos['FECHA DE ENTREGA'].dt.isocalendar().week
df_preventivos['FECHA'] = pd.to_numeric(df_preventivos['FECHA DE ENTREGA'], errors='coerce')

semanal = df_preventivos.groupby(by='SEMANA')['KILOS'].sum().reset_index()
diario = df_preventivos.groupby(by='FECHA')['KILOS'].sum().reset_index()






