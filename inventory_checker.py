# inventory_checker.py
from product_manager import products

threshold = 5  # порог уведомления


def set_threshold(value):
    global threshold
    threshold = value
    print(f"Порог уведомления установлен: {threshold}")


def check_low_stock():
    print("\n--- Товары с низким остатком ---")
    low_stock_products = [p for p in products if p["quantity"] <= threshold]
    if not low_stock_products:
        print("Все товары в норме.")
    else:
        for product in low_stock_products:
            print(
                f"[ID: {product['id']}] "
                f"{product['name']} | "
                f"Остаток: {product['quantity']} шт."
            )
    print()