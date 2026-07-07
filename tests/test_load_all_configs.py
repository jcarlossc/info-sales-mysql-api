from pathlib import Path

from info_sales_mysql_api.utils.load_yaml.loader_yaml import load_all_configs


def test_load_all_configs_retorna_dicionario():
    """
    Verifica se a função retorna um dicionário
    ao carregar um arquivo YAML válido.
    """

    # Arrange (Preparação)

    # Diretório de teste contendo arquivos YAML
    config_path = Path("config")

    # Act (Execução)

    # Executa a função que será testada
    resultado = load_all_configs(config_path)

    # Assert (Verificação)

    # Verifica se o retorno é um dicionário
    assert isinstance(resultado, dict)

    # Verifica se a configuração "logging.yaml"
    # foi carregada para o dicionário
    assert resultado["logging"]["logging"]["level"] == "INFO"

    # Verifica se a configuração "logging.yaml"
    # foi carregada para o dicionário
    assert (
        resultado["logging"]["logging"]["format"]
        == "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # Verifica se a configuração "paths.yaml"
    # foi carregada para o dicionário
    assert resultado["paths"]["logs"]["file"] == "logs/app.log"
