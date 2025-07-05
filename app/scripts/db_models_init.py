# scripts/ db_models_init
from app.db import engine
from app.db import models

models.Base.metadata.create_all(bind=engine)