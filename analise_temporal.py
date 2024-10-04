import pandas as pd
import basics as bs
import matplotlib.pyplot as plt

def normalize_prices(df: pd.DataFrame):
    '''
    
    Normaliza os valores de todas as colunas que tiverem
    a palavra 'Price' no nome. A normalização é feita no
    próprio dataframe (inplace) dividindo cada valor dessas 
    colunas pelo seu máximo.

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe com as colunas a serem normalizadas
    
    '''
    columns = df.columns
    for column in columns:
        if 'Price' in str(column):
            df[column] = df[column] / df[column].max()

def rename_columns(df: pd.DataFrame, string):
    '''

    Função utilizada para adicionar uma palavra ao
    nome das colunas de um DataFrame que é realizada
    inplace, ou seja, altera o próprio DataFrame
    passado como parâmetro. Caso haja uma coluna com 
    nome `Date`, ela não é renomeada.

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame com as colunas a serem renomeadas
    
    string: str
        Palavra a ser adicionada no nome das colunas

    '''
    column_names = list(df.columns)
    new_names = dict()
    for name in column_names:
        if (name == 'Date'):
            continue
        else:
            new_names[name] = name + " " +  string
    df.rename(columns=new_names, inplace=True)

def agrupate_datasets(df1: pd.DataFrame, df2: pd.DataFrame, df1_name: str = 1, df2_name: str = 2) -> pd.DataFrame:
    '''

    Função utilizada para juntar dois datasets diferentes.
    A junção é feita com base na coluna 'Date' dos datasets.

    Parameters
    ----------
    df1: pd.Dataframe
        DataFrame a ser mesclado

    df2: pd.Dataframe
        Dataframe a ser mesclado
    
    df1_name: str
        Nome do primeiro DataFrame para personalização das 
        colunas no DataFrame agrupado. O padrão é 1.
    
    df2_name: str
        Nome do segundo DataFrame para personalização das 
        colunas no DataFrame agrupado. O padrão é 2.

    Returns
    -------
    df.DataFrame
        DataFrame final com a mesclagem dos DataFrames 
        passados como parâmetros com base nas datas dos
        DataFrames. Caso um DataFrame não contenha o valor
        nas mesmas datas que o outro, as colunas são 
        preenchidas com 0.

    '''
    
    rename_columns(df1, df1_name)
    rename_columns(df2, df2_name)

    df_result = pd.merge(df1, df2, on='Date', how='outer')
    
    df_result.fillna(0, inplace=True)

    return df_result

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

# Para não rodar o script sem ser o principal
if __name__ == "__main__":
    # Colunas trabalhadas
    colunas = ['Date', 'Price']
    df1, nome1 = bs.choose_dataset(2, True)
    df1 = bs.filtrar_colunas(df1, colunas)
    df1 = bs.converter_dados(df1)
    df2, nome2 = bs.choose_dataset(3, True)
    df2 = bs.filtrar_colunas(df2, colunas)
    df2 = bs.converter_dados(df2)

    final_df = agrupate_datasets(df1, df2, nome1, nome2)


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

    # Agrupa os dados pelas datas no período determinado
    final_df = agrupate_dates(final_df, period)

    # Divide cada coluna de preço por seu máximo para ver o maior período de crescimento
    # final_df = 
    normalize_prices(final_df)

    # Verifica quais colunas serão plotadas no gráfico
    price_columns = list()
    for column in list(final_df.columns):
        if 'Price' in str(column):
            price_columns.append(column)

    final_df.plot(x='Start Date', y=price_columns, kind='line')
    plt.show()
    