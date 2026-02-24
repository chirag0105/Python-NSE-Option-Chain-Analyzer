from fastapi import FastAPI

app = FastAPI(title="NSE Option Chain Analyzer API")

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
