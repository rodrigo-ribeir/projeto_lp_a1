import pandas as pd
import basics as bs
import analise_temporal as at
import matplotlib.pyplot as plt

df_bitcoin, name_b = bs.choose_dataset(1, True)
df_ethereum, name_e = bs.choose_dataset(2, True)
df_solana, name_s = bs.choose_dataset(3, True)

columns = ['Date', 'Price', 'Change %']

df_bitcoin = bs.filtrar_colunas(df_bitcoin, columns)
df_solana = bs.filtrar_colunas(df_solana, columns)
df_ethereum = bs.filtrar_colunas(df_ethereum, columns)

df_bitcoin = bs.converter_dados(df_bitcoin)
df_solana = bs.converter_dados(df_solana)
df_ethereum = bs.converter_dados(df_ethereum)

def remove_lines_diff(df1: pd.DataFrame, df2: pd.DataFrame, df3: pd.DataFrame, column: str = 'Date'):
    '''
    Remove as linhas que estão na coluna de um DataFrame, mas não estão
    na coluna do outro

    Parameters
    ----------
    df1, df2, df3: pd.DataFrame
        DataFrames que serão comparados e modificados

    column: str
        Coluna que está presente nos dois DataFrames e será observada

    Returns
    -------
    dfr1, dfr2, dfr3
        Retorna novos DataFrames somente com linhas iguais
    '''
    dates_bool = df1[column].isin(df2[column])
    dates = (df1[column])[dates_bool]
    dfr1 = df1[df1[column].isin(dates)]
    dfr2 = df2[df2[column].isin(dates)]
    dfr3 = df3[df3[column].isin(dates)]
    return dfr1, dfr2, dfr3

df_bitcoin, df_solana, df_ethereum = remove_lines_diff(df_bitcoin, df_solana, df_ethereum)

def graph_compare_prices(df: pd.DataFrame, crypto_compare: str, cor: str):
    '''
    Plota o gráfico para comparar os preços do Bitcoin com os de outra criptomoeda.

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame com os dados da criptomoeda que será comparada

    crypto_compare: str
        O nome da cripomoeda que será utilizada, sendo ela uma das seguintes:
        - 'Solana'
        - 'Ethereum'

    cor: str
        Cor para a linha da criptomoeda escolhida

    Returns
    -------
    fig
    Retorna o gráfico com as duas criptomoedas, sendo um eixo fixo 'Date'
    e outros eixos para os preços de cada criptomoeda
    (Bitcoin e 'crypto_compare'), para compará-las
    '''
    fig, eixo1 = plt.subplots(figsize=(10, 5))
    df_bitcoin.plot.line(x='Date', y='Price', ax=eixo1, label='Bitcoin', color='blue')
    eixo1.set_ylabel('Preço Bitcoin')

    eixo2 = eixo1.twinx()
    df.plot.line(x='Date', y='Price', ax=eixo2, label=crypto_compare, color=cor)
    eixo2.set_ylabel(f'Preço {crypto_compare}')

    plt.xticks(rotation=45)

    fig.canvas.draw_idle()
    plt.matshow(fig)


fig1 = graph_compare_prices(df_solana, 'Solana', 'orange')
#plt.show()
fig2 = graph_compare_prices(df_ethereum, 'Ethereum', 'green')

df_agrupate1 = at.agrupate_datasets(df_bitcoin, df_solana, "btc", "sol")
df_agrupate2 = at.agrupate_datasets(df_bitcoin, df_ethereum, "btc", "eth")

def qtd_same_sign(df: pd.DataFrame, columns: list):
    '''
    Verifica cada linha de duas colunas (que possuam valores inteiros) para saber 
    se aumentam/diminuem juntas com mais frequência ou não

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame que já está agrupado

    columns: list
        Lista de colunas que serão comparadas

    Returns
    -------
    true_count
        Quantidade de vezes que os valores aumentaram/diminuíram juntos

    false_count
        Quantidade de vezes que, de um dia para o outro, um valor aumentou e o outro diminuiu
    '''
    print(df[columns])
    df['Bool Hipótese'] = ((df[columns[0]] >= 0) & (df[columns[1]] >= 0)) | ((df[columns[0]] <= 0) & (df[columns[1]] <= 0))
    true_count = df['Bool Hipótese'].value_counts()[True]
    false_count = df['Bool Hipótese'].value_counts()[False]
    return true_count, false_count

#column = ["Change % btc", "Change % sol"]

#t, f = qtd_same_sign(df_agrupate1, column)

#print(f"True: {t}, False: {f}")