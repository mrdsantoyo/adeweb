import pandas as pd
import datetime as dt


with pd.ExcelFile(r"//192.168.10.2/Compartidos/Calidad Compartida (192.168.10.254)/5. KPI´s calidad/2025/Reporte de POES 2025 (ACTUAL).xlsx", engine='openpyxl') as workbook:

    df = pd.read_excel(
        workbook,
        sheet_name='%diario',
        usecols='A:NB',
        skiprows=6,
        nrows=30,
        header=0
    )
    workbook.close()

    fecha_inicio = dt.date(2025, 1, 1)
    num_dias = df.columns.size - 1

    date_labels = [
        (fecha_inicio + dt.timedelta(days=i)).strftime('%d/%m/%y') 
        for i in range(num_dias)
        ]

    df.columns = ["Área"] + date_labels
    df.reset_index(drop=True)
    df = df.T
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    df = df.apply(pd.to_numeric, errors='coerce')
    df.index = pd.to_datetime(df.index, format='%d/%m/%y')

