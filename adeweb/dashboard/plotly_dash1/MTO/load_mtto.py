import pandas as pd

sheets = {
    'PREVENTIVO 2024': 'A:G',
    'PREVENTIVO 2025': 'A:G'
    }

dfs = []
dfs1 = []
with pd.ExcelFile(r"//192.168.10.2/Compartidos/Mantenimiento (192.168.10.254)/KPI'S.xlsx", engine="openpyxl") as workbook:

    for sheet_name, usecols in sheets.items():
        try:
            df_temp = pd.read_excel(
                io=workbook,
                sheet_name=sheet_name,
                usecols=usecols,
                header=0,
                keep_default_na=True
            )
            print(f"{workbook} - {sheet_name}: shape={df_temp.shape}")
            dfs.append(df_temp)
            workbook.close()
        except Exception as e:
            print(f"Error en hoja {sheet_name} del primer workbook: {e}")
    workbook.close()

with pd.ExcelFile(r"//192.168.10.2/Compartidos/Mantenimiento (192.168.10.254)/EL CAPITAN RUBEN/KPI'S MANTENIMIENTO 2025.xlsx", engine="openpyxl") as workbook1:

    # Leer segundo workbook
    for sheet_name, usecols in sheets.items():
        try:
            df_temp1 = pd.read_excel(
                io=workbook1,
                sheet_name=sheet_name,
                usecols=usecols,
                header=0,
                keep_default_na=True
            )
            print(f"{workbook1} - {sheet_name}: shape={df_temp1.shape}")
            dfs1.append(df_temp1)
        except Exception as e:
            print(f"Error en hoja {sheet_name} del segundo workbook: {e}")
    workbook1.close()

if dfs:
    df_wb = pd.concat(dfs, ignore_index=True)
else:
    df_wb = pd.DataFrame()

if dfs1:
    df_wb1 = pd.concat(dfs1, ignore_index=True)
else:
    df_wb1 = pd.DataFrame()

df_wb.columns = df_wb.columns.str.strip()
df_wb1.columns = df_wb1.columns.str.strip()

df_wb['FECHA'] = pd.to_datetime(df_wb['FECHA'], errors='coerce', format='%d/%b/%Y')
df_wb1['FECHA'] = pd.to_datetime(df_wb1['FECHA'], errors='coerce', format='%d/%b/%Y')

df = pd.concat([df_wb, df_wb1], ignore_index=True)

df = df.loc[:, ~df.columns.duplicated()]
df.columns = df.columns.str.strip()
df = df.loc[:, ~df.columns.duplicated()]

df = df.sort_values(by='FECHA', ascending=False)
df = df.dropna(subset=['FECHA'])

# print("Final DF shape:", df.shape)
# print(df.head(20))

df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce', format='%d/%b/%Y')

def convertir_timedelta(val):
    try:
        if isinstance(val, pd.Timedelta):
            return val
        td = pd.to_timedelta(str(val), errors='coerce')
        return td if pd.notnull(td) else pd.Timedelta(seconds=0)
    except Exception:
        return pd.Timedelta(seconds=0)

df['TIEMPO_RAW'] = df['TIEMPO'].apply(convertir_timedelta)
df['TIEMPO'] = df['TIEMPO_RAW'].apply(
    lambda x: f"{int(x.total_seconds() // 3600):02}:{int((x.total_seconds() % 3600) // 60):02}"
)

df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce')

df.rename(
    columns={
        'AGUDO1': 'AGUDO 1',
        'AGUDO2': 'AGUDO 2'
    },
    inplace=True
)

df['ESTATUS'] = df['ESTATUS'].replace('FS', 'FUERA DE SERVICIO')
df0 = df.map(lambda x: x.strip() if isinstance(x, str) else x)
df0 = df0.sort_values(by='FECHA', ascending=False)

sheets = ["CORRECTIVOS 2025", "CORRECTIVOS 2024", "CORRECTIVOS 2023"]
with pd.ExcelFile(r"//192.168.10.2/Compartidos/Mantenimiento (192.168.10.254)/EL CAPITAN RUBEN/DFTO-MTO-020 REGISTRO DE SERVICIOS Y MANTENIMIENTOS CORRECTIVOS.xlsx", engine='openpyxl') as workbook:
    try:
        dfs = []
        for sheet in sheets:
            df = pd.read_excel(
                workbook,
                sheet_name=sheet,
                skiprows=8,
                header=0,
                # usecols="A:L",
            )
            dfs.append(df)
        workbook.close()
        print(f"Se cargaron {len(df)} registros de servicios y correctivos.")
    except Exception as e:
        print(f"No se encontró la hoja de {sheet}")
        workbook.close()

df_correctivos = pd.concat(dfs, ignore_index=True)
df_correctivos.columns = df_correctivos.columns.str.strip(' ')
df_correctivos = df_correctivos.drop(columns=["Unnamed: 0"])
df_correctivos['Fecha de solicitud'] = pd.to_datetime(df_correctivos['Fecha de solicitud'], dayfirst=True, errors='coerce')
df_correctivos['Tiempo de ejecución Hrs/Min'] = pd.to_timedelta(df_correctivos['Tiempo de ejecución Hrs/Min'].astype(str).str.strip(), errors='coerce')
df_correctivos = df_correctivos.sort_values(by='Fecha de solicitud', ascending=False)
df_correctivos['Tipo de mantenimiento'] = df_correctivos['Tipo de mantenimiento'].astype(str).str.strip(' ').str.upper()

df_preventivos = df0
cuenta = len(df_preventivos[df_preventivos['ESTATUS'] == "REALIZADO"]) + len(df_correctivos[df_correctivos['Tipo de mantenimiento'] == "CORRECTIVO"]) + len(df_correctivos[df_correctivos['Tipo de mantenimiento'] == "SERVICIO"])
porc_preventivo = round(len(df_preventivos[df_preventivos['ESTATUS'] == "REALIZADO"]) / cuenta, 2)
porc_correctivo = round(len(df_correctivos[df_correctivos['Tipo de mantenimiento'] == "CORRECTIVO"]) / cuenta, 2)
porc_servicios = round(len(df_correctivos[df_correctivos['Tipo de mantenimiento'] == "SERVICIO"]) / cuenta, 2)
porcentajes = [porc_preventivo, porc_correctivo, porc_servicios]

