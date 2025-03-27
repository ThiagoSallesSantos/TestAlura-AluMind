# Alura - AluMind

Teste par a vaga de Python com foco em LLM Alura.

Autor: [Thiago Salles Santos](https://github.com/ThiagoSallesSantos)

## Requisitos

Ferramentas necessárias:

* Python versão 3.10.* ou superior;
* Módulos pip (versão 23.* ou superior) e venv;
* Docker versão 28.* ou superior.
* Ollama versão 0.6.0
  * modelo llama3.2:latest instalado

## Configuração

Segue a configuração necessária para a execução da aplicação:

### **Criação de um ambiente virtual:**

```
python3 -m venv </caminho/para/novo/ambiente/virtual>
```

### **Acessar o ambiente virtual criado:**

* Linux:

  ```
  source </caminho/ambiente/virtual>/bin/activate
  ```
* Windows:

  ```
  </caminho/ambiente/virtual>\Scripts\activate.bat
  ```

### **Instalar as depedências:**

```
pip3 install -r requirements.txt
```

### **Setar as variaveis de ambientes:**

Para isso acesse o arquivo [.env](./.env) e configure aplicação, por padrão essas são as variaveis bases:

```
VERSION="0.0.1-beta"

APPLICATION__APP_HOST="localhost"
APPLICATION__APP_PORT=9876
APPLICATION__APP_DEBUG=1

DATABASE__DB_DBMS="postgresql"
DATABASE__DB_USERNAME="user"
DATABASE__DB_PASSWORD="pass"
DATABASE__DB_HOST="localhost"
DATABASE__DB_DATABASE="DatabaseAluMind"
DATABASE__DB_PORT=5432

EMAIL__EMAIL_EMAIL="test@test.com"
EMAIL__EMAIL_PASSWORD=""
EMAIL__EMAIL_MODEL="ollama"
EMAIL__EMAIL_API_KEY=""

```

**IMPORTANTE****:** ***As variaveis de EMAIL devem ser configuradas!* **para que aja o funcionamento correto do sistema de envio de e-mails, para isso basta adicionar o seu e-mail na variável "EMAIL__EMAIL_EMAIL" e a senha de aplicativo do **GMAIL** na variavel "EMAIL__EMAIL_PASSWORD".

### **Iniciar docker compose:**

```
docker compose up -d
```

### **Configurar o banco de dados:**

Esse comando cria as tabelas no banco de dados.

```
python3 setup_db.py
```

### Executar o código:

```
python3 main.py
```

## Testes

Dentro do diretório padrão da aplicação temos a pasta de "tests/". nela existe alguns testes, para ilucidar o sistema.

### Envio de Feedbacks

O Envio de feedbacks é feito por meio do endpoint "/feedbacks/" apartir de método "POST", espera receber-se um JSON com as seguintes variáveis:

```
{
    "id": "4042f20a-45f4-4647-8050-139ac16f610a",
    "feedback": "Gosto muito de usar o Alumind! Está me ajudando bastante em relação a alguns problemas que tenho. Só quer ia que houvesse uma forma mais fácil de eu mesmo realizar a edição do meu perfil dentro da minha conta",
    "options": {
        "model": "",
        "api_key": ""
    }
}
```

**OBS:** Sendo "*options*" um parametro opicional, que permite escolher qual provedor de modelo deseja utilizar, entre: "ollama", "openai", "gemini". No caso de escolha do "openai", "gemini", é necessário informar a "*api_key*", caso não informe o parâmetro de "*options*", por padrão será utilizado o "ollama".

### Relatório

Para acessar o relatório basta acessar através do seu navegador, o endpoint "/report/".

### Envio de E-mails

O envio de e-mail irá ocorrer todos os sábados às 23:59, e enviará o e-mail somente para os e-mails cadastrados no banco de dados.

#### Adicionar E-mail ao banco de dados

Para cadastrar um e-mail no banco de dados, para que esse e-mail receba o relatório da semana, basta enviar um "POST" para o endpoint "/email/", com o seguinte JSON:

```
{
    "email": "",
    "name": ""
}
```

Onde o "email" refere-se ao e-mail da pessoa, e "name" ao nome da pessoa que irá receber o relatório.

## Organização

O sistema se encontra organizado no seguinte formato:

```
├── docker-compose.yml
├── instructions
│   └── Teste vaga de Python com foco em LLM _ Alura.pdf
├── main.py
├── README.md
├── requirements.txt
├── setup_db.py
├── src
│   ├── database
│   │   ├── connect.py
│   │   ├── models.py
│   │   ├── query.py
│   │   └── utils.py
│   ├── model
│   │   ├── classify_feedback.py
│   │   ├── email.py
│   │   ├── model.py
│   │   ├── prompt.py
│   │   └── statistics.py
│   ├── routes
│   │   ├── email.py
│   │   ├── feedback.py
│   │   ├── __init__.py
│   │   ├── report.py
│   │   └── utils.py
│   ├── schemas
│   │   └── schemas.py
│   └── settings.py
├── templates
│   ├── base.html
│   ├── feature_report.html
│   ├── feedback_report.html
│   ├── footer.html
│   ├── header.html
│   ├── report.html
│   └── sentiment_report.html
└── tests
    ├── get_feedback.py
    ├── send_email.py
    ├── send_feedback.py
    ├── test_classify.py
    └── test_email.py

```
