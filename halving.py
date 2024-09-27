import numpy as np
import pandas as pd
from matplotlib import pyplot as plot

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
            nao_eiste.append(col)
    
    if len(nao_existe)!=0: #checando se a lista nao_existe está vazia
        raise ValueError(f"Erro: As colunas {nao_existe} não estão no DataFrame.")
    
    colunas = ['Date', 'Price']
    dataframe = dataframe[colunas]
    return dataframe

df = filtrar_colunas(df, ['Date', 'Price'])


df['Date'] = pd.to_datetime(df['Date'])
df['Price'] = df['Price'].str.replace(',', '')
df['Price'] = pd.to_numeric(df['Price'])

print(df.isnull().sum()) # não há dados vazios.

#removendo linhas com datas duplicadas (se houver)
df['Date'] = df['Date'].drop_duplicates()
df = df.dropna()
#print(df)

#verificando se há datas faltando:
data_ini = df['Date'].min()
data_fim = df['Date'].max()
intervalo_datas = pd.date_range(data_ini, data_fim)
datas_faltando = intervalo_datas.difference(df['Date'])
if not datas_faltando.empty:
    print("Datas faltando:")
    print(datas_faltando)
else:
    print("Não há datas faltando")

#print(type(df['Date'][0]))
#df.set_index('Date', inplace=True)
#print(df)

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
#o banco de dados desponível para dowload vai ate 24/03/2024

def ordenando_indices(frame: pd.DataFrame):
    frame = frame.set_index('Date')
    frame = frame.sort_index()
    frame = frame.reset_index()
    return frame

halving_1 = ordenando_indices(halving_1)
halving_2 = ordenando_indices(halving_2)
halving_3 = ordenando_indices(halving_3)
print(halving_3)

halving_3.plot.line(x='Date', y='Price')
#plot.savefig("meuplot.png", dpi=300)

