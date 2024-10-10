Códigos utilizados
==================

Segue abaixo uma breve descrição de cada arquivo de códigos


`Analise Temporal`_
-------------------
Funções criadas para a análise das criptomoedas ao longo do tempo que
trabalham de maneira semelhante e conversam entre si (Entradas e saídas
relacionadas). Além de funções diretamente relacionadas a datas, como 
*agrupate_dates()*, contém também funções que trabalham e formatam com os
dados dos dataframes, como *normalize_value_columns()*, que frequentemente
foram utilizadas em um mesmo contexto

`Basics`_
---------
Funções criadas para um contexto geral, com funções básicas para serem
utilizadas em diversos contextos, como *read_data()* que apenas realizado
a tarefa de abrir o arquivo passado.

`Hipotese Jean`_
----------------
Esse corpo de código foi criado com o intuito de trabalhar com os dataframes
e responder a primeira hipótese: **Ethereum ou Solana? Qual das duas será mais
utilizada no futuro**

`Hipotese Helora`_
------------------
Esse corpo de código foi criado com a intenção de armazenar as funções e as 
funções que visam a análise da segunda hipótese: **Influência do Bitcoin: As 
variações no preço do Bitcoin influenciam no valor das outras moedas?**

`Hipotese Rodrigo`_
-------------------
Esse corpo de código foi criado para realizar a análise dos dados de maneira
a realizar a análise proposta na terceira hipótese: **Halving do Bitcoin: 
Quanto tempo depois ocorrem os picos de preço?**

.. _`Analise Temporal`: analise_temporal.html
.. _`Basics`: basics.html
.. _`Hipotese Jean`: hipotese_Jean.html
.. _`Hipotese Helora`: hipotese_Helora.html
.. _`Hipotese Rodrigo`: hipotese_Rodrigo.html

.. toctree::
   :maxdepth: 4

   analise_temporal
   basics
   hipotese_Jean
   hipotese_Helora
   hipotese_Rodrigo