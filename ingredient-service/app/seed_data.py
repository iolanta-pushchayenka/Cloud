from app.database import SessionLocal
from app.models import IngredientCategory, Ingredient, IngredientInventory
from datetime import datetime

db = SessionLocal()

# --- Category ---
cat1 = IngredientCategory(
    name="Vegetables",
    description="Fresh vegetables"
)

cat2 = IngredientCategory(
    name="Dairy",
    description="Milk products"
)

db.add_all([cat1, cat2])
db.commit()

db.refresh(cat1)
db.refresh(cat2)

# --- Ingredient ---
ing1 = Ingredient(
    name="Tomato",
    description="Red tomato",
    category_id=cat1.category_id,
    price=2,
    availability_status="available"
)

ing2 = Ingredient(
    name="Cheese",
    description="Cheddar cheese",
    category_id=cat2.category_id,
    price=5,
    availability_status="available"
)

db.add_all([ing1, ing2])
db.commit()

db.refresh(ing1)
db.refresh(ing2)

# --- Inventory ---
inv1 = IngredientInventory(
    ingredient_id=ing1.ingredient_id,
    stock_quantity=100,
    reserved_quantity=10
)

inv2 = IngredientInventory(
    ingredient_id=ing2.ingredient_id,
    stock_quantity=50,
    reserved_quantity=5
)

db.add_all([inv1, inv2])
db.commit()

db.close()