import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename
import pandas as pd
from fpdf import FPDF
from datetime import datetime

class StorageApp:
    def __init__(self):
        # Основные данные приложения (вместо базы данных)
        self.products = [
            {"ID": "001", "Наименование": "Ноутбук Dell XPS 13", "Категория": "Электроника", 
             "Количество": 15, "Цена": 68999, "Мин. остаток": 5, "Последнее обновление": "14.05.2025"},
            {"ID": "002", "Наименование": "Монитор LG 27\"", "Категория": "Электроника", 
             "Количество": 8, "Цена": 24999, "Мин. остаток": 3, "Последнее обновление": "14.05.2025"},
            {"ID": "003", "Наименование": "Клавиатура Logitech", "Категория": "Периферия", 
             "Количество": 25, "Цена": 4999, "Мин. остаток": 10, "Последнее обновление": "14.05.2025"}
        ]
        
        self.current_id = 3  # Для генерации новых ID
        
        # Создаем главное окно входа
        self.create_login_window()

    def create_login_window(self):
        self.login_root = tk.Tk()
        self.login_root.title("Система управления складом")
        self.login_root.geometry("400x300")
        self.login_root.configure(bg="white")
        
        frame = tk.Frame(self.login_root, bg="white")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Иконка
        icon_label = tk.Label(frame, text="📦", font=("Arial", 36), bg="white")
        icon_label.pack(pady=10)
        
        # Заголовок
        title_label = tk.Label(frame, text="Система управления\nскладом", font=("Arial", 16), bg="white")
        title_label.pack(pady=10)
        
        # Поле для ввода логина
        login_label = tk.Label(frame, text="Логин", font=("Arial", 12), bg="white")
        login_label.pack(pady=5)
        self.login_entry = tk.Entry(frame, font=("Arial", 12), width=30)
        self.login_entry.pack(pady=5)
        
        # Поле для ввода пароля
        password_label = tk.Label(frame, text="Пароль", font=("Arial", 12), bg="white")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(frame, font=("Arial", 12), width=30, show="*")
        self.password_entry.pack(pady=5)
        
        # Кнопка "Войти"
        login_button = tk.Button(frame, text="Войти", font=("Arial", 14), bg="black", fg="white", 
                               command=self.login)
        login_button.pack(pady=10)
        
        self.login_root.mainloop()

    def login(self):
        username = self.login_entry.get()
        password = self.password_entry.get()
        
        if username == "admin" and password == "password":
            self.login_root.destroy()
            self.create_main_window()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

    def create_main_window(self):
        self.root = tk.Tk()
        self.root.title("Главное меню")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Верхняя панель с кнопками
        top_frame = tk.Frame(self.root, bg="#f0f0f0")
        top_frame.pack(pady=10)
        
        # Кнопки
        self.add_button = tk.Button(top_frame, text="+ Добавить", bg="black", fg="white", 
                                  font=("Arial", 12), command=self.open_add_product_window)
        self.add_button.grid(row=0, column=0, padx=5)
        
        self.edit_button = tk.Button(top_frame, text="📝 Редактировать", bg="gray", fg="white", 
                                   font=("Arial", 12), command=self.edit_product)
        self.edit_button.grid(row=0, column=1, padx=5)
        
        self.delete_button = tk.Button(top_frame, text="❌ Удалить", bg="gray", fg="white", 
                                    font=("Arial", 12), command=self.delete_product)
        self.delete_button.grid(row=0, column=2, padx=5)
        
        self.update_button = tk.Button(top_frame, text="🔄 Обновить", bg="gray", fg="white", 
                                     font=("Arial", 12), command=self.update_table)
        self.update_button.grid(row=0, column=3, padx=5)
        
        self.report_button = tk.Button(top_frame, text="📋 Сформировать отчет", bg="gray", fg="white", 
                                     font=("Arial", 12), command=self.open_report_window)
        self.report_button.grid(row=0, column=4, padx=5)
        
        # Пользовательская аватарка и колокольчик
        user_avatar = tk.Label(top_frame, text="👤", font=("Arial", 16), bg="#f0f0f0")
        user_avatar.grid(row=0, column=6, padx=10)
        
        bell_icon = tk.Label(top_frame, text="🔔", font=("Arial", 16), bg="#f0f0f0")
        bell_icon.grid(row=0, column=5, padx=10)
        
        # Таблица для отображения данных
        table_frame = tk.Frame(self.root, bg="#f0f0f0")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем таблицу с помощью Treeview
        self.columns = ("ID", "Наименование", "Категория", "Количество", "Цена", "Мин. остаток")
        self.tree = ttk.Treeview(table_frame, columns=self.columns, show="headings", selectmode="browse")
        
        # Настройка заголовков столбцов
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        
        # Добавляем полосу прокрутки
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Обновляем таблицу
        self.update_table()
        
        self.root.mainloop()

    def update_table(self):
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Добавляем данные
        for product in self.products:
            values = (
                product["ID"],
                product["Наименование"],
                product["Категория"],
                product["Количество"],
                f"{product['Цена']:,} ₽".replace(",", " "),
                product["Мин. остаток"]
            )
            self.tree.insert("", "end", values=values)

    def open_add_product_window(self, product=None):
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("Добавление продукта" if not product else "Редактирование продукта")
        self.add_window.geometry("400x400")
        self.add_window.configure(bg="white")
        
        # Заголовок
        title_text = "Добавить продукт" if not product else "Редактировать продукт"
        title_label = tk.Label(self.add_window, text=title_text, font=("Arial", 16), bg="white")
        title_label.pack(pady=10)
        
        # Поле для наименования
        name_label = tk.Label(self.add_window, text="Наименование", font=("Arial", 12), bg="white")
        name_label.pack(pady=5)
        self.name_entry = tk.Entry(self.add_window, font=("Arial", 12), width=30)
        self.name_entry.pack(pady=5)
        
        # Выбор категории
        category_label = tk.Label(self.add_window, text="Категория", font=("Arial", 12), bg="white")
        category_label.pack(pady=5)
        categories = ["Электроника", "Периферия", "Офисная техника", "Аксессуары"]
        self.category_combobox = ttk.Combobox(self.add_window, values=categories, font=("Arial", 12), width=27)
        self.category_combobox.set("Выберите категорию")
        self.category_combobox.pack(pady=5)
        
        # Поле для количества
        quantity_label = tk.Label(self.add_window, text="Количество", font=("Arial", 12), bg="white")
        quantity_label.pack(pady=5)
        self.quantity_entry = tk.Entry(self.add_window, font=("Arial", 12), width=30)
        self.quantity_entry.pack(pady=5)
        
        # Поле для цены
        price_label = tk.Label(self.add_window, text="Цена", font=("Arial", 12), bg="white")
        price_label.pack(pady=5)
        self.price_entry = tk.Entry(self.add_window, font=("Arial", 12), width=30)
        self.price_entry.pack(pady=5)
        
        # Поле для минимального остатка
        min_stock_label = tk.Label(self.add_window, text="Минимальный остаток", font=("Arial", 12), bg="white")
        min_stock_label.pack(pady=5)
        self.min_stock_entry = tk.Entry(self.add_window, font=("Arial", 12), width=30)
        self.min_stock_entry.pack(pady=5)
        
        # Если редактируем, заполняем поля
        if product:
            self.name_entry.insert(0, product["Наименование"])
            self.category_combobox.set(product["Категория"])
            self.quantity_entry.insert(0, str(product["Количество"]))
            self.price_entry.insert(0, str(product["Цена"]))
            self.min_stock_entry.insert(0, str(product["Мин. остаток"]))
            self.editing_id = product["ID"]
        else:
            self.editing_id = None
        
        # Кнопки
        button_frame = tk.Frame(self.add_window, bg="white")
        button_frame.pack(pady=10)
        
        save_text = "💾 Сохранить" if not product else "💾 Применить изменения"
        save_button = tk.Button(button_frame, text=save_text, font=("Arial", 12), bg="black", fg="white", 
                              command=lambda: self.save_product(product is not None))
        save_button.grid(row=0, column=0, padx=5)
        
        cancel_button = tk.Button(button_frame, text="❌ Отмена", font=("Arial", 12), bg="gray", fg="white", 
                                command=self.add_window.destroy)
        cancel_button.grid(row=0, column=1, padx=5)

    def save_product(self, is_edit=False):
        try:
            name = self.name_entry.get()
            category = self.category_combobox.get()
            quantity = int(self.quantity_entry.get())
            price = float(self.price_entry.get())
            min_stock = int(self.min_stock_entry.get())
            
            if not all([name, category]):
                raise ValueError("Заполните все поля")
            
            if quantity < 0 or price < 0 or min_stock < 0:
                raise ValueError("Значения не могут быть отрицательными")
            
            current_date = datetime.now().strftime("%d.%m.%Y")
            
            if is_edit:
                # Обновляем существующий продукт
                for product in self.products:
                    if product["ID"] == self.editing_id:
                        product.update({
                            "Наименование": name,
                            "Категория": category,
                            "Количество": quantity,
                            "Цена": price,
                            "Мин. остаток": min_stock,
                            "Последнее обновление": current_date
                        })
                        break
            else:
                # Добавляем новый продукт
                self.current_id += 1
                new_id = f"{self.current_id:03d}"
                self.products.append({
                    "ID": new_id,
                    "Наименование": name,
                    "Категория": category,
                    "Количество": quantity,
                    "Цена": price,
                    "Мин. остаток": min_stock,
                    "Последнее обновление": current_date
                })
            
            self.update_table()
            self.add_window.destroy()
            messagebox.showinfo("Успех", "Продукт успешно сохранен!")
            
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {str(e)}")

    def edit_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите продукт для редактирования")
            return
        
        item = self.tree.item(selected_item[0])
        product_id = item['values'][0]
        
        # Находим продукт в списке
        product_to_edit = None
        for product in self.products:
            if product["ID"] == product_id:
                product_to_edit = product
                break
        
        if product_to_edit:
            self.open_add_product_window(product_to_edit)

    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите продукт для удаления")
            return
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот продукт?"):
            item = self.tree.item(selected_item[0])
            product_id = item['values'][0]
            
            # Удаляем продукт из списка
            self.products = [p for p in self.products if p["ID"] != product_id]
            self.update_table()
            messagebox.showinfo("Успех", "Продукт успешно удален")

    def open_report_window(self):
        self.report_window = tk.Toplevel(self.root)
        self.report_window.title("Отчеты по товарам")
        self.report_window.geometry("900x700")
        self.report_window.configure(bg="#f0f0f0")
        
        # Верхняя панель с фильтрами
        filter_frame = tk.Frame(self.report_window, bg="#f0f0f0")
        filter_frame.pack(pady=10)
        
        # Фильтр: Пороговое количество
        threshold_label = tk.Label(filter_frame, text="Пороговое количество", font=("Arial", 12), bg="#f0f0f0")
        threshold_label.grid(row=0, column=0, padx=5, pady=5)
        self.threshold_entry = tk.Entry(filter_frame, font=("Arial", 12), width=15)
        self.threshold_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Фильтр: Категория
        category_label = tk.Label(filter_frame, text="Категория", font=("Arial", 12), bg="#f0f0f0")
        category_label.grid(row=0, column=2, padx=5, pady=5)
        categories = ["Все категории", "Электроника", "Периферия", "Офисная техника", "Аксессуары"]
        self.report_category_combobox = ttk.Combobox(filter_frame, values=categories, font=("Arial", 12), width=15)
        self.report_category_combobox.set("Все категории")
        self.report_category_combobox.grid(row=0, column=3, padx=5, pady=5)
        
        # Фильтр: Статус
        status_label = tk.Label(filter_frame, text="Статус", font=("Arial", 12), bg="#f0f0f0")
        status_label.grid(row=0, column=4, padx=5, pady=5)
        statuses = ["Все статусы", "Ниже порога", "В наличии", "Нет в наличии"]
        self.status_combobox = ttk.Combobox(filter_frame, values=statuses, font=("Arial", 12), width=15)
        self.status_combobox.set("Все статусы")
        self.status_combobox.grid(row=0, column=5, padx=5, pady=5)
        
        # Кнопка применить фильтры
        apply_button = tk.Button(filter_frame, text="Применить", font=("Arial", 12), bg="black", fg="white", 
                               command=self.apply_filters)
        apply_button.grid(row=0, column=6, padx=5, pady=5)
        
        # Таблица для отображения данных
        table_frame = tk.Frame(self.report_window, bg="#f0f0f0")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем таблицу с помощью Treeview
        report_columns = ("Товар", "Категория", "Количество", "Статус", "Последнее обновление")
        self.report_tree = ttk.Treeview(table_frame, columns=report_columns, show="headings")
        
        # Настройка заголовков столбцов
        for col in report_columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=150, anchor="center")
        
        # Добавляем полосу прокрутки
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.report_tree.yview)
        self.report_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.report_tree.pack(fill=tk.BOTH, expand=True)
        
        # Кнопки экспорта
        export_frame = tk.Frame(self.report_window, bg="#f0f0f0")
        export_frame.pack(pady=10)
        
        excel_button = tk.Button(export_frame, text="💾 Экспорт в Excel", bg="black", fg="white", 
                               font=("Arial", 12), command=self.export_to_excel)
        excel_button.pack(side="left", padx=5)
        
        pdf_button = tk.Button(export_frame, text="📄 Экспорт в PDF", bg="black", fg="white", 
                             font=("Arial", 12), command=self.export_to_pdf)
        pdf_button.pack(side="left", padx=5)
        
        # Применяем фильтры при открытии
        self.apply_filters()

    def apply_filters(self):
        # Очищаем таблицу
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        # Получаем значения фильтров
        threshold = self.threshold_entry.get()
        category = self.report_category_combobox.get()
        status = self.status_combobox.get()
        
        # Фильтруем данные
        filtered_data = []
        for product in self.products:
            # Определяем статус товара
            if product["Количество"] <= 0:
                product_status = "Нет в наличии"
            elif product["Количество"] < product["Мин. остаток"]:
                product_status = "Ниже порога"
            else:
                product_status = "В наличии"
            
            # Применяем фильтры
            include = True
            
            # Фильтр по пороговому количеству
            if threshold:
                try:
                    if product["Количество"] > int(threshold):
                        include = False
                except ValueError:
                    pass
            
            # Фильтр по категории
            if category != "Все категории" and product["Категория"] != category:
                include = False
                
            # Фильтр по статусу
            if status != "Все статусы" and product_status != status:
                include = False
                
            if include:
                filtered_data.append({
                    "Товар": product["Наименование"],
                    "Категория": product["Категория"],
                    "Количество": product["Количество"],
                    "Статус": product_status,
                    "Последнее обновление": product["Последнее обновление"]
                })
        
        # Добавляем данные в таблицу
        for item in filtered_data:
            self.report_tree.insert("", "end", values=(
                item["Товар"],
                item["Категория"],
                item["Количество"],
                item["Статус"],
                item["Последнее обновление"]
            ))

    def export_to_excel(self):
        # Собираем данные из таблицы отчета
        data = []
        for item in self.report_tree.get_children():
            values = self.report_tree.item(item)['values']
            data.append({
                "Товар": values[0],
                "Категория": values[1],
                "Количество": values[2],
                "Статус": values[3],
                "Последнее обновление": values[4]
            })
        
        if not data:
            messagebox.showwarning("Ошибка", "Нет данных для экспорта")
            return
        
        # Создаем DataFrame
        df = pd.DataFrame(data)
        
        # Предлагаем пользователю выбрать место сохранения
        file_path = asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Сохранить отчет как"
        )
        
        if file_path:
            try:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Успех", f"Данные успешно экспортированы в {file_path}")
            except Exception as e:
                messagebox.showwarning("Ошибка", "Нет данных для экспорта")
            return
        
        # Создаем DataFrame
        df = pd.DataFrame(data)
        
        # Предлагаем пользователю выбрать место сохранения
        file_path = asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Сохранить отчет как"
        )
        
        if file_path:
            try:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Успех", f"Данные успешно экспортированы в {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось экспортировать данные: {str(e)}")

    def export_to_pdf(self):
        # Собираем данные из таблицы отчета
        data = []
        for item in self.report_tree.get_children():
            values = self.report_tree.item(item)['values']
            data.append(values)
        
        if not data:
            messagebox.showwarning("Ошибка", "Нет данных для экспорта")
            return
        
        # Предлагаем пользователю выбрать место сохранения
        file_path = asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Сохранить отчет как"
        )
        
        if file_path:
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                
                # Заголовок отчета
                pdf.cell(200, 10, txt="Отчет по товарам на складе", ln=True, align='C')
                pdf.ln(10)
                
                # Дата генерации отчета
                pdf.set_font("Arial", size=10)
                pdf.cell(200, 10, txt=f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}", ln=True)
                pdf.ln(10)
                
                # Заголовки таблицы
                pdf.set_font("Arial", size=10, style='B')
                col_widths = [60, 40, 30, 40, 40]
                headers = ["Товар", "Категория", "Количество", "Статус", "Обновление"]
                
                for i, header in enumerate(headers):
                    pdf.cell(col_widths[i], 10, txt=header, border=1)
                pdf.ln()
                
                # Данные таблицы
                pdf.set_font("Arial", size=10)
                for row in data:
                    for i, item in enumerate(row):
                        pdf.cell(col_widths[i], 10, txt=str(item), border=1)
                    pdf.ln()
                
                # Сохраняем PDF
                pdf.output(file_path)
                messagebox.showinfo("Успех", f"Данные успешно экспортированы в {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось экспортировать данные: {str(e)}")

# Запуск приложения
if __name__ == "__main__":
    app = StorageApp()