# currency_vmms
API para fornecer variações de médias móveis simples das moedas Bitcoin e Etherium, através de um serviço de backend python. 

O projeto foi implementado utilizando um servidor Flask, o qual disponibiliza o endpoint para retorno da variação da MMS para cada moeda no período desejado, sendo considerada a MMS para 20, 50 e 200 dias, com base nos últimos 365 dias. Para cálculo das médias, são utilizados os valores de fechamento de cada moeda, obtidos através da API de candles do Mercado Bitcoin.

## Execução

Para execução do projeto, deve-se instalar as dependências listadas em requirements.txt, em ambiente Python (recomendado python 3.7 com ambiente virtual). Ademais, devem ser definidas as variáveis de ambiente:

1. **DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_SCHEMA** - Conexão com o banco de dados, sendo respectivamente: usuário, senha, endereço IP do host, porta do host, esquema usado para o projeto.
2. **STAGE** - Definição do ambiente de execução entre Local, Teste, Desenvolvimento ou Produção, respectivamente associados aos valores: Local, Test, Development, Production.
3. **MAIL_USER, MAIL_PASSWORD, NOTIFICATION_EMAIL** - Dados para envio de e-mail de alerta, via SMTP, sendo respectivamente: e-mail de login e sua senha para o servidor SMTP utilziado, e o e-mail para o qual a notificação será enviada.
4. **LOGS_FOLDER** - Caminho para o diretório onde serão gerados os arquivos de Log.
5. **HOST, PORT** - Endereço do Host e sua porta para executar a aplicação (Padrão localhost:5000).

Deve-se ter um serviço de banco de dados MySQL ativo, o que pode ser feito utilizando o container:

**docker run --name mysqlbd1 -e MYSQL_ROOT_PASSWORD=my_password -p "3307:3306" -d mysql**

Deve ser criado o esquema **currency_vmms** no banco. Com base na criação do container acima, basta executar os comandos a seguir para entrar no mesmo e criar o esquema:

**docker exec -it mysqlbd1 bash**

**mysql -u root -pmy_password**

**CREATE SCHEMA currency_vmms;**

Então, é preciso executar o script **manager.py** para realizar a migração e adicionar os modelos do projeto como tabelas no banco. Para tanto, esse script deve ser executado com os parâmetros, em ordem:

1. db init
2. db migrate
3. db upgrade

Feito isto, basta executar o script **application.py** para iniciar o servidor. Por padrão, o Flask o executará em **localhost:5000**. Para melhor entendimento e uso da aplicação, acessar a documentação Swagger: http://localhost:5000/apidocs/

A aplicação também pode ser iniciada em container, utilizando Dockerfile do projeto. Basta construí-lo informando as mesmas variáveis de ambiente citadas anteriormente, já tendo as dependências de banco descritas configuradas e ativas.

## Jobs Assíncronos

O projeto possui uma funcionalidade de **Scheduler**, a qual irá executar Jobs periódicos para atualização da base de dados, bem como para verificação e tratamento de falhas. Há dois schedulers implementados, de modo que ambos se iniciam ao iniciar a aplicação:

1. **CurrenciesMMSScheduler**: Executado diariamente, com o objetivo de incrementar os registros do banco correspondentes às médias móveis simples para Bitcoin e Etherium. Este módulo obtém o valor de fechamento de cada moeda, a cada dia, por meio da API de candles, e então cálcula as médias móveis simples de 20, 50 e 200 dias, para os dias correspondentes, persistindo o resultado em banco. Dessa forma, a cada dia em que executar, atualizará a base com o cálculo de médias para aquele dia. 

* Caso haja algum erro durante sua execução, incluindo indisponibilidade da API de candles, será feito um número N de tentativas, incrementando o tempo entre cada tentativa em 1 minuto. Se ainda assim não houver sucesso, o scheduler será agendado para o dia seguinte. Dado isso, para tratar dias em que não foi possível realizar o cálculo, sempre ao iniciar a execução diária do scheduler, será verificado no banco qual o último dia registrado, e então a operação de incremento das médias será feita para os dias faltantes. Sendo assim, caso a API de candles fique indisponível por um período, será feita toda a atualização dos dias faltantes acumulados desse período, assim que a API ficar disponível novamente. 

* O Scheduler também irá realizar o carregamento inicial da tabela, calculando as MMS de 20, 50 e 200 dias, dos últimos 365 dias, de cada moeda. Isso será identificado e executado quando a tabela correspondente no banco estiver vazia.

2. **MissingDaysMonitoringScheduler**: Executado a cada hora, com o objetivo de verificar se há algum registro de MMS faltante no banco, para os últimos 365 dias. Caso haja, então será enviado um e-mail de alerta informando os dias faltantes, o que será feito através do módulo para envios de e-mail via SMTP. 
 
* O serviço SMTP foi configurado no script **mail**, com base em um servidor Gmail. Para que o mesmo funcione, as variáveis de ambiente **MAIL_USER** e **MAIL_PASSWORD** devem ser preenchidas com o login de uma conta Gmail, com a opção de **Acesso a apps menos seguras** habilitada (ou Navegação segura desabilitada). Além disso, deve ser fornecido o e-mail de destino das notificações, para a variável **NOTIFICATION_EMAIL**.

## Logs

Foi implementado um módulo para geração de **Logs**, o qual é usado tanto para os Schedulers quanto para a aplicação de modo que São gerados arquivos de Log separados para cada um. No caso dos Schedulers, são gravados possíveis erros na execução diária dos mesmos, além de informações da execução com sucesso. De forma semelhante, para a aplicação são gravados os erros que podem ocorrer no acesso a endpoints, assim como dados de requisições para os mesmos.

## Testes

Foram implementados testes unitários para os principais métodos, contidos no diretório de **tests**, os quais foram separados por móodulos e arquivos, buscando ter a cobertura da maior parte do código. Para execução dos mesmos, basta usar o comando **pytest** nesse diretório, já tendo as variáveis de ambiente definidas:

1. STAGE: Test
2. LOGS_FOLDER: Caminho para o diretório raíz do projeto.
3. As variáveis referente ao serviço de e-mail não são utilzadas no teste, então não precisam ser definidas nesse ambiente. Já para conexão de banco, é definida, na classe de teste, uma conexão com uma base SQLite simples que será gerada para os testes, não havendo necessidade das variáveis de ambiente.

## Organização

A arquitetura da aplicação seguiu uma divisão em camadas, segundo padrão do Flask:

1. **resources**: Classes representando os Endpoints e seus métodos.
2. **services**: Fornece os serviços que solicitam acesso à banco e realizam processamentos para retorno do resultado.
3. **repositories**: Define as operações sobre a base de dados.
4. **configurations**: Define a configuração da aplicação, como rotas e ambiente.
5. **models**: Mapeamento das tabelas do banco, usadas para migração e operações com SQLAlchemy.
6. **common**: Classes Abstratas, classes para exceções e outros métodos reutilizáveis.
7. **swagger**: Documentação da aplicação,, interativa pela interface Swagger.
8. **schemas**: Classes para validação de dados de entrada, com base na lib marshmallow.

* Foram criados handlers personalizados para tratar as exceções conhecidas da API.
* Os dados enviados na requisição à um endpoint são validados, a fim de identificar e informar problemas como dados em formato inválido (e.g. data final maior do que a inicial, datas em formato fora do esperado, etc) e consultas com data de início anterior a 365 dias.
