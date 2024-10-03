import pandas as pd
import basics as bs
import matplotlib.pyplot as plt

def agrupate_dates(df: pd.DataFrame, period: str = 'M') -> pd.DataFrame:
    '''
    Agrupa as datas em períodos de tempo pré-determinados

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame com os dados a serem agrupados

    period: str
        Informa qual será o período a ser agrupado, por
        padrão agrupa em meses
        Pode ser agrupado nos seguintes formatos:
        - 'W' -> Semanas
        - 'M' -> Meses
        - 'B' -> Bimestres
        - 'T' -> Trimestres
        - 'S' -> Semestres
        - 'Y' -> Anos

    Returns
    -------
    pd.DataFrame
        Retorna o dataframe agrupado no período especificado
    '''
    total_data = df.shape[0]
    dm = 0
    match period.upper():
        case 'W':
            dm = 7
        case 'M':
            dm = 30
        case 'B':
            dm = 60
        case 'T':
            dm = 90
        case 'S':
            dm = 180
        case 'Y':
            dm = 365
        case _:
            print(f'Not a valid period in {__name__}.')
            quit()
    start_date = df.loc[0, 'Date']
    end_date = df.loc[0, 'Date'] + pd.Timedelta(days=dm)
    idx = 0
    s_dates = [start_date]
    e_dates = [end_date]
    while idx < total_data:
        if (df.loc[idx, 'Date'] - end_date).days <= 0:
            df.loc[idx, 'Date'] = start_date
            idx += 1
        else:
            df.loc[idx, 'Date'] = end_date
            idx += 1
            start_date = end_date
            end_date += pd.Timedelta(days=dm)
            s_dates.append(start_date)
            e_dates.append(end_date)
    dfc = df.groupby('Date').mean()
    dfc['Start Date'] = s_dates
    dfc['End Date'] = e_dates
    return dfc

df = bs.choose_dataset()
colunas = ['Date', 'Price']
df = bs.filtrar_colunas(df, colunas)
df = bs.converter_dados(df)
print("Por padrão, os dados são agrupados em meses.")
period = 'M'
ans = input("Você deseja mudar o período? [Y/N]\n -> ")
if (ans.lower() == 'y'):
    print("Períodos:\n [W] Semanas; [M] Meses; [B] Bimestres; [T] Trimestres; [S] Semestres; [Y] Anos")
    ans = input("Digite o período que você deseja:\n -> ")
    if not(ans.upper() in ['W', 'M', 'B', 'T', 'S', 'Y']):
        print("Período inválido.")
        quit()
    else: period = ans

df = agrupate_dates(df, period)
df.plot(x='Start Date', y='Price', kind='line')
plt.show()
