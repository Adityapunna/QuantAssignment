from fastapi import FastAPI
from app.api.v1.endpoints import indicators, auth

app = FastAPI(debug=True)

@app.get("/")
def test():
    return {"msg": "it works"}
app.include_router(indicators.router, prefix="/api/v1", tags=["Indicators"])
app.include_router(auth.router, tags=["Auth"])

