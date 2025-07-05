
#  Quant Backend Assignment – Financial Indicators API

##  Overview

This project is a **FastAPI-based backend** for computing **stock indicators** like SMA, EMA, RSI, MACD, and Bollinger Bands using preloaded stock data. It includes:
- **Tier-based access control** (Free, Pro, Premium)
- **JWT authentication**
- **Daily request limits**
- **In-memory data processing** for speed

---

##  Tech Stack

| Layer        | Technology               |
|--------------|--------------------------|
| Framework    | FastAPI (Python 3.10.10) |
| Auth         | JWT (via python-jose)    |
| Database     | PostgreSQL + SQLAlchemy  |
| Data Format  | Parquet via Pandas       |
| ORM          | SQLAlchemy               |
| Web Server   | Uvicorn (ASGI)           |

---

##  Project Structure

```
QuantAssignment/
├── app/
│   ├── api/v1/endpoints/         # Routers: indicators, auth
│   ├── services/                 # Business logic (indicators, auth, access control)
│   ├── db/                       # Models and DB setup
│   └── utils/                    # Helper functions
├── config.py                     # Config constants
├── main.py                       # FastAPI app entry point
├── requirements.txt              # Python dependencies
├── architecture.md               # System design doc
└── README.md                     # You're here!
```

---

##  Setup Instructions

### 1. Clone & Create Environment

```bash
git clone <repo_url>
cd QuantAssignment
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare the `.env` File (optional)

Ensure your `DATABASE_URL` is set (or configure in `config.py`).

### 4. Run the Server

```bash
uvicorn main:app --reload
```

---

## 🛠 Features

-  Secure endpoints with JWT
-  Tier-based access (Free, Pro, Premium)
-  Daily request limits per tier
-  Preloaded `.parquet` file for fast access
-  OpenAPI docs via `/docs`

---

##  Authentication

### Signup

```
POST /signup
{
  "email": "user@example.com",
  "password": "password123",
  "tier": "Free"
}
```

### Login

```
POST /login
→ Returns: { "access_token": "..." }
```

Use this token in `Authorization: Bearer <token>` for all `/indicators/*` endpoints.

---

##  API Endpoints

| Method | Endpoint                  | Description             |
|--------|---------------------------|-------------------------|
| GET    | `/indicators/sma`         | Simple Moving Average   |
| GET    | `/indicators/ema`         | Exponential MA          |
| GET    | `/indicators/rsi`         | Relative Strength Index |
| GET    | `/indicators/macd`        | MACD Indicator          |
| GET    | `/indicators/bollinger`   | Bollinger Bands         |

All accept:
- `stock_symbol`
- `start_date`, `end_date`
- `period` (or custom args)

#### /indicators/sma

- **stock_symbol**: `str` (e.g., "AAPL")
- **start_date**: `YYYY-MM-DD`
- **end_date**: `YYYY-MM-DD`
- **period**: `int` (default: 20)

---

#### /indicators/ema

- **stock_symbol**: `str`
- **start_date**: `YYYY-MM-DD`
- **end_date**: `YYYY-MM-DD`
- **period**: `int` (default: 20)

---

#### /indicators/rsi

- **stock_symbol**: `str`
- **start_date**: `YYYY-MM-DD`
- **end_date**: `YYYY-MM-DD`
- **period**: `int` (default: 14)

---

#### /indicators/macd

- **stock_symbol**: `str`
- **start_date**: `YYYY-MM-DD`
- **end_date**: `YYYY-MM-DD`
- **fast_period**: `int` (default: 12)
- **slow_period**: `int` (default: 26)
- **signal_period**: `int` (default: 9)

---

#### /indicators/bollinger

- **stock_symbol**: `str`
- **start_date**: `YYYY-MM-DD`
- **end_date**: `YYYY-MM-DD`
- **period**: `int` (default: 20)
- **num_std_dev**: `int` (default: 2)

---

##  Subscription Tiers

| Tier     | Indicators        | Max Days | Daily Requests |
|----------|-------------------|----------|----------------|
| Free     | SMA, EMA          | 90       | 50             |
| Pro      | + RSI, MACD       | 365      | 500            |
| Premium  | All               | Full     | Unlimited      |

---

##  Testing

You can test endpoints using:
- Swagger UI: `http://localhost:8000/docs`
- Postman / Curl with JWT token
- Unit tests (written for core indicator logic)

---

##  Documentation

-  See `architecture.md` for detailed system design.
-  Cleanly modularized by domain.

---

##  Future Improvements

- Add Redis-based rate limiting (e.g. `slowapi`)
- Add database migrations via Alembic
- Dockerize the app for easier deployment
- Add CI tests and monitoring hooks

---

##  Author

**Aditya Punna**  
Backend Developer | Quant Assignment

---

##  Submission Checklist

- Working API with all 5 indicators
- JWT Auth with Signup/Login
- Tier-based access + daily request logic
- Fast load of parquet data  
- Code modularized into services/routers
- Efficient Data cleaning, preprocessing (Handling Nulls etc)
- Column names are handled to avoid ambiguity
- Markdown docs (`README.md`, `architecture.md`)
