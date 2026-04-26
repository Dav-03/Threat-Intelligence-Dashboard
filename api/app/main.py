from fastapi import FastAPI

app = FastAPI(title="Threat Intel API")

@app.get("/health")
def health():
    return {"status": "ok"}
