from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Representa as configurações da aplicação.

    Todos os atributos são carregados automaticamente do
    arquivo .env.
    """

    # Chave da API
    api_key: str

    # Endereço do servidor MySQL.
    mysql_host: str

    # Porta utilizada pelo servidor MySQL.
    mysql_port: int = 3306

    # Nome do banco de dados.
    mysql_database: str

    # Usuário do banco.
    mysql_user: str

    # Senha do banco.
    mysql_password: str

    # Configuração do Pydantic.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
