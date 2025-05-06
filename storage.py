# storage.py
import json
import os
from product_manager import products, next_id, DATA_FILE


def save_data():
    data = {
        "products": products,
        "next_id": next_id
    }
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Данные сохранены.")


def load_data():
    global products, next_id
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            products.clear()
            products.extend(data.get("products", []))
            next_id = data.get("next_id", len(products) + 1)
        print("Данные загружены.")
    else:
        print("Файл данных не найден.")