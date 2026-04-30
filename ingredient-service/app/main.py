from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Ingredient, IngredientInventory

import logging

# ---------------- logging ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ---------------- app ----------------
app = FastAPI()

# ---------------- DB dependency ----------------


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- GET /ingredients ----------------


@app.get("/ingredients")
def get_ingredients(db: Session = Depends(get_db)):
    logger.info("Fetching ingredients list")

    ingredients = db.query(Ingredient).all()

    result = []

    for ing in ingredients:
        inventory = db.query(IngredientInventory).filter(
            IngredientInventory.ingredient_id == ing.ingredient_id
        ).first()

        result.append({
            "id": ing.ingredient_id,
            "name": ing.name,
            "description": ing.description,
            "price": ing.price,
            "available": (
                inventory.stock_quantity - inventory.reserved_quantity
                if inventory else 0
            )
        })

    return result
