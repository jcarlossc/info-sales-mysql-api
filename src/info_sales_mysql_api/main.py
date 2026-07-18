from fastapi import FastAPI

from info_sales_mysql_api.api.routes.summary_router import router

app = FastAPI(
    title="Info Sales MySQL API",
    version="1.0.0",
)

app.include_router(router)
