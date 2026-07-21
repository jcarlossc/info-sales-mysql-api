<div align="center">

# 📊 Info Sales MySQL API

<img src="https://github.com/jcarlossc/info-sales-mysql-api/blob/main/images/ca386977-a347-4b7f-9b76-6d66e9918efa.png">

### Pipeline Analítico de Vendas  

Info Sales MySQL API é uma API desenvolvida em Python utilizando FastAPI, responsável por consumir dados de um banco MySQL, realizar tratamento, 
validação e análise das informações e disponibilizar indicadores de negócio (KPIs) através de endpoints REST.

O projeto foi desenvolvido aplicando práticas modernas de Engenharia de Software, Arquitetura Limpa e Data Analytics, simulando um ambiente de 
produção utilizado em empresas de tecnologia.

<img src="https://img.shields.io/badge/Python-276DC3?style=for-the-badge&logo=r&logoColor=white" />
<img src="https://img.shields.io/badge/STATUS-EM%20DESENVOLVIMENTO-success?style=for-the-badge" />
<img src="https://img.shields.io/badge/LICENSE-MIT-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/TESTS-pytest-orange?style=for-the-badge" />

</div>

---

## 🎯 Objetivos
* Consumir dados de um banco MySQL
* Validar dados antes do processamento
* Tratar exceções 
* Calcular KPIs de negócio
* Disponibilizar métricas através de API REST
* Garantir qualidade do código com testes automatizados
* Automatizar releases e integração contínua
* Demonstrar boas práticas de desenvolvimento profissional

## 🏗 Arquitetura
```
                MySQL Database
                       │
                       ▼
             SQLAlchemy Connection
                       │
                       ▼
              Data Standardization
                       │
                       ▼
                Data Cleanning 
                       │
                       ▼
                 Business KPIs            
                       │
                       ▼
               FastAPI Endpoints
                       │
                       ▼
                   JSON API
```

## 📁 Estrutura do Projeto

```
info_sales_mysql_api/
├───.github
│   └───workflows
│          ├───ci.yml
│          └───release-please.yml                
├───config
│     ├───db.yaml
│     ├───logging.yaml
│     └───paths.yaml
├───htmlcov
├───images
├───logs
│     └───app.log
├───script_sql
│     └───loja_info_plus.sql
├───src
│   └───info_sales_mysql_api
│       ├───api
│       │   ├───dependencies
│       │   |    └───api_key.py
│       │   ├───routes
│       │   |    └───summary_router.py
│       │   └───schema
│       │        └───schema_summary.py
│       ├───cleanning
│       │        └───data_clean.py
│       ├───database
│       │   ├───connection
│       │   |    └───get_connection.py
│       │   └───query
│       │        └───load_sales.py
│       ├───pipeline
│       │        └───pipeline_service.py
│       ├───standardization
│       │        └───get_standardization.py
│       ├───summary
│       │        └───get_summary.py
│       ├───utils
│       │      ├───config_env
│       │      │     └───Settings.py
│       │      ├───load_yaml
│       │      │     └───loader_yaml.py
│       │      ├───loggers
│       │      │     └───logger.py
│       │      └───retry
│       │            └───load_retry.py
│       └───main.py
├───tests
├───.coverage
├───.env
├───.env.example
├───.gitignore
├───pre-commit-config.yaml
├───LICENSE
├───poetry.lock
├───pyproject.toml
└───README.md

```

## Mode de Utilização

1. Execute o XAMPP
* Caso não o tenha, baixe-o: <a href="https://www.apachefriends.org/pt_br/download.html">https://www.apachefriends.org/pt_br/download.html</a>
* Instale-o normalmente
* Execute o Painel de Controle
* Acione o Apache e o MySQL/MariaDB
* Ao lado do botão start/stop do MySQL/MariaDB, clique em Admin. Isso irá abrir a interface do MySQL/MariaDB no navegador
* Clique na aba importar e em escolher arquivo: o script está na raiz do projeto: ```script_sql/loja_info_plus.sql```, após isso, clique em importar no final da página
* A configuração do Banco de Dados está no ```.env.example```

3. Com a linguagem Python instalada: <a href="https://www.python.org/downloads/" target="_blank">https://www.python.org/downloads/</a>
4. Instale o pipx: 
```
pip install pipx
```
5. Em seguida:
```
pipx ensurepath
```
6. E, por fim, o gerenciador Poetry:
```
pipx install poetry
```
7. Clone o repositório e acesse o diretório
```
git clone https://github.com/jcarlossc/info-sales-mysql-api.git
cd info-sales-mysql-api
```
8. Instalação das dependências:
```
poetry install
```
9. Para executar o projeto:
```
poetry run task app
```

## Licença
Este projeto está licenciado sob MIT License.

## 🎯 Desenvolvedor focado em:

- Data Engineering
- Analytics
- R Programming
- Python Programming
- Automação de processos
- Engenharia de Software

## Contato
* Autor: Carlos da Costa
* Recife, PE - Brasil
* Telefone: +55 81 99712 9140
* Telegram: @jcarlossc
* Blogger linguagem R: https://informaticus77-r.blogspot.com/
* Blogger linguagem Python: https://informaticus77-python.blogspot.com/
* Email: jcarlossc1977@gmail.com
* LinkedIn: https://www.linkedin.com/in/carlos-da-costa-669252149/
* GitHub: https://github.com/jcarlossc
* Kaggle: https://www.kaggle.com/jcarlossc/
* Twitter/X: https://x.com/jcarlossc1977
