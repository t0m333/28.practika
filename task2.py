import tkinter as tk
from tkinter import ttk
import psycopg

# очистка таблицы
def clear_tab():
    for i in tab.get_children():
        tab.delete(i)

def show_data():
    # коннект к базе алкенов
    conn = psycopg.connect(
        dbname="alkenes_task2",
        user="postgres",
        password="Admin", # пароль
        host="localhost",
        port=5432
    )
    
    cur = conn.cursor()
    cur.execute("SELECT name, formula, carbon_count, hydrogen_count, molar_mass FROM public.alkenes ORDER BY carbon_count ASC")
    rows = cur.fetchall()
    
    cur.close()
    conn.close()

    # чистим чтобы не было дублей при повторном нажатии
    clear_tab()

    # цикл для заполнения таблицы
    for r in rows:
        n = r[0]
        f = r[1]
        c = r[2]
        h = r[3]
        m = r[4]
        tab.insert("", tk.END, values=(n, f, c, h, m))


root = tk.Tk()
root.title("Задание 2")
root.geometry("800x350")

# надпись
lbl = ttk.Label(root, text="Каталог: Алкены")
lbl.pack(pady=5)

# кнопки
btn1 = ttk.Button(root, text="Показать", command=show_data)
btn1.pack(pady=5)

btn2 = ttk.Button(root, text="Очистить таблицу", command=clear_tab)
btn2.pack(pady=5)

# фрейм для таблицы и скролла
f1 = ttk.Frame(root)
f1.pack(padx=10, pady=10, fill="x", expand=False)

# таблица height=3
tab = ttk.Treeview(f1, columns=("c1", "c2", "c3", "c4", "c5"), show="headings", height=3)

# заголовки
tab.heading("c1", text="Название")
tab.heading("c2", text="Формула")
tab.heading("c3", text="Атомов C")
tab.heading("c4", text="Атомов H")
tab.heading("c5", text="Масса, г/моль")

# ширину колонок настроил
tab.column("c1", width=150, anchor="w")
tab.column("c2", width=100, anchor="center")
tab.column("c3", width=80, anchor="center")
tab.column("c4", width=80, anchor="center")
tab.column("c5", width=100, anchor="center")

# скролл
scroll = ttk.Scrollbar(f1, orient="vertical", command=tab.yview)
tab.configure(yscrollcommand=scroll.set)

tab.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

root.mainloop()