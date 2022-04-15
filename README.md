# currency_vmms
API para fornecer variações de médias móveis simples das moedas Bitcoin e Etherium, através de um serviço de backend python. 

O projeto foi implementado utilizando um servidor Flask, o qual disponibiliza o endpoint para retorno da variação da MMS para cada moeda no período desejado, sendo considerada a MMS para 20, 50 e 200 dias, com base nos últimos 365 dias. Para cálculo das médias, são utilizados os valores de fechamento de cada moeda, obtidos através da API de candles do Mercado Bitcoin.

Para execução do projeto, deve-se instalar as dependências listadas em requirements.txt, em ambiente Python (recomendado python 3.7 com ambiente virtual). Ademais, devem ser definidas as variáveis de ambiente:

1. **DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_SCHEMA** - Conexão com o banco de dados, sendo respectivamente: usuário, senha, endereço IP do host, porta do host, esquema usado para o projeto.
2. **STAGE** - Definição do ambiente de execução entre Local, Teste, Desenvolvimento ou Produção, respectivamente associados aos valores: Local, Test, Development, Production.

Deve-se ter um serviço de banco de dados MySQL ativo, o que pode ser feito utilizando o container:

**docker run --name mysqlbd1 -e MYSQL_ROOT_PASSWORD=my_password -p "3307:3306" -d mysql**

Deve ser criado o esquema **currency_vmms** no banco. Então, é preciso executar o script **manager.py** para realizar a migração e adicionar os modelos do projeto como tabelas no banco. Para tanto, esse script deve ser executado com os parâmetros, em orddem:

1. db init
2. db migrate
3. db upgrade

Feito isto, basta executar o script **application.py** para iniciar o servidor. Por padrão, o Flask o executará em **localhost:5000**. Para melhor entendimento e uso da aplicação, acessar a documentação Swagger: http://localhost:5000/apidocs/

A aplicação também pode ser iniciada em container, utilizando Dockerfile do projeto. Basta construí-lo informando as mesmas variáveis de ambiente citadas anteriormente, já tendo as dependências de banco descritas configuradas e ativas.

O projeto possui uma funcionalidade de **Scheduler**, a qual irá executar Jobs periódicos para atualização da base de dados, bem como para verificação e tratamento de falhas. Há dois schedulers implementados, de modo que ambos se iniciam ao iniciar a aplicação:

1. **CurrenciesMMSScheduler**: Executado diariamente, com o objetivo de incrementar os registros do banco correspondentes às médias móveis simples para Bitcoin e Etherium. Este módulo obtém o valor de fechamento de cada moeda, a cada dia, por meio da API de candles, e então cálcula as médias móveis simples de 20, 50 e 200 dias, para os dias correspondentes, persistindo o resultado em banco. Dessa forma, a cada dia em que executar, atualizará a base com o cálculo de médias para aquele dia. Caso haja algum erro durante sua execução, incluindo indisponibilidade da API de candles, será feito um número fixo de retentativas, e se ainda assim não houver sucesso, o scheduler será agendado para o dia seguinte. Dado isso, para tratar dias em que não foi possível realizar o cálculo, sempre ao iniciar a execução diária do scheduler, será verificado no banco qual o último dia registrado, e então a operação de incremento das médias será feita para os dias faltantes. Sendo assim, caso a API de candles fique indisponível por um período, será feita toda a atualização dos dias faltantes acumulados desse período, assim que a API ficar disponível novamente.