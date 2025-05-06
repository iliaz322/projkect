# main.py
from product_manager import add_product, view_products, edit_product, delete_product
from inventory_checker import check_low_stock, set_threshold
from storage import save_data, load_data


def main_menu():
    print("\n=== Система учёта продуктов на складе ===")
    print("1. Добавить товар")
    print("2. Просмотреть товары")
    print("3. Редактировать товар")
    print("4. Удалить товар")
    print("5. Проверить остатки")
    print("6. Установить порог уведомления")
    print("7. Сохранить данные")
    print("8. Загрузить данные")
    print("9. Выход")


def run_app():
    while True:
        main_menu()
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
            check_low_stock()
        elif choice == "6":
            try:
                threshold = int(input("Введите пороговое значение: "))
                set_threshold(threshold)
            except ValueError:
                print("Ошибка: введите число.")
        elif choice == "7":
            save_data()
        elif choice == "8":
            load_data()
        elif choice == "9":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    run_app()