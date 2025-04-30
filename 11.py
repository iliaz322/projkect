products = []
next_id = 1


def add_product():
    global next_id
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
        "id": next_id,
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


def module_menu():
    while True:
        print("=== Модуль управления товарами ===")
        print("1. Добавить товар")
        print("2. Просмотреть товары")
        print("3. Редактировать товар")
        print("4. Удалить товар")
        print("5. Вернуться в главное меню")

        choice = input("Выберите действие: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            edit_product()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    module_menu()