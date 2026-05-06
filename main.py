import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
from datetime import datetime

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("600x500")

        self.history = []
        self.load_history()

        # Ползунок длины пароля
        tk.Label(root, text="Длина пароля (4–30):").pack(pady=5)
        self.length_var = tk.IntVar(value=12)
        self.length_slider = ttk.Scale(
            root, from_=4, to=30, orient='horizontal',
            variable=self.length_var
        )
        self.length_slider.pack(pady=5, fill='x', padx=20)

        # Отображение текущей длины
        self.length_label = tk.Label(root, text="12 символов")
        self.length_label.pack(pady=2)

        self.length_var.trace('w', self.update_length_label)

        # Чекбоксы для выбора символов
        self.use_letters = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)

        tk.Checkbutton(root, text="Буквы (a‑z, A‑Z)",
                       variable=self.use_letters).pack(anchor='w', padx=20)
        tk.Checkbutton(root, text="Цифры (0‑9)",
                       variable=self.use_digits).pack(anchor='w', padx=20)
        tk.Checkbutton(root, text="Спецсимволы (!@#$%)",
                       variable=self.use_special).pack(anchor='w', padx=20)

        # Кнопка генерации
        tk.Button(root, text="Сгенерировать пароль",
                  command=self.generate_password, bg='green', fg='white').pack(pady=10)

        # Поле отображения пароля
        self.password_var = tk.StringVar()
        tk.Entry(root, textvariable=self.password_var,
                font=('Arial', 12), justify='center').pack(
            pady=5, fill='x', padx=20
        )

        # Таблица истории
        tk.Label(root, text="История паролей:").pack(pady=(20, 5))
        columns = ('Password', 'Length', 'Date')
        self.tree = ttk.Treeview(root, columns=columns, show='headings', height=8)
        self.tree.heading('Password', text='Пароль')
        self.tree.heading('Length', text='Длина')
        self.tree.heading('Date', text='Дата и время')
        self.tree.column('Password', width=200)
        self.tree.column('Length', width=80)
        self.tree.column('Date', width=180)
        self.tree.pack(pady=5, padx=20, fill='both', expand=True)

        self.update_history_table()

    def update_length_label(self, *args):
        length = self.length_var.get()
        self.length_label.config(text=f"{length} символов")

    def generate_password(self):
        length = self.length_var.get()

        # Проверка минимальной длины
        if length < 4:
            messagebox.showerror("Ошибка", "Минимальная длина пароля — 4 символа")
            return

        # Формирование набора символов
        chars = ""
        if self.use_letters.get():
            chars += string.ascii_letters
        if self.use_digits.get():
            chars += string.digits
        if self.use_special.get():
            chars += "!@#$%^&*()"

        # Проверка, что хотя бы один тип символов выбран
        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
            return

        # Генерация пароля
        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_var.set(password)

        # Добавление в историю
        entry = {
            'password': password,
            'length': length,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.history.append(entry)
        self.save_history()
        self.update_history_table()

    def update_history_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entry in reversed(self.history[-50:]):  # Последние 50 записей
            self.tree.insert('', 'end', values=(
                entry['password'],
                entry['length'],
                entry['date']
            ))

    def save_history(self):
        with open('password_history.json', 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        try:
            with open('password_history.json', 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
