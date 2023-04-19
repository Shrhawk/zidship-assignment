from fastapi import FastAPI

from utils.data_population import populate_courier
from views.easypost_views import easypost_router


app = FastAPI(openapi_url="/openapi.json", title="ZidShip")


populate_courier()


@app.get("/")
async def zidship_service_health():
    return {
        "service": "ZidShip Service Version 1.0"
    }

app.router.prefix = "/api/v1"
app.include_router(easypost_router, prefix="/easypost", tags=["EasyPost"])
