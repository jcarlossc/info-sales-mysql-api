from pydantic import BaseModel


class Period(BaseModel):
    start: str
    end: str


class Metadata(BaseModel):
    rows: int
    columns: int
    products: int
    sellers: int
    period: Period


class KPIs(BaseModel):
    revenue: float
    profit: float
    orders: int
    items_sold: int
    average_ticket: float
    average_discount: float
    margin: float


class Products(BaseModel):
    top_revenue: dict[str, float]
    top_quantity: dict[str, int]
    lowest_revenue: dict[str, float]


class Categories(BaseModel):
    revenue: dict[str, float]
    quantity: dict[str, int]


class Sellers(BaseModel):
    revenue: dict[str, float]
    orders: dict[str, int]
    profit: dict[str, float]


class Geography(BaseModel):
    states: dict[str, float]
    cities: dict[str, float]


class Time(BaseModel):
    year: dict[int, float]
    month: dict[str, float]
    weekday: dict[str, float]


class Payments(BaseModel):
    methods: dict[str, float]


class Status(BaseModel):
    orders: dict[str, int]


class SalesSummary(BaseModel):
    metadata: Metadata
    kpis: KPIs
    products: Products
    categories: Categories
    sellers: Sellers
    geography: Geography
    time: Time
    payments: Payments
    status: Status
