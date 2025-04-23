import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

##### LIBERACIÓN de PT ######
dfs = []
sheets = {
    "CHICHARRÓN PRENSADO": "A,C:F,L:Q,S,T,X:AF",
    "PELLET": "A,C:F,L:Q,S,T,X:AJ",
    "PORCIONADOS": "A,C:E,K:O,Q,R,V:AA",
    "EMBUTIDOS": "A,C:E,K:Q,S,T,X:AB",
    "MANTECA": "A,C:E,J:Q,S,T,X:AF",
    "AHUMADOS": "A,C:F,L,N:Q,S,T,X:AC",
    "CARNE PARA HAMBURGUESA Y MOLIDA": "A,C:E,K:O,Q,R,V:Z",
    "ARRACHERA": "A,C:E,K:P,R,S,W:AB",
    "COCIDOS Y ESTERILIZADOS": "A,C:D,F,G,M:Q,S,T,X:AE"
    }

for sheet_name, cols in sheets.items():
    try:
        # workbook = pd.ExcelFile("Excel\\D-FTO-ACI-083 Bitácora de liberación de PT 2025.xlsx")
        workbook = pd.ExcelFile("//192.168.10.2/Compartidos/Calidad Compartida (192.168.10.254)/8. BITACORA DE LIBERACIÓN DE PT Y MP/D-FTO-ACI-083 Bitácora de liberación de PT 2025.xlsx")
        df = pd.read_excel(
            workbook,
            sheet_name=sheet_name,
            usecols=cols,
            skiprows=8  # Saltar filas irrelevantes
        )
        dfs.append(df)
    except Exception as e:
        print(f"Error cargando {sheet_name}: {e}")
        pass

##### BPM's OPERATIVAS ######
sheets_bpm = {
    "ENERO": "A:P",
    "FEBRERO": "A:Q",
    "MARZO": "A:M",
    "ABRIL": "A:K",
    "MAYO": "A:L",
    "JUNIO": "A:K",
    "JULIO": "A:K",
    "AGOSTO": "A:K",
    "SEPTIEMBRE": "A:K",
    "OCTUBRE": "A:K",
    "NOVIEMBRE": "A:K",
    "DICIEMBRE": "A:K"
    }

bpm_operativo_df = pd.DataFrame()
for sheet, cols in sheets_bpm.items():
    try:
        # workbook_bpm = pd.ExcelFile(r"C:/Users/daniel.santoyo/KPI-EDA/Excel/Bitacora de BPM's 2025.xlsx")
        workbook_bpm = pd.ExcelFile(r"//192.168.10.2/Compartidos/Calidad Compartida (192.168.10.254)/5. KPI´s calidad/2025/Bitacora de BPM's 2025.xlsx")
        temp_df = pd.read_excel(
            workbook_bpm,
            sheet_name=sheet,
            usecols=cols,
            nrows=21,
            header=1
        )
        bpm_operativo_df = pd.concat([bpm_operativo_df, temp_df], axis=1)
    except Exception as e:
        # print(f"✖️ La hoja {sheet} en {workbook_bpm.book if hasattr(workbook_bpm, 'book') else 'workbook'} no existe: {e}")
        pass
bpm_operativo_df = bpm_operativo_df.T
bpm_operativo_df.columns = bpm_operativo_df.iloc[0]
bpm_operativo_df = bpm_operativo_df.drop(bpm_operativo_df.index[0])
bpm_operativo_df = bpm_operativo_df.drop(columns=['AREA', np.nan], errors='ignore')
bpm_operativo_df = bpm_operativo_df.fillna(0)
bpm_operativo_df['PROMEDIOS DIARIOS'] = bpm_operativo_df.mean(axis=1, numeric_only=True).round(2)
bpm_operativo_df.columns = bpm_operativo_df.columns.str.strip().str.upper()
bpm_operativo_df.index = bpm_operativo_df.index.rename('FECHA')
bpm_operativo_df = bpm_operativo_df[bpm_operativo_df["PROMEDIOS DIARIOS"] != 0]
bpm_operativo_df.index = pd.to_datetime(bpm_operativo_df.index)
bpm_operativo_df['MES'] = bpm_operativo_df.index.month
bpm_operativo_df['MES'] = bpm_operativo_df['MES'].map(
    {
        1: 'ENERO',
        2: 'FEBRERO',
        3: 'MARZO',
        4: 'ABRIL',
        5: 'MAYO',
        6: 'JUNIO',
        7: 'JULIO',
        8: 'AGOSTO',
        9: 'SEPTIEMBRE',
        10: 'OCTUBRE',
        11: 'NOVIEMBRE',
        12: 'DICIEMBRE'
        }
    )

print(f"✅ Se cargaron {bpm_operativo_df.shape[0]} filas〰️ y {bpm_operativo_df.shape[1]} columnas🔼 de BPM's OPERATIVAS")

##### BPM's PERSONALES ######
bpm_personales_df = pd.DataFrame()
for sheet, cols in sheets_bpm.items():
    try:
        temp_df = pd.read_excel(
            workbook_bpm,
            sheet_name=sheet,
            usecols=cols,
            nrows=25,
            skiprows=23,
            header=1
        )
        bpm_personales_df = pd.concat([bpm_personales_df, temp_df], axis=1)
    except Exception as e:
        # print(f"✖️ La hoja {sheet} en {workbook_bpm.book if hasattr(workbook_bpm, 'book') else 'workbook'} no existe: {e}")
        pass

bpm_personales_df = bpm_personales_df.T
bpm_personales_df.columns = bpm_personales_df.iloc[0]
bpm_personales_df = bpm_personales_df.drop(bpm_personales_df.index[0])
bpm_personales_df.columns = bpm_personales_df.columns.str.strip().str.upper()
bpm_personales_df = bpm_personales_df.dropna(how='all', axis=1)
bpm_personales_df = bpm_personales_df.fillna(0)
bpm_personales_df.index = bpm_personales_df.index.rename('FECHA')
bpm_personales_df.index = pd.to_datetime(bpm_personales_df.index, errors='coerce')
bpm_personales_df['MES'] = bpm_personales_df.index.month

bpm_personales_df['MES'] = bpm_personales_df['MES'].map(
    {
        1: 'ENERO',
        2: 'FEBRERO',
        3: 'MARZO',
        4: 'ABRIL',
        5: 'MAYO',
        6: 'JUNIO',
        7: 'JULIO',
        8: 'AGOSTO',
        9: 'SEPTIEMBRE',
        10: 'OCTUBRE',
        11: 'NOVIEMBRE',
        12: 'DICIEMBRE'
        }
    )
bpm_personales_df = bpm_personales_df.dropna(subset=['MES'])
bpm_personales_df = bpm_personales_df.apply(pd.to_numeric, errors='coerce')
bpm_personales_df['PROMEDIOS DIARIOS'] = bpm_personales_df.drop(columns=['MES'], errors='ignore').mean(axis=1)
bpm_personales_df = bpm_personales_df[bpm_personales_df["PROMEDIOS DIARIOS"] != 0]

print(f"✅ Se cargaron {bpm_personales_df.shape[0]} filas〰️ y {bpm_personales_df.shape[1]} columnas🔼 de BPM's PERSONALES")
