import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def ler_arquivo(arquivo, separador=',', encoding='utf-8'):
    """
    Ler arquivo csv com pandas
    """
    
    try:
        dataframe = pd.read_csv(arquivo, sep=separador,encoding = encoding)
        return dataframe
    except FileNotFoundError:
        print(f'Arquivo {arquivo} não encontrado.')
    except pd.errors.EmptyDataError:
        print(f'Erro: O arquivo {arquivo} está vazio.\
            Certifique-se de que está no diretório correto')
    
df = ler_arquivo('bitcoin_historical_data.csv')
    

def filtrar_colunas(dataframe: pd.DataFrame, colunas: list):
    nao_existe = []
    for col in colunas:
        if not col in dataframe.columns:
            nao_existe.append(col)
    
    if len(nao_existe)!=0:
        raise ValueError(f"Erro: As colunas {nao_existe} não estão no DataFrame.")
    
    dataframe = dataframe[colunas]
    return dataframe

df = filtrar_colunas(df, ['Date', 'Price'])


def converter_dados(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Esta função realiza as seguintes operações no DataFrame:
    1. Converte a coluna 'Date' para o formato datetime.
    2. Remove as vírgulas da coluna 'Price' e converte os valores para números.
    """

    dataframe['Date'] = pd.to_datetime(dataframe['Date'])

    dataframe['Price'] = dataframe['Price'].str.replace(',', '', regex=True)
    dataframe['Price'] = pd.to_numeric(dataframe['Price'])
    
    return dataframe

df = converter_dados(df)

#verificando se há dados faltando:
def verificar_dados_faltando(dataframe: pd.DataFrame):
    
    # Verificar se todas as colunas têm zero valores nulos
    if not (dataframe.isnull().sum() == 0).all():
        raise ValueError("Há dados faltando em uma ou mais colunas.")
    
    return True

verificar_dados_faltando(df) # não há dados vazios.

#removendo linhas com datas duplicadas (se houver)
df['Date'] = df['Date'].drop_duplicates()
df = df.dropna()

def divisao_por_data(data1, data2):
    try:
        data1 = pd.to_datetime(data1)
        data2 = pd.to_datetime(data2)
    except TypeError:
        print("Os parâmetros de entrada da função deve ser datas")
    
    if(data1 > data2):
        raise ValueError("parâmetro 'data1' deve vir antes de 'data2' temporalmente")
    
    new_df = df[(data1 <= df['Date']) & (df['Date'] < data2)]
    return new_df

halving_1 = divisao_por_data("11/28/2012", "07/09/2016")
halving_2 = divisao_por_data("07/09/2016", "05/11/2020")
halving_3 = divisao_por_data("05/11/2020", "04/19/2024")
#o banco de dados desponível para download vai até 24/03/2024

def ordenando_indices(frame: pd.DataFrame):
    frame = frame.set_index('Date')
    frame = frame.sort_index()
    frame = frame.reset_index()
    return frame

halving_1 = ordenando_indices(halving_1)
halving_2 = ordenando_indices(halving_2)
halving_3 = ordenando_indices(halving_3)

def dias_apos_halving(dataframe: pd.DataFrame):
    """
    Esta função altera a coluna 'Date' para o período de tempo entre \
        a data da linha atual e a data inicial (primeira linha)"
    """
    data_inicial = dataframe['Date'].iloc[0]
    dataframe['Date'] = dataframe['Date'].apply(lambda d: (d - data_inicial).days)
    return dataframe

halving_1 = dias_apos_halving(halving_1)
halving_2 = dias_apos_halving(halving_2)
halving_3 = dias_apos_halving(halving_3)

def alterando_nome_e_indice(dataframe: pd.DataFrame):
    dataframe = dataframe.rename(columns={'Date': 'dias_apos_halving'})
    #dataframe = dataframe.set_index('dias_apos_halving')
    return dataframe

halving_1 = alterando_nome_e_indice(halving_1)
halving_2 = alterando_nome_e_indice(halving_2)
halving_3 = alterando_nome_e_indice(halving_3)


def aumento_percentual(dataframe: pd.DataFrame):
    valor_inicial = dataframe['Price'].iloc[0]
    dataframe['aumento_percentual'] = dataframe['Price'].apply(lambda x: (x/valor_inicial - 1)*100)
    return dataframe

halving_1 = aumento_percentual(halving_1)
halving_2 = aumento_percentual(halving_2)
halving_3 = aumento_percentual(halving_3)


def maior_serie(*series: pd.Series):
    maior_tamanho = 0
    serie_retorno = None
    for serie_atual in series:
        tamanho_atual = len(serie_atual)
        if(tamanho_atual > maior_tamanho):
            maior_tamanho = tamanho_atual
            serie_retorno = serie_atual
    return serie_retorno


mais_dias_apos_halving = maior_serie(halving_1['dias_apos_halving'],\
    halving_2['dias_apos_halving'], halving_3['dias_apos_halving'])

def adicionar_coluna(dataframe: pd.DataFrame, serie: pd.Series, nome: str) -> pd.DataFrame:
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
    """
    # Normalizando cada ciclo pelo valor máximo do respectivo ciclo
    dataframe['Ciclo 1 Normalizado'] = dataframe['Ciclo 1'] / dataframe['Ciclo 1'].max() * 100
    dataframe['Ciclo 2 Normalizado'] = dataframe['Ciclo 2'] / dataframe['Ciclo 2'].max() * 100
    dataframe['Ciclo 3 Normalizado'] = dataframe['Ciclo 3'] / dataframe['Ciclo 3'].max() * 100
    
    return dataframe

# Normalizando os ciclos
df_final = normalizar_ciclos_por_preco_maximo(df_final)


def indices_max_e_min(dataframe: pd.DataFrame):
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

plt.savefig("halving.png", dpi=300)
#plt.show()
