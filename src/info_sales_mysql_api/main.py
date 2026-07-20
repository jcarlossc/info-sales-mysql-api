from fastapi import Depends
from fastapi import FastAPI

# Dependência responsável por validar a API Key
# antes da execução de qualquer endpoint.
from info_sales_mysql_api.api.dependencies.api_key import validate_api_key

# Importa todas as rotas da API.
from info_sales_mysql_api.api.routes.summary_router import router


# Cria a aplicação principal da API.
app = FastAPI(
    # Nome exibido na documentação Swagger.
    title="Info Sales MySQL API",
    # Versão da API.
    version="1.0.0",
    # Dependência global.
    # Toda requisição deverá passar pela validação
    # da API Key antes de acessar qualquer endpoint.
    dependencies=[Depends(validate_api_key)],
)

# Registra todas as rotas do módulo Summary.
app.include_router(router)
