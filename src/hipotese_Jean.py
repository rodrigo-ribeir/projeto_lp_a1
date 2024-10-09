import pandas as pd
import basics as bs
import analise_temporal as at
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

    df = at.agrupate_datasets(df1, df2, nome1, nome2)
    at.column_volume_times_value(df)
    recent_df = at.recent_data(df, 30)
    
    period = at.ask_period()
    
    # Agrupa os dados pelas datas no período determinado
    df = at.agrupate_dates(df, period)
    
    max_per_column = at.each_column_max(df)

    print("\n -> Lista dos maiores valores por coluna do dataframe:")
    for key, value in list(max_per_column.items()):
        print(f" --> Max em {"["+ key + "]":25s} = {value};")

    # Divide cada coluna não normalizada por seu máximo
    # para melhorar a visualização de cada dataset
    at.normalize_value_columns(df)

    return df, recent_df

if __name__ == "__main__":

    df, rdf = load_data()
    
    colunas_f = list(df.columns)
    prices = volumes = changes = value_volume = False
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
        if 'Vol x Value' in column and not(value_volume):
            value_volume = True
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
        
        if value_volume:        
            # Printa as colunas das variações
            change_columns = list(filter((lambda x: True if 'Vol x Value' in x else False), colunas_f))
            df.plot(x='Start Date', y=change_columns, kind='line', grid=True)
            plt.show()
    
    ans = input("\n -> Deseja a análise recente dos dados? [Y/N]\n --> ")
    try:
        ans = ans.upper()
    except:
        print(" --> Resposta não pode ser processada")
        raise ValueError
    if (ans == 'Y'):
        print("--> Análise recente dos dados:\n")
        mc = at.each_column_max(rdf)
        print("\n -> Lista dos maiores valores por coluna do dataframe:")
        for key, value in list(mc.items()):
            print(f" --> Max em {"["+ key + "]":25s} = {value};")
        if prices:
            # Printa as colunas dos preços
            price_columns = list(filter((lambda x: True if 'Price' in x else False), colunas_f))    
            rdf.plot(x='Date', y=price_columns, kind='line', grid=True)
            plt.show()

        if volumes:
            # Printa as colunas dos volumes
            vol_columns = list(filter((lambda x: True if 'Vol.' in x else False), colunas_f))
            rdf.plot(x='Date', y=vol_columns, kind='line', grid=True)
            plt.show()

        if changes:        
            # Printa as colunas das variações
            change_columns = list(filter((lambda x: True if 'Change %' in x else False), colunas_f))
            rdf.plot(x='Date', y=change_columns, kind='line', grid=True)
            plt.show()
        
        if value_volume:        
            # Printa as colunas das variações
            change_columns = list(filter((lambda x: True if 'Vol x Value' in x else False), colunas_f))
            rdf.plot(x='Date', y=change_columns, kind='line', grid=True)
            plt.show()

    print("\n -> Exiting...\n")