import pandas as pd
import re
import warnings
warnings.filterwarnings('ignore')

#####Control Documental - Estatus   Return df_documentos
def load_control_documental():
    df1 = []
    sheets = {
        'Dirección General (A)': 'I:M',
        'I+D (A)': 'I:M',
        'SGIA (A)': 'I:M',
        'GOP (A) ': 'I:M',
        'ACI (A) ': 'I:M',
        'Almacén (A)  ': 'I:M',
        'Mantenimiento (A)  ': 'I:M',
        'TIC (A) ': 'I:M',
        'Producción (A)': 'I:M',
        'GCH': 'I:M',
        'Mercadotécnia (A)': 'I:M',
        'SMO (A) ': 'I:M',
        'Seguridad Patrimonial (A) ': 'I:M',
        'Sanidad (A)': 'I:M',
        'Contabilidad (A)': 'I:M',
        'Fiscal (A)': 'I:M',
        'Costos (A)': 'I:M',
        'Tesorería (A)': 'I:M',
        'Cuentas por Cobrar (A)': 'I:M',
        'Ventas (A) ': 'I:M',
        'Seguridad e Higiene (A)': 'I:M',
        'Compras (A)': 'I:M',
        'Control Vehicular (A) ': 'I:M',
        'Gerencia de Administración (A)': 'I:M',
        'Área Jurídica (A)': 'I:M',
        'Cultura Organizacional (A) ': 'I:M'
    }
    # workbook="Excel/Control de actualización de vigencia por documento D.xlsm"
    with pd.ExcelFile(r"//192.168.10.2/Compartidos/SGI/Documentación/INDICADORES DE RECARGA/Control de actualización de vigencia por documento D.xlsm", engine="openpyxl") as workbook:
        for sheet_name, usecols in sheets.items():
            try:
                df = pd.read_excel(
                    workbook,
                    sheet_name=sheet_name,
                    usecols=usecols,
                    skiprows=2,
                    nrows=1
                )
                df['Departamento'] = sheet_name
                df1.append(df)
            except:
                print(f'Error en la hoja {sheet_name}.')
        workbook.close()
    
    df1 = pd.concat(df1)
    df1.rename(
        columns={x: x.replace('(A)', '').strip().capitalize() for x in df1.columns},
        inplace=True
    )
    df1['Total de Publicados'] = (df1['Publicados'].combine_first(df1['Publicado']).combine_first(df1['Listos para publicar']))
    df_documentos = df1[['Departamento', 'Total de Publicados', 'En flujo', 'Ausencia', 'Vigencia v.', 'Rechazados']].copy()
    df_documentos['Departamento'] = df_documentos['Departamento'].str.replace(r'\s*\(A\)\s*', '', regex=True).str.strip()
    df_documentos = df_documentos.fillna(0)  
    df_documentos.index = df_documentos['Departamento']
    df_documentos.index = df_documentos.index.str.strip(' ()')
    df_documentos = df_documentos.drop(columns='Departamento')
    df_documentos['Total'] = df_documentos.sum(axis=1)

    return df_documentos

###### TIF                          Return df
def load_tif():
    # workbook="Excel/Seguimiento TIF.xlsx"
    with pd.ExcelFile(r"//192.168.10.2/Compartidos/SGI/GAP/Seguimiento Indicador TIF/Seguimiento TIF.xlsx", engine="openpyxl") as workbook:
        df = pd.read_excel(
            workbook,
            skiprows=1
            )
        workbook.close()
        df.columns = df.columns.str.strip()
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
        df['Fecha Final'] = pd.to_datetime(df['Fecha Final'], errors='coerce')
        df['Fecha Vencimiento'] = pd.to_datetime(df['Fecha Vencimiento'], errors='coerce')
        df['Días transcurridos'] = (pd.Timestamp.today() - df['Fecha']).dt.days
        df['Días propuestos'] = (df['Fecha Vencimiento']-df['Fecha']).dt.days
        df['Días propuestos'] = df['Días propuestos'].fillna(0)
        df['Retraso'] = df['Días transcurridos'] - df['Días propuestos']
        df['Mes'] = df['Fecha'].dt.month
        df['Mes'] = df['Mes'].map(
            {
                1:'Enero',
                2:'Febrero',
                3:'Marzo',
                4:'Abril',
                5:'Mayo',
                6:'Junio',
                7:'Julio',
                8:'Agosto',
                9:'Septiembre',
                10:'Octubre',
                11:'Noviembre',
                12:'Diciembre'
                }
            )

        
        df1 = df
        df1 = df1.sort_values('Fecha', ascending=True)
        df1 = df1[df1['Estatus']!='CERRADA']
        df1 = df1.groupby('Departamento')['Estatus'].count()
        df1 = df1.reset_index().sort_values('Departamento')
        df1 = df1.rename(columns={'Estatus':'Abiertas'})
        df1.index = df1['Departamento']
        df1 = df1.drop(columns='Departamento')
        
        df2 = df
        df2 = df2.sort_values('Fecha', ascending=True)
        df2 = df2[df2['Estatus']=='Completado']
        df2 = df2.groupby('Departamento')['Estatus'].count()
        df2 = df2.reset_index().sort_values('Departamento')
        df2 = df2.rename(columns={'Estatus':'Cerradas'})
        df2.index = df2['Departamento']
        df2 = df2.drop(columns='Departamento')
            
        df3 = pd.concat([df1, df2], axis=1)
        df3['Eficiencia'] = ((df3['Abiertas'] / (df3['Abiertas']+df3['Cerradas']))*100).round(2)
        df3 = df3.fillna(0)
        
        return df

###### Acciones correctivas         Retrun df_ac
def load_ac():
    with pd.ExcelFile(r"C:/Users/daniel.santoyo/OneDrive - EMPACADORA DILUSA DE AGUASCALIENTES SA DE CV/EDA DSA/Auditorías/IndicadorAC1.xlsx", engine="openpyxl") as workbook:
        # sheets = ["SeguimientoAC-2023", "SeguimientoAC"]
    # for sheet in sheets:
        df = pd.read_excel(
            io = workbook,
            sheet_name = "SeguimientoAC",
            usecols='A:O',
            skiprows=10,
        )
        workbook.close()
        df.columns = df.columns.str.strip()
    df = df.drop(
        columns=[
            'Descripción de la no conformidad', 'Norma', 'Origen de desviación']
        )

    return df



