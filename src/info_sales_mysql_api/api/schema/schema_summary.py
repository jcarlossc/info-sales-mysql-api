from pydantic import BaseModel


class Period(BaseModel):
    """
    Representa o intervalo de datas da base de vendas.

    Attributes
    ----------
    start : str
        Data inicial das vendas.
    end : str
        Data final das vendas.
    """

    start: str
    end: str


class Metadata(BaseModel):
    """
    Metadados gerais da base de dados utilizada na análise.

    Attributes
    ----------
    rows : int
        Quantidade total de registros.
    columns : int
        Quantidade total de colunas.
    products : int
        Número de produtos distintos.
    sellers : int
        Número de vendedores distintos.
    period : Period
        Intervalo de datas da base.
    """

    rows: int
    columns: int
    products: int
    sellers: int
    period: Period


class KPIs(BaseModel):
    """
    Principais indicadores de desempenho (KPIs).
    """

    revenue: float
    profit: float
    orders: int
    items_sold: int
    average_ticket: float
    average_discount: float
    margin: float


class Products(BaseModel):
    """
    Indicadores relacionados aos produtos.
    """

    top_revenue: dict[str, float]
    top_quantity: dict[str, int]
    lowest_revenue: dict[str, float]


class Categories(BaseModel):
    """
    Indicadores por categoria de produto.
    """

    revenue: dict[str, float]
    quantity: dict[str, int]


class Sellers(BaseModel):
    """
    Indicadores de desempenho dos vendedores.
    """

    revenue: dict[str, float]
    orders: dict[str, int]
    profit: dict[str, float]


class Geography(BaseModel):
    """
    Indicadores geográficos.
    """

    states: dict[str, float]
    cities: dict[str, float]


class Time(BaseModel):
    """
    Indicadores temporais das vendas.
    """

    year: dict[int, float]
    month: dict[str, float]
    weekday: dict[str, float]


class Payments(BaseModel):
    """
    Distribuição do faturamento por forma de pagamento.
    """

    methods: dict[str, float]


class Status(BaseModel):
    """
    Distribuição dos pedidos por status.
    """

    orders: dict[str, int]


class SalesSummary(BaseModel):
    """
    Resumo completo das métricas disponibilizadas pela API.

    Este modelo agrega os metadados da base, KPIs,
    rankings, distribuições e indicadores utilizados
    pelos dashboards e análises.
    """

    metadata: Metadata
    kpis: KPIs
    products: Products
    categories: Categories
    sellers: Sellers
    geography: Geography
    time: Time
    payments: Payments
    status: Status
