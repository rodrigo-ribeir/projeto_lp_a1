import pandas as pd
import matplotlib.pyplot as plt

def normalize_value_columns(df: pd.DataFrame):
    '''
    Normaliza os valores de todas as colunas que não 
    houverem a palavra 'Date' no nome e que não sejam 
    colunas com valores em porcentagens. A normalização 
    é feita no próprio dataframe (inplace) dividindo 
    cada valor dessas colunas pelo seu máximo.

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe com as colunas a serem normalizadas
    '''
    # Gera uma lista com o nome de todas as colunas que não
    # contenham a palavra 'Date' ou '%' no nome ( visto que 
    # são dados já normalizados )
    columns = list(filter((lambda x: False if 'Date' in x or '%' in x else True), list(df.columns)))
    df[columns] = df[columns].apply(lambda x: x / x.max())

def rename_columns(df: pd.DataFrame, string):
    '''
    Função utilizada para adicionar uma palavra ao
    nome das colunas de um DataFrame que é realizada
    inplace, ou seja, altera o próprio DataFrame
    passado como parâmetro. Caso haja uma coluna com 
    a palavra `Date` no nome, ela não é renomeada.

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame com as colunas a serem renomeadas
    
    string: str
        Palavra a ser adicionada no nome das colunas
    '''
    # Função reutilizada para retirar colunas com palavra 'Date'
    column_names = list(filter((lambda x: False if 'Date' in x else True), list(df.columns)))
    # Cria um dicionário cujas chaves são os nomes atuais das
    # colunas e seus valores os nomes modificados
    new_names = {nome: nome + " " + string for nome in column_names}
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
            print(f'{period} isn\'t a valid period.')
            raise ValueError
    
    start_date = df.loc[0, 'Date']
    end_date = df.loc[0, 'Date'] + pd.Timedelta(days=dm)
    
    # Listas que serão adicionadas ao dataset contendo
    # o ínicio e o fim de cada intervalo
    s_dates = [start_date]
    e_dates = [end_date]

    total_data = df.shape[0]
    idx = 0
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

def ask_period() -> str:
    '''
    Função secundária para interação com o usuário
    acerca do período de agrupamento do dataset.

    Return
    ------
    str
        Retorna um caractere representando o tipo
        de período escolhido.
        
        Possíveis caracteres de retorno:
        - 'W';
        - 'M';
        - 'B';
        - 'T';
        - 'S';
        - 'Y'
    '''
    print("\n -> Por padrão, os dados são agrupados em meses.")
    period = 'M'
    ans = input(" -> Você deseja mudar o período? [Y/N]\n --> ")
    if (ans.lower() == 'y'):
        print(" -> Períodos:\n --> [W] Semanas; [M] Meses; [B] Bimestres; [T] Trimestres; [S] Semestres; [Y] Anos")
        ans = input(" --> Digite o período que você deseja:\n ---> ")
        if not(ans.upper() in ['W', 'M', 'B', 'T', 'S', 'Y']):
            print(" --> Período inválido.")
            raise ValueError
        else: 
            period = ans.upper()
    return period

def each_column_max(df: pd.DataFrame) -> dict:
    '''
    Função que retorna o valor máximo de cada coluna
    (com exceção de colunas com `Date` no nome) no
    formato de um dicionário.

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame contendo as colunas a serem analisadas

    Return
    ------
    dict
        Dicionário cujas chaves são os nomes das colunas
        analisadas e os valores são o maior valor daquela
        coluna
    '''
    def operate_columns(x: pd.Series, dicio: dict):
        if 'Date' in x.name:
            pass
        else:
            dicio[x.name] = x.max()
    result = dict()
    df.apply(lambda x: operate_columns(x, result))
    for key, value in list(result.items()):
        result[key] = f'{value:_.2f}'
    return result

def column_volume_times_value(df: pd.DataFrame):
    '''
    Função cria uma nova coluna no dataframe que
    contém o resultado da multiplicação do volume
    pelo preço de cada criptomoeda, gerando uma 
    visualização da relação do valor total em 
    circulação de cada criptomoeda naquele período

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame a ser adicionada a nova coluna.
        É importante notar que o DataFrame deve
        conter as colunas `Price` e `Vol.` de
        ambas criptomoedas e na mesma ordem.
    '''
    colunas = df.columns
    prices = list()
    volumes = list()
    names = list()
    for c in colunas:
        if ('Price' in c):
            prices.append(c)
            name = c.split(" ")[1]
            if not(name in names):
                names.append(name)
        if ('Vol.' in c):
            volumes.append(c)
            name = c.split(" ")[1]
            if not(name in names):
                names.append(name)

    if (len(prices) != len(volumes)) or (len(volumes) != len(names)):
        print("\n --> ERRO: Quantidades de cada coluna não correspondem.")
        print(" --> Há um número diferente de colunas 'Price' e 'Vol.'.\n")
        raise Exception

    if ((len(prices) == 0) or (len(volumes) == 0)):
        print("\n --> ERRO: Dataframe não contem as colunas necessárias para essa operação")
        print(" --> Colunas esperadas: \"Price\"; \"Vol.\"\n")
        raise Exception
    
    for idx in range(len(prices)):
        name = names[idx]
        df[f'Vol x Value ({name})'] = df[prices[idx]] * df[volumes[idx]]

def recent_data(df: pd.DataFrame, dias: int = 30) -> pd.DataFrame:
    '''
    Função criada para pegar o intervalo do número de
    dias passado como parâmetro mais recente.
    
    Parameters
    ----------
    df: pd.DataFrame
        O dataframe a ser coletado o intervalo de dias
    
    dias: int
        O número de dias anteriores ao último dado que
        devem ser inclusos na análise

    Return
    ------
    pd.Dataframe
        Retorna o dataframe no intervalo solicitado
    '''
    if not('Date' in list(df.columns)):
        print(" --> DataFrame deve conter a coluna 'Date'")
        raise Exception
    num_dias = df.shape[0]-1
    newest_date = df.loc[num_dias, 'Date']
    interval_start = newest_date - pd.Timedelta(days = dias)
    
    recent_df = df.loc[df['Date'] >= interval_start].reset_index(drop=True)
    return recent_df
