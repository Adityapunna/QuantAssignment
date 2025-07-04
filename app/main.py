from fastapi import FastAPI
from app.api.v1.endpoints import indicators

app = FastAPI(debug=True)

@app.get("/")
def test():
    return {"msg": "it works"}
app.include_router(indicators.router, prefix="/api/v1", tags=["Indicators"])

#
# print("✅ App starting...")  # Debug line
#
# from fastapi import FastAPI
#
# app = FastAPI(
#     # title="MyApp",
#     # root_path="/api/v1",
#     # openapi_url="/api/v1/openapi.json",
#     # docs_url="/api/v1/docs",
#     # redoc_url="/api/v1/redoc",
#     debug=True
# )
#
# @app.get("/")
# def test():
#     print("✅ /test hit")  # Debug
#     return {"msg": "works"}
#
# from fastapi import FastAPI
#
# app = FastAPI(debug=True)
#
# @app.get("/")
# def test():
#     print("✅ /test hit")  # Debug
#     return {"msg": "works"}