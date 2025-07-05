from fastapi import FastAPI
from app.api.v1.endpoints import indicators, auth
from app.services.loader import load_and_clean_data

app = FastAPI(debug=True)

@app.on_event("startup")
def load_parquet_data():
    app.state.stock_data = load_and_clean_data()
@app.get("/")
def test():
    return {"msg": "it works"}
app.include_router(indicators.router, prefix="/api/v1", tags=["Indicators"])
app.include_router(auth.router, tags=["Auth"])

