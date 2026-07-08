from fastapi import FastAPI
from app.routes.stats import router as stats_router
from app.routes.indicators import router as indicator_router
from app.routes.alerts import router as alerts_router
from app.routes.feeds import router as feeds_router
from app.utils.auth import router as auth_router

app = FastAPI(title="Threat Intel API")
app.include_router(auth_router)
app.include_router(stats_router)
app.include_router(indicator_router)
app.include_router(alerts_router)
app.include_router(feeds_router)

@app.get("/health")
def health():
    return {"status": "ok"}

