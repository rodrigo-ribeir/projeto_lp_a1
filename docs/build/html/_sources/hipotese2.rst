Hipótese 2: Influência do Bitcoin - As variações no preço do Bitcoin influenciam no valor das outras moedas?
============================================================================================================

Introdução
----------

O Bitcoin é a criptomoeda de maior valor no mercado e vem se tornando cada vez mais conhecida. Essa fama 
pode acabar gerando nas outras pessoas um interesse nas outras criptomoedas. Podendo fazer com que o preço
de outras criptomoedas aumente quando o preço do Bitcoin aumenta e diminua quando o preço do Bitcoin diminiu.

Análise Inicial
---------------

Queremos comparar as variações diárias de preços do Bitcoin_ com as de Solana_ e Ethereum_. Para fazer essa
comparação, utilizaremos os preços e as mudanças diárias de cada criptomoeda. Sendo assim, serão 
necessárias somente as colunas `Price`, `Date` e `Change %`:

- `Bitcoin`

.. include:: ../../data/dataframes/bitcoin_values.md
    :parser: myst_parser.sphinx_

- `Solana`

.. include:: ../../data/dataframes/solana_values.md
    :parser: myst_parser.sphinx_

- `Ethereum`

.. include:: ../../data/dataframes/ethereum_values.md
    :parser: myst_parser.sphinx_


Observações
-----------

Separaremos em duas etapas:

**Visualização Gráfica**

- `Bitcoin vs Solana`:

.. image:: ../../data/imagens/bitcoin_x_solana.png

- `Bitcoin vs Ethereum`:

.. image:: ../../data/imagens/bitcoin_x_ethereum.png

Observando os gráficos acima, pode-se perceber que mudanças significativas nos preços do Bitcoin podem levar
a variações também consideráveis nas outras criptomoedas. No entanto, visualizar somente os gráficos, nem sempre
é a melhor opção, pois pode haver detalhes faltando que não são tão claros. Por isso, também faremos uma
comparação por tabelas.

**Análise pela Tabela**

- `Bitcoin vs Solana`:

.. include:: ../../data/dataframes/bitcoin_x_solana.md
    :parser: myst_parser.sphinx_

- `Bitcoin vs Ethereum`:

.. include:: ../../data/dataframes/bitcoin_x_ethereum.md
    :parser: myst_parser.sphinx_

Tendo as tabelas agrupadas, podemos comparar as colunas `Change %`, e calcular a quantidade de vezes que
ambas tiveram uma mudança positiva/negativa e a quantidade de vezes que as mudanças foram opostas. Teremos
assim, o seguinte resultado:

- Tabela 1 - Mesmas mudanças: 1003, Mudanças opostas: 341
- Tabela 2 - Mesmas mudanças: 1120, Mudanças opostas: 224

Portanto, é fácil ver que a frequência em que as mudanças são as mesmas é maior do que quando são opostas.

Conclusão
---------

Observando os dados obtidos, é notório que, de certo modo, os aumentos e quedas do Bitcoin podem influenciar as outras
criptomoedas. Os gráficos mostram que quando ocorre os picos de aumento do preço do Bitcoin ocorre também aumento nas
outras criptomoedas. Já as tabelas mostram que a Solana e a Ethereum tiveram aumentos de preço em datas em que os preços
do Bitcoin também aumentaram. Juntando os gráficos e as tabelas podemos observar com mais clareza e não poe-se negar que
pode haver uma correlação positiva entre as criptomoedas e o Bitcoin.

**Aviso Legal**: Sabendo dessas informações, nada podemos concluir com certeza sobre a hipótese questionada, porque seria 
necessário conhecer um pouco mais sobre ou ter ajuda de profissionais nas áreas de Probabilidade e Análises no geral.

.. _Ethereum: https://www.investing.com/crypto/ethereum
.. _Solana: https://www.investing.com/crypto/solana
.. _Bitcoin: https://www.investing.com/crypto/bitcoin