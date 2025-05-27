from datetime import datetime
from uuid import uuid4

from fastapi import FastAPI

from src.domain.category import Category

app = FastAPI()

movies_category = Category(
    id=uuid4(),
    name="Filme",
    description="Categoria de filmes",
    created_at=datetime.now(),
    updated_at=datetime.now(),
    is_active=True,
)

series_category = Category(
    id=uuid4(),
    name="Série",
    description="Categoria de séries",
    created_at=datetime.now(),
    updated_at=datetime.now(),
    is_active=True,
)


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


@app.get("/categories")
def list_categories():
    return {
        "categories": [
            movies_category,
            series_category,
        ]
    }
