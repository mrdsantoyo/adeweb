import pandas as pd

sheets = {
    'PREVENTIVO 2024': 'A:G',
    'PREVENTIVO 2025': 'A:G'
    }

dfs = []
dfs1 = []
workbook = r"//192.168.10.2/Compartidos/Mantenimiento (192.168.10.254)/KPI'S.xlsx"
workbook1 = r"//192.168.10.2/Compartidos/Mantenimiento (192.168.10.254)/EL CAPITAN RUBEN/KPI'S MANTENIMIENTO 2025.xlsx"

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
    except Exception as e:
        print(f"Error en hoja {sheet_name} del primer workbook: {e}")

# Leer cada hoja del segundo workbook
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

if dfs:
    df_wb = pd.concat(dfs, ignore_index=True)
else:
    df_wb = pd.DataFrame()

if dfs1:
    df_wb1 = pd.concat(dfs1, ignore_index=True)
else:
    df_wb1 = pd.DataFrame()

# # Antes de concatenar ambos, verifica la columna FECHA
# print(df_wb.shape)
# print(df_wb1.shape)

# CONVERSIÓN DE FECHA
# Ajusta el format a lo que realmente tengas en tus archivos.
# Por ejemplo, si tus fechas se ven como "05/dic/2024", usa '%d/%b/%Y'
# Si en alguno se ven de otra forma, deberás ajustarlo.
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

df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce', format='%d/%b/%Y')#.astype(str)
# df=df.sort_values(by='FECHA', ascending=False)
# df['FECHA1'] = df['FECHA'].dt.strftime('%d/%m/%Y')

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
# df['FECHA'] = df['FECHA'].dt.strftime('%d/%b/%y')

# return df
