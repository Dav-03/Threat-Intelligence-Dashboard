from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import stats, indicators, alerts, feeds
from app.utils.auth import router as auth_router

app = FastAPI(title="Threat Intel API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(indicators.router)
app.include_router(alerts.router)
app.include_router(feeds.router)
app.include_router(stats.router)

@app.get("/health")
def health():
    return {"status": "ok"}