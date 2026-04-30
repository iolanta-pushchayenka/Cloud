from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

Base = declarative_base()

# Category


class IngredientCategory(Base):
    __tablename__ = "ingredient_category"
    __table_args__ = {"schema": "IngredientService"}

    category_id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


# Ingredient
class Ingredient(Base):
    __tablename__ = "ingredient"
    __table_args__ = {"schema": "IngredientService"}

    ingredient_id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    category_id = Column(Integer, ForeignKey(
        "IngredientService.ingredient_category.category_id"))
    price = Column(Integer)
    availability_status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


# Inventory
class IngredientInventory(Base):
    __tablename__ = "ingredient_inventory"
    __table_args__ = {"schema": "IngredientService"}

    ingredient_id = Column(
        Integer,
        ForeignKey("IngredientService.ingredient.ingredient_id"),
        primary_key=True)
    stock_quantity = Column(Integer)
    reserved_quantity = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow)
