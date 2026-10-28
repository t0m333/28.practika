import tkinter as tk
from tkinter import ttk
import psycopg

def очистить_таблицу():
    for строка in таблица.get_children():
        таблица.delete(строка)

def показать_алканы():
    with psycopg.connect(
        dbname="organic_chemistry",
        user="postgres",
        password="Пароль", 
        host="localhost",
        port=5432,
        connect_timeout=5
    ) as соединение:
        with соединение.cursor() as курсор:
            курсор.execute("""
                SELECT name, formula, carbon_count
                FROM public.alkanes
                ORDER BY carbon_count ASC
            """)
            алканы = курсор.fetchall()

    очистить_таблицу()

    for алкан in алканы:
        название = алкан[0]
        формула = алкан[1]
        число_атомов = алкан[2]
        таблица.insert("", tk.END, values=(название, формула, число_атомов))

окно = tk.Tk()
окно.title("Алканы — органическая химия (из БД)")
окно.geometry("680x420")

надпись = ttk.Label(окно, text="Каталог алканов")
надпись.pack(pady=10)

кнопка_показать = ttk.Button(окно, text="Показать из БД", command=показать_алканы)
кнопка_показать.pack(pady=5)

кнопка_очистки = ttk.Button(окно, text="Очистить таблицу", command=очистить_таблицу)
кнопка_очистки.pack(pady=5)

таблица = ttk.Treeview(окно, columns=("name", "formula", "carbon_count"), show="headings", height=10)
таблица.heading("name", text="Название")
таблица.heading("formula", text="Формула")
таблица.heading("carbon_count", text="Атомов углерода")

таблица.column("name", width=220, anchor="w")
таблица.column("formula", width=160, anchor="center")
таблица.column("carbon_count", width=180, anchor="center")

таблица.pack(padx=15, pady=10, fill="both", expand=True)

окно.mainloop()
