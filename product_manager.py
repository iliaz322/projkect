# product_manager.py
import json
import os

DATA_FILE = "data.json"
products = []
next_id = 1


def load_products():
    global products, next_id
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            products.extend(data.get("products", []))
            next_id = data.get("next_id", len(products) + 1)


def save_products():
    data = {
        "products": products,
        "next_id": next_id
    }
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def add_product():
    global next_id  # ✅ Сначала объявляем глобальной
    print("\n--- Добавление нового товара ---")
    name = input("Введите название товара: ")
    category = input("Введите категорию: ")
    supplier = input("Введите поставщика: ")

    try:
        price = float(input("Введите цену: "))
        quantity = int(input("Введите количество на складе: "))
    except ValueError:
        print("Ошибка: цена или количество указаны неверно.")
        return

    product = {
        "id": next_id,  # ✅ Теперь всё верно
        "name": name,
        "category": category,
        "supplier": supplier,
        "price": price,
        "quantity": quantity
    }

    products.append(product)
    print(f"Товар '{name}' успешно добавлен!")
    next_id += 1


def view_products():
    print("\n--- Список товаров ---")
    if not products:
        print("Склад пуст.")
        return
    for product in products:
        print(
            f"[ID: {product['id']}] "
            f"{product['name']} | "
            f"Категория: {product['category']} | "
            f"Поставщик: {product['supplier']} | "
            f"Цена: {product['price']} | "
            f"Остаток: {product['quantity']}"
        )
    print()


def edit_product():
    view_products()
    try:
        product_id = int(input("Введите ID товара для редактирования: "))
    except ValueError:
        print("Ошибка: введён некорректный ID.")
        return

    for product in products:
        if product["id"] == product_id:
            print(f"\nРедактирование: {product['name']}")

            name = input(f"Новое название [{product['name']}]: ")
            if name:
                product['name'] = name

            category = input(f"Новая категория [{product['category']}]: ")
            if category:
                product['category'] = category

            supplier = input(f"Новый поставщик [{product['supplier']}]: ")
            if supplier:
                product['supplier'] = supplier

            price_input = input(f"Новая цена [{product['price']}]: ")
            if price_input:
                try:
                    product['price'] = float(price_input)
                except ValueError:
                    print("Ошибка: неверный формат цены.")

            quantity_input = input(f"Новое количество [{product['quantity']}]: ")
            if quantity_input:
                try:
                    product['quantity'] = int(quantity_input)
                except ValueError:
                    print("Ошибка: неверный формат количества.")

            print("Данные обновлены.")
            return

    print("Ошибка: товар не найден.")


def delete_product():
    view_products()
    try:
        product_id = int(input("Введите ID товара для удаления: "))
    except ValueError:
        print("Ошибка: введён некорректный ID.")
        return

    for index, product in enumerate(products):
        if product["id"] == product_id:
            removed = products.pop(index)
            print(f"Товар '{removed['name']}' удален.")
            return

    print("Ошибка: товар не найден.")