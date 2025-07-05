
---
# Architecture – Backend Assignment

##  Tech Stack

| Layer         | Technology Used                                  |
|---------------|--------------------------------------------------|
| Backend       | **FastAPI (Python 3.10.10)**                     |
| Auth          | **JWT-based Authentication** using `python-jose` |
| Database      | **PostgreSQL** with SQLAlchemy ORM               |
| Data Handling | **Pandas**, preloaded `.parquet` file            |
| API Server    | **Uvicorn** (ASGI)                               |
| Docs          | **FastAPI Swagger/OpenAPI** UI                   |

---

## System Overview

[//]: # (###  Component Diagram)

[//]: # ()
[//]: # ()
[//]: # ([PostgreSQL DB])
## Data Loading Strategy

- At startup, the entire `.parquet` file (3 years of OHLC stock data) is loaded into memory via Pandas.
- Stored as `app.state.stock_data` using `@app.on_event("startup")`.
- This approach ensures:
  - Fast access via multi-index filtering (symbol + date).
  - Avoids expensive disk I/O per request.
- If data grows large, this can be switched to:
  - **Polars/Dask** for lazy loading
  - **Database-backed storage** like TimescaleDB

---

## Technical Indicators Implemented

| Indicator     | Parameters                          |
|---------------|-------------------------------------|
| SMA           | Period                              |
| EMA           | Period                              |
| RSI           | Period                              |
| MACD          | Fast, Slow, Signal Periods          |
| Bollinger     | Period, Std Dev Multiplier          |

---

## Subscription & Access Model

| Tier     | Indicators        | Max Days Allowed | Daily Requests |
|----------|-------------------|------------------|----------------|
| Free     | SMA, EMA          | 90 days          | 50             |
| Pro      | + RSI, MACD       | 365 days         | 500            |
| Premium  | All + Bollinger   | 3 years (full)   | Unlimited      |

### All checks are enforced using a `check_access(user, indicator, dates)` function.

---

##  Rate Limiting Strategy

- Each `User` model has:
  - `requests_today`: int
  - `last_request_date`: date
- If `last_request_date != today`, requests reset.
- Enforced per request before processing.

>  Avoids need for Redis or external counters.

---

##  Scalability Considerations

| Concern             | Current Approach                  | Future Ready? |
|---------------------|-----------------------------------|----------------|
| Large Data File     | Loaded once, stored in memory     | ✅             |
| Request Limits      | Stored in DB                      | ✅             |
| Caching             | Optional layer (Redis)            | ⚪             |
| Async Support       | FastAPI + Uvicorn (ASGI) enabled  | ✅             |
| Deployment          | Docker-compatible                 | ✅             |

---

##  Security Considerations

- JWT auth required for all `/indicators/*` endpoints
- Tokens verified using `python-jose`
- Passwords hashed with `passlib[bcrypt]`
- Data access is strictly filtered by:
  - Tier
  - Date range
  - Indicator allowed
- Rate-limiting prevents abuse

---

## Conclusion

This design ensures:
- Fast indicator responses
- Scalable tier-based restrictions
- Clean, modular, secure codebase
- Ready for caching and Dockerization

