import pandas as pd

def read_data(name: str, separator: str = ',', encode: str = "utf-8") -> pd.DataFrame:
    '''
    Função utilizada para ler um arquivo .csv que se encontra
    dentro da pasta "data"

    Parameters
    ----------
    name: str
        String contendo o nome do arquivo (com a extensão de 
        tipo '.csv') a ser carregado
    
    separator: str
        Parâmetro opcional que pode ser passado caso o arquivo 
        csv apresente separadores diferentes do padrão (',')
    
    encode: str
        Parâmetro opcional que pode ser passado caso o arquivo 
        esteja em uma codifição diferente da padrão ('utf-8')

    Return
    ------
    pd.DataFrame
        Retorna um DataFrame contendo o conteúdo do arquivo
        passado como parâmetro
    '''
    archive = "..\\data\\" + name
    try:
        df = pd.read_csv(archive, sep=separator, encoding= encode)
    except FileNotFoundError:
        print(f"O arquivo {name} não foi encontrado na pasta data.")
        quit()
    except Exception as erro:
        print(f"Não foi possível abrir o arquivo {name}. Verifique o conteúdo do arquivo.")
        print(f"Erro: {erro}")
        quit()
    else:
        return df
    
def choose_dataset(select: int = 0, return_name: bool = False) -> pd.DataFrame | str:
    '''
    Função para facilitar a abertura dos diferentes arquivos 
    utilizados no decorrer do trabalho

    Parameters
    ----------
    select: int
        Parâmetro que, se não for passado, gera um input dentro
        da função solicitando um valor. Refere-se a qual dataset 
        será aberto.
        As opções estão listadas abaixo:
        - 1: Bitcoin Historical Data.csv
        - 2: Ethereum Historical Data.csv
        - 3: Solana Historical Data.csv
        - 4: ( Outro: gera um input solicitando o nome )

    return_name: bool
        Se passado como true retorna também o nome do dataset
        carregado. O padrão é False

    Returns
    -------
    pd.DataFrame
        Retorna um dataframe contendo o conteúdo de um arquivo
        selecionado na pasta "data"

    str
        Retorna o nome do dataset caso o parâmetro `return_name`
        seja passado como True
    '''
    
    if (select == 0):
        print("Selecione o índice de qual dos três datasets você deseja abrir")
        ans = input("{ 1 - Bitcoin // 2 - Ethereum // 3 - Solana // 4 - Outro}\n-> ")
        try:
            select = int(ans)
        except TypeError:
            print("Você deve digitar um número de 1 a 4.")

    df = None
    data_name = ""
    match select:
        case 1:
            df = read_data("Bitcoin Historical Data.csv")
            data_name = "Bitcoin"
        case 2:
            df = read_data("Ethereum Historical Data.csv")
            data_name = "Ethereum"
        case 3:
            df = read_data("Solana Historical Data.csv")
            data_name = "Solana"
        case 4:
            name = input("Digite o nome do arquivo sem a extensão (.csv):\n ->") + ".csv"
            df = read_data(name)
            data_name = name[0:-4]
        case _:
            print("Digite uma opção válida --> {1, 2, 3 ou 4}.")
    if return_name:
        return df, data_name
    return df

def filtrar_colunas(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    '''
    Função utilizada para filtrar as colunas desejadas do
    dataframe.

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe contendo o conteúdo a ser filtrado pelas
        colunas;

    columns: list[str]
        Lista no formato ["Coluna 1", "Coluna 2", ...] contendo
        o nome das colunas que devem ser mantidas no dataframe.

    Return
    ------
    pd.DataFrame
        Retorna o dataframe somente com as colunas passadas como
        parâmetro
    
    '''
    not_in = []
    for col in columns:
        if not col in df.columns:
            not_in.append(col)
    
    if len(not_in)!=0:
        raise ValueError(f"Erro: As colunas {not_in} não estão no DataFrame.")
    
    df = df[columns]
    return df

def converter_dados(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Função que formata as diferentes colunas contidas no
    dataframe utilizado como padrão.
    
    Dados
    -----
    A função formata as seguintes colunas se presentes
    no dataframe passado
       - `Date`; `Price`; `High`; `Low`; `Vol.`; `Change %`

    Formatações
    -----------
    - `Date`:
        - Transforma a string em um objeto datetime do pandas

    - `Open` / `Price` / `High` / `Low`:
        - Remove as vírgulas e converte os valores para números.
    - `Vol.`:
        - Células vazias são preenchidas com 0 e transforma os
        valores em números (Substituindo 'K' por uma multiplicação em 
        ordem {10^3}, 'M' por uma multiplicação em ordem {10^6} e 'B'
        por uma multiplicação em ordem de {10^9})
    - `Change`:
        - Remove o símbolo de porcentagem e transforma os
        valores em sua representação decimal entre 0 e 1 
        (mantendo o sinal).
    '''
    def format_vol(celula: str):
        if (pd.isna(celula)):
            celula = 0
        elif ('K' in str(celula)):
            celula = celula.replace('K', '')
            celula = pd.to_numeric(celula) * pow(10,3)
        elif ('M' in str(celula)):
            celula = celula.replace('M', '')
            celula = pd.to_numeric(celula) * pow(10,6)
        elif ('B' in str(celula)):
            celula = celula.replace('B', '')
            celula = pd.to_numeric(celula) * pow(10,8)
        else:
            celula = pd.to_numeric(celula)
        return celula
    
    columns = df.columns
    if 'Date' in columns:
        df['Date'] = pd.to_datetime(df['Date'])
    if 'Open' in columns:
        df['Open'] = df['Open'].replace(',', '', regex=True)
        df['Open'] = pd.to_numeric(df['Open'])
    if 'Price' in columns:
        df['Price'] = df['Price'].replace(',', '', regex=True)
        df['Price'] = pd.to_numeric(df['Price'])
    if 'High' in columns:
        df['High'] = df['High'].replace(',', '', regex=True)
        df['High'] = pd.to_numeric(df['High'])
    if 'Low' in columns:
        df['Low'] = df['Low'].replace(',', '', regex=True)
        df['Low'] = pd.to_numeric(df['Low'])
    if 'Vol.' in columns:
        copy = df['Vol.'].copy().replace(',', '', regex=True)
        copy = copy.map(format_vol)
        df['Vol.'] = copy
    if 'Change %' in columns:
        df['Change %'] = df['Change %'].replace('%', '', regex=True)
        df['Change %'] = pd.to_numeric(df['Change %'])
        df['Change %'] /= 100
    return df