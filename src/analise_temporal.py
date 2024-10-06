import pandas as pd
import basics as bs
import matplotlib.pyplot as plt

def load_data() -> pd.DataFrame:
    '''
    Carrega os dados para funcionamento da função
    quando executada diretamente e formata usando
    as funções do arquivo de códigos basics.py, além
    de realizar as operações de groupby pelo período
    e normalização dos dados.
    
    Return
    ------
    pd.DataFrame
        Retorna o dataset final agrupado e formatado
    '''
    colunas = ['Date', 'Price', 'Vol.', 'Change %']
    df1, nome1 = bs.choose_dataset(2, True)
    df1 = bs.filtrar_colunas(df1, colunas)
    df1 = bs.converter_dados(df1)
    df2, nome2 = bs.choose_dataset(3, True)
    df2 = bs.filtrar_colunas(df2, colunas)
    df2 = bs.converter_dados(df2)
    print(f" -> Os datasets trabalhados são: \n --> {nome1}\n --> {nome2}")
    print("\n -> As colunas analisadas são:")
    for item in colunas:
        print(f" --> {item}")

    df = agrupate_datasets(df1, df2, nome1, nome2)

    period = ask_period()

    # Agrupa os dados pelas datas no período determinado
    df = agrupate_dates(df, period)
    # Divide cada coluna não normalizada por seu máximo
    # para melhorar a visualização de cada dataset
    normalize_value_columns(df)

    return df

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

if __name__ == "__main__":

    df = load_data()
    
    colunas_f = list(df.columns)
    prices = volumes = changes = False
    for column in colunas_f:
        if 'Price' in column and not(prices):
            prices = True
            continue
        if 'Vol.' in column and not(volumes):
            volumes = True
            continue
        if 'Change %' in column and not(changes):
            changes = True
            continue

    
            
    # Verificação e plot das colunas presentes no dataset
    ans = input("\n -> Deseja imprimir os gráficos? [Y/N]\n --> ")
    try:
        ans = ans.upper()
    except:
        print(" --> Resposta não pode ser processada")
        raise ValueError
    if (ans == 'Y'): 
        if prices:
            # Printa as colunas dos preços
            price_columns = list(filter((lambda x: True if 'Price' in x else False), colunas_f))    
            df.plot(x='Start Date', y=price_columns, kind='line', grid=True)
            plt.show()

        if volumes:
            # Printa as colunas dos volumes
            vol_columns = list(filter((lambda x: True if 'Vol.' in x else False), colunas_f))
            df.plot(x='Start Date', y=vol_columns, kind='line', grid=True)
            plt.show()

        if changes:        
            # Printa as colunas das variações
            change_columns = list(filter((lambda x: True if 'Change %' in x else False), colunas_f))
            df.plot(x='Start Date', y=change_columns, kind='line', grid=True)
            plt.show()
    
    print("\n -> Exiting...\n")