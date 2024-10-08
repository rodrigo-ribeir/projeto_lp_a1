import pandas as pd
import basics as bs
import analise_temporal as at
import matplotlib.pyplot as plt

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

def graph_compare_prices(df: pd.DataFrame, crypto_compare: str, cor: str):
    '''
    Salva os gráficos que comparam os preços do Bitcoin com os de outra 
    criptomoeda.

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
    '''
    fig, eixo1 = plt.subplots(figsize=(10, 5))
    df_bitcoin.plot.line(x='Date', y='Price', ax=eixo1, label='Bitcoin', color='blue')
    eixo1.set_ylabel('Preço Bitcoin')

    eixo2 = eixo1.twinx()
    df.plot.line(x='Date', y='Price', ax=eixo2, label=crypto_compare, color=cor)
    eixo2.set_ylabel(f'Preço {crypto_compare}')
    
    plt.savefig(f"../data/imagens/bitcoin_x_{crypto_compare.lower()}.png", format='png', dpi=300)

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

def load_format_dataset(idx: int, columns: list) -> pd.DataFrame:
    '''
    Função básica para carregar os datasets utilizados na hipótese.

    Parameters
    ----------
    idx: int
        Inteiro que indica o dataset que será aberto com base na função 
        choose_dataset (1: Bitcoin; 2: Ethereum; 3: Solana)

    columns: list
        Lista contendo as colunas que serão utilizadas

    Return
    ------
    pd.DataFrame
        Dataframe formatado e filtrado com as colunas que serão utilizadas
    '''
    df, name = bs.choose_dataset(idx, True)
    df = bs.filtrar_colunas(df, columns)
    df = bs.converter_dados(df)
    return df, name

if __name__ == "__main__":
    
    columns = ['Date', 'Price', 'Change %']

    df_bitcoin, name_b = load_format_dataset(1, columns)
    df_ethereum, name_e = load_format_dataset(2, columns)
    df_solana, name_s = load_format_dataset(3, columns)

    df_bitcoin, df_solana, df_ethereum = remove_lines_diff(df_bitcoin, df_solana, df_ethereum)

    # Gera as imagens dos gráficos que são armazenadas em ../data/imagens
    graph_compare_prices(df_solana, 'Solana', 'orange')
    graph_compare_prices(df_ethereum, 'Ethereum', 'green')

    # Gera dataframes utilizados na pasta ../data/dataframes
    with open('../data/dataframes/bitcoin_values.md', "w", encoding='utf-8') as archive:
        df_bitcoin.tail(5).to_markdown(archive, index=False)
    
    with open('../data/dataframes/ethereum_values.md', "w", encoding='utf-8') as archive:
        df_ethereum.tail(5).to_markdown(archive, index=False)
    
    with open('../data/dataframes/solana_values.md', "w", encoding='utf-8') as archive:
        df_solana.tail(5).to_markdown(archive, index=False)
    
    df_agrupate1 = at.agrupate_datasets(df_bitcoin.copy(), df_solana, "btc", "sol")
    df_agrupate2 = at.agrupate_datasets(df_bitcoin, df_ethereum, "btc", "eth")
    
    with open('../data/dataframes/bitcoin_x_solana.md', "w", encoding='utf-8') as archive:
        df_agrupate1.tail(5).to_markdown(archive, index=False)

    with open('../data/dataframes/bitcoin_x_ethereum.md', "w", encoding='utf-8') as archive:
        df_agrupate2.tail(5).to_markdown(archive, index=False)

    T_s, F_s = qtd_same_sign(df_agrupate1, ['Change % btc', 'Change % sol'])
    print(f"Mesmas mudanças: {T_s}, Mudanças opostas: {F_s}")
    T_e, F_e = qtd_same_sign(df_agrupate2, ['Change % btc', 'Change % eth'])
    print(f"Mesmas mudanças: {T_e}, Mudanças opostas: {F_e}")