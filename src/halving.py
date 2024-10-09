import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def ler_arquivo(arquivo, separador=',', encoding='utf-8'):
    """
    Ler arquivo CSV com pandas.

    Parameters
    ----------
    arquivo : str
        O caminho do arquivo CSV que vai ser lido.
    separador : str, optional
        O separador do arquivo (padrão é ',').
    encoding : str, optional
        Como o arquivo vai ser codificado (o padrão é 'utf-8').

    Returns
    -------
    pd.DataFrame
        DataFrame contendo os dados do arquivo CSV.

    Raises
    ------
    FileNotFoundError
        Se o arquivo não existir ou não for encontrado.
    pd.errors.EmptyDataError
        Caso o arquivo estiver vazio.

    Examples
    --------
    >>> df = ler_arquivo('dados.csv')
    >>> df.head()
    """
    
    try:
        dataframe = pd.read_csv(arquivo, sep=separador, encoding=encoding)
        return dataframe
    except FileNotFoundError:
        print(f'Arquivo {arquivo} não encontrado.')
    except pd.errors.EmptyDataError:
        print(f'Erro: O arquivo {arquivo} está vazio. Certifique-se de que está no diretório correto')
    
df = ler_arquivo('./data/Bitcoin Historical Data.csv')

def filtrar_colunas(dataframe: pd.DataFrame, colunas: list):
    """
    Filtra colunas do DataFrame.

    Parameters
    ----------
    dataframe : pd.DataFrame
        O DataFrame para ser filtrado.
    colunas : list
        Lista de nomes de colunas para serem mantidas.

    Returns
    -------
    pd.DataFrame
        DataFrame com apenas as colunas passadas no parâmetro.

    Raises
    ------
    ValueError
        Se alguma das colunas passadas no parâmetro não estiver presente no DataFrame.

    Examples
    --------
    >>> df_filtrado = filtrar_colunas(df, ['Date', 'Price'])
    >>> df_filtrado.head()
    """
    
    nao_existe = []
    for col in colunas:
        if not col in dataframe.columns:
            nao_existe.append(col)
    
    if len(nao_existe) != 0:
        raise ValueError(f"Erro: As colunas {nao_existe} não estão no DataFrame.")
    
    dataframe = dataframe[colunas]
    return dataframe

df = filtrar_colunas(df, ['Date', 'Price'])

def converter_dados(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Converte os dados do DataFrame.

    1. Converte a coluna 'Date' para o formato de datetime.
    2. Remove as vírgulas da coluna 'Price' e converte os valores para números.

    Parameters
    ----------
    dataframe : pd.DataFrame
        O DataFrame a ser convertido.

    Returns
    -------
    pd.DataFrame
        DataFrame com as colunas convertidas.

    Examples
    --------
    >>> df_convertido = converter_dados(df)
    >>> df_convertido.dtypes['Date'] == 'datetime64[ns]'
    True
    """
    
    dataframe['Date'] = pd.to_datetime(dataframe['Date'])
    dataframe['Price'] = dataframe['Price'].str.replace(',', '', regex=True)
    dataframe['Price'] = pd.to_numeric(dataframe['Price'])
    
    return dataframe

df = converter_dados(df)

def verificar_dados_faltando(dataframe: pd.DataFrame):
    """
    Verifica se há dados faltando no DataFrame.

    Parameters
    ----------
    dataframe : pd.DataFrame
        O DataFrame a ser verificado.

    Returns
    -------
    bool
        True se não houver dados faltando, False caso contrário.

    Raises
    ------
    ValueError
        Se houver dados faltando em alguma coluna.

    Examples
    --------
    >>> verificar_dados_faltando(df)
    True
    """
    
    if not (dataframe.isnull().sum() == 0).all():
        raise ValueError("Há dados faltando em uma ou mais colunas.")
    
    return True

verificar_dados_faltando(df)

# Removendo linhas com datas duplicadas (se houver)
df['Date'] = df['Date'].drop_duplicates()
df = df.dropna()

def divisao_por_data(data1, data2):
    """
    Filtra o DataFrame com base em um intervalo de datas.

    Parameters
    ----------
    data1 : str
        A data inicial do intervalo.
    data2 : str
        A data final do intervalo.

    Returns
    -------
    pd.DataFrame
        DataFrame filtrado contendo apenas os dados entre as datas especificadas.

    Raises
    ------
    ValueError
        Se 'data1' é maior que 'data2'.

    Examples
    --------
    >>> df_filtrado = divisao_por_data("01/01/2020", "01/01/2021")
    >>> df_filtrado.head()
    """
    
    try:
        data1 = pd.to_datetime(data1)
        data2 = pd.to_datetime(data2)
    except TypeError:
        print("Os parâmetros de entrada da função devem ser datas")
    
    if data1 > data2:
        raise ValueError("parâmetro 'data1' deve vir antes de 'data2' temporalmente")
    
    new_df = df[(data1 <= df['Date']) & (df['Date'] < data2)]
    return new_df

halving_1 = divisao_por_data("11/28/2012", "07/09/2016")
halving_2 = divisao_por_data("07/09/2016", "05/11/2020")
halving_3 = divisao_por_data("05/11/2020", "04/19/2024")

def ordenando_indices(frame: pd.DataFrame):
    """
    Ordena o DataFrame com base na coluna 'Date'.

    Parameters
    ----------
    frame : pd.DataFrame
        O DataFrame a ser ordenado.

    Returns
    -------
    pd.DataFrame
        DataFrame ordenado pelo índice da data.

    Examples
    --------
    >>> frame_ordenado = ordenando_indices(halving_1)
    >>> frame_ordenado.head()
    """
    
    frame = frame.set_index('Date')
    frame = frame.sort_index()
    frame = frame.reset_index()
    return frame

halving_1 = ordenando_indices(halving_1)
halving_2 = ordenando_indices(halving_2)
halving_3 = ordenando_indices(halving_3)

def dias_apos_halving(dataframe: pd.DataFrame):
    """
    Altera a coluna 'Date' para o número de dias após o halving.

    Parameters
    ----------
    dataframe : pd.DataFrame
        O DataFrame contendo os dados do halving.

    Returns
    -------
    pd.DataFrame
        DataFrame com a coluna 'Date' alterada para dias após o halving.

    Examples
    --------
    >>> df_dias = dias_apos_halving(halving_1)
    >>> df_dias['dias_apos_halving'].head()
    """
    
    data_inicial = dataframe['Date'].iloc[0]
    dataframe['Date'] = dataframe['Date'].apply(lambda d: (d - data_inicial).days)
    return dataframe

halving_1 = dias_apos_halving(halving_1)
halving_2 = dias_apos_halving(halving_2)
halving_3 = dias_apos_halving(halving_3)

def alterando_nome_e_indice(dataframe: pd.DataFrame):
    """
    Altera o nome da coluna 'Date' para 'dias_apos_halving'.

    Parameters
    ----------
    dataframe : pd.DataFrame
        O DataFrame cujas colunas serão renomeadas.

    Returns
    -------
    pd.DataFrame
        DataFrame com a coluna renomeada.

    Examples
    --------
    >>> df_alterado = alterando_nome_e_indice(halving_1)
    >>> df_alterado.columns
    Index(['dias_apos_halving', 'Price', 'aumento_percentual'], dtype='object')
    """
    
    dataframe = dataframe.rename(columns={'Date': 'dias_apos_halving'})
    return dataframe

halving_1 = alterando_nome_e_indice(halving_1)
halving_2 = alterando_nome_e_indice(halving_2)
halving_3 = alterando_nome_e_indice(halving_3)

def aumento_percentual(dataframe: pd.DataFrame):
    """
    Calcula o aumento percentual em relação ao preço inicial.

    Parameters
    ----------
    dataframe : pd.DataFrame
        O DataFrame contendo os preços.

    Returns
    -------
    pd.DataFrame
        DataFrame com uma nova coluna 'aumento_percentual'.

    Examples
    --------
    >>> df_aumento = aumento_percentual(halving_1)
    >>> df_aumento['aumento_percentual'].head()
    """
    
    valor_inicial = dataframe['Price'].iloc[0]
    dataframe['aumento_percentual'] = dataframe['Price'].apply(lambda x: (x/valor_inicial - 1)*100)
    return dataframe

halving_1 = aumento_percentual(halving_1)
halving_2 = aumento_percentual(halving_2)
halving_3 = aumento_percentual(halving_3)

def maior_serie(*series: pd.Series):
    """
    Retorna a maior série dentre as séries fornecidas.

    Parameters
    ----------
    *series : pd.Series
        As séries a serem comparadas.

    Returns
    -------
    pd.Series
        A maior série com base no número de elementos.

    Examples
    --------
    >>> maior = maior_serie(halving_1['dias_apos_halving'], halving_2['dias_apos_halving'])
    >>> len(maior)
    122  # Exemplo, dependendo do tamanho das séries
    """
    maior_tamanho = 0
    serie_retorno = None
    for serie_atual in series:
        tamanho_atual = len(serie_atual)
        if tamanho_atual > maior_tamanho:
            maior_tamanho = tamanho_atual
            serie_retorno = serie_atual
    return serie_retorno

mais_dias_apos_halving = maior_serie(
    halving_1['dias_apos_halving'],
    halving_2['dias_apos_halving'],
    halving_3['dias_apos_halving']
)

def adicionar_coluna(dataframe: pd.DataFrame, serie: pd.Series, nome: str) -> pd.DataFrame:
    """
    Adiciona uma nova coluna ao DataFrame.

    Parameters
    ----------
    dataframe : pd.DataFrame
        O DataFrame ao qual a coluna será adicionada.
    serie : pd.Series
        A série que será adicionada como coluna.
    nome : str
        O nome da nova coluna.

    Returns
    -------
    pd.DataFrame
        O DataFrame com a nova coluna adicionada.

    Examples
    --------
    >>> df = pd.DataFrame()
    >>> df = adicionar_coluna(df, pd.Series([1, 2, 3]), 'Nova Coluna')
    >>> df
       Nova Coluna
    0            1
    1            2
    2            3
    """
    dataframe[nome] = serie
    return dataframe

df_final = pd.DataFrame()
adicionar_coluna(df_final, mais_dias_apos_halving, 'Dias após halving')
adicionar_coluna(df_final, halving_1['aumento_percentual'], 'Ciclo 1')
adicionar_coluna(df_final, halving_2['aumento_percentual'], 'Ciclo 2')
adicionar_coluna(df_final, halving_3['aumento_percentual'], 'Ciclo 3')

def normalizar_ciclos_por_preco_maximo(dataframe: pd.DataFrame):
    """
    Normaliza os ciclos no DataFrame com base no preço máximo de cada ciclo.
    
    A normalização é feita dividindo os valores de 'Ciclo 1', 'Ciclo 2' e 'Ciclo 3'
    pelo preço máximo correspondente de cada ciclo.

    Parameters
    ----------
    dataframe : pd.DataFrame
        O DataFrame contendo os ciclos a serem normalizados.

    Returns
    -------
    pd.DataFrame
        O DataFrame com os ciclos normalizados.

    Examples
    --------
    >>> df = pd.DataFrame({'Ciclo 1': [100, 200, 300], 'Ciclo 2': [150, 250, 350]})
    >>> df_normalizado = normalizar_ciclos_por_preco_maximo(df)
    >>> df_normalizado
       Ciclo 1  Ciclo 2  Ciclo 1 Normalizado  Ciclo 2 Normalizado
    0      100      150                  33.33                 42.86
    1      200      250                 66.67                 71.43
    2      300      350                 100.00                100.00
    """
    # Normalizando cada ciclo pelo valor máximo do respectivo ciclo
    dataframe['Ciclo 1 Normalizado'] = dataframe['Ciclo 1'] / dataframe['Ciclo 1'].max() * 100
    dataframe['Ciclo 2 Normalizado'] = dataframe['Ciclo 2'] / dataframe['Ciclo 2'].max() * 100
    dataframe['Ciclo 3 Normalizado'] = dataframe['Ciclo 3'] / dataframe['Ciclo 3'].max() * 100
    
    return dataframe

# Normalizando os ciclos
df_final = normalizar_ciclos_por_preco_maximo(df_final)

def indices_max_e_min(dataframe: pd.DataFrame):
    """
    Retorna os índices do máximo e mínimo na coluna 'Price'.

    Parameters
    ----------
    dataframe : pd.DataFrame
        O DataFrame que contém a coluna 'Price'.

    Returns
    -------
    tuple
        Os índices do máximo e do mínimo na coluna 'Price'.

    Examples
    --------
    >>> indices_max_min = indices_max_e_min(df_final)
    >>> indices_max_min
    (2, 0)  # Exemplo, dependendo dos dados
    """
    indice_maximo = dataframe['Price'].idxmax()
    indice_minimo = dataframe['Price'].idxmin()
    return indice_maximo, indice_minimo

indice_maximo_1, indice_minimo_1 = indices_max_e_min(halving_1)
indice_maximo_2, indice_minimo_2 = indices_max_e_min(halving_2)
indice_maximo_3, indice_minimo_3 = indices_max_e_min(halving_3)

# Plote as colunas normalizadas
df_final.plot.line(x='Dias após halving', y=['Ciclo 1 Normalizado', 'Ciclo 2 Normalizado', 'Ciclo 3 Normalizado'])
plt.title('Aumento Percentual Normalizado Após Halving')
plt.ylabel('Aumento Percentual Normalizado (%)')
plt.xlabel('Dias Após Halving')
plt.grid()

# Obtenha os dias correspondentes aos índices máximos
dias_maximos_1 = halving_1['dias_apos_halving'].iloc[indice_maximo_1]
dias_maximos_2 = halving_2['dias_apos_halving'].iloc[indice_maximo_2]
dias_maximos_3 = halving_3['dias_apos_halving'].iloc[indice_maximo_3]

# Adicione linhas verticais nos pontos de preço máximo
plt.axvline(x=dias_maximos_1, color='red', linestyle='--', label='Máx Ciclo 1')
plt.axvline(x=dias_maximos_2, color='green', linestyle='--', label='Máx Ciclo 2')
plt.axvline(x=dias_maximos_3, color='blue', linestyle='--', label='Máx Ciclo 3')

plt.legend()
plt.savefig("halving.png", dpi=300)
#plt.show()
