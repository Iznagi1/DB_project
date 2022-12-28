from pathlib import Path
from procedures_db import *
from functools import partial
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import tkinter as tk



def get_revenue_callback(win, connection, output_entry):
    output_entry.delete(1.0, tk.END)
    revenue = round(calculate_revenue(connection), 2)
    output_entry.insert(tk.END, f"Выручка составила {revenue}")


def get_profit_callback(win, connection, output_entry):
    output_entry.delete(1.0, tk.END)
    profit = round(calculate_profit(connection), 2)
    output_entry.insert(tk.END, f"Прибыль составила {profit}")


def get_most_popular_dish_callback(win, connection, output_entry):
    output_entry.delete(1.0, tk.END)
    dish_name, order_count = find_most_popular_dish(connection)
    output_entry.insert(tk.END, f"Самое популярное блюдо {dish_name}, количество заказов {order_count}")


def add_waiter_callback(win, connection, entry):
    name = str(entry.get())
    print(name)
    add_waiter(connection, name)


def add_discount_callback(win, connection, entry):
    data = str(entry.get())
    data = data.split()
    discount_percentage = data[-1]
    data = data[:-1]
    string = ''
    for i in data:
        string += i + ' '
    string = string[:-1]

    print(data)
    if not discount_percentage.isdigit() and not (1 <= int(discount_percentage) <= 100):
        print(2)
        return
    if not all(x.isspace() or x.isalnum() for x in string):
        print(3)
        return
    print(string, discount_percentage)
    add_discount(connection, string, discount_percentage)


def get_most_valuable_waiter_callback(win, connection, output_entry):
    output_entry.delete(1.0, tk.END)
    max_name, max_amount, min_name, min_amount = find_most_valuable_waiter(connection)
    max_amount = round(max_amount, 2)
    min_amount = round(min_amount, 2)
    output_entry.insert(tk.END, f"Лучший официант {max_name}, приняв заказов на сумму {max_amount}\nХудший официант {min_name}, приняв заказов на сумму {min_amount}")


def get_most_unprofitable_discount_callback(win, connection, output_entry):
    output_entry.delete(1.0, tk.END)
    max_name, max_amount, min_name, min_amount = find_most_unprofitable_discount(connection)
    max_amount = round(max_amount, 2)
    min_amount = round(min_amount, 2)
    output_entry.insert(tk.END, f"Самая убыточная скидка {max_name}, убыток составил {max_amount}\nНаименее убыточная скидка {min_name}, убыток составил {min_amount}")


def get_most_popular_group_callback(win, connection, output_entry):
    output_entry.delete(1.0, tk.END)
    name, count = find_most_popular_group(connection)
    output_entry.insert(tk.END, f"Самая популярная группа {name}, количество заказов {count}")

def create_gui(connection):

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"/home/izanagi/PycharmProjects/DB_project/assets/frame0")


    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)


    window = Tk()

    window.geometry("1440x1024")
    window.configure(bg = "#FFFFFF")


    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 1024,
        width = 1440,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        720.0,
        512.0,
        image=image_image_1
    )

    canvas.create_text(
        246.0,
        33.0,
        anchor="nw",
        text="Cafe manager Lite",
        fill="#FFFFFF",
        font=("Inter Bold", 64 * -1)
    )

    canvas.create_rectangle(
        881.0,
        185.0,
        1327.0,
        333.0,
        fill="#FF0089",
        outline="")

    canvas.create_rectangle(
        881.0,
        377.0,
        1327.0,
        525.0,
        fill="#FF0089",
        outline="")

    canvas.create_rectangle(
        99.0,
        377.0,
        549.0,
        525.0,
        fill="#FF0089",
        outline="")

    canvas.create_rectangle(
        99.0,
        185.0,
        549.0,
        333.0,
        fill="#FF0089",
        outline="")

    canvas.create_rectangle(
        99.0,
        569.0,
        549.0,
        717.0,
        fill="#FF0089",
        outline="")

    canvas.create_rectangle(
        99.0,
        761.0,
        549.0,
        909.0,
        fill="#FF0089",
        outline="")

    canvas.create_rectangle(
        881.0,
        569.0,
        1327.0,
        717.0,
        fill="#FF0089",
        outline="")

    canvas.create_rectangle(
        881.0,
        761.0,
        1327.0,
        909.0,
        fill="#FF0089",
        outline="")

    entry_image_1 = PhotoImage(
        file=relative_to_assets("add_waiter_entry.png"))
    entry_bg_1 = canvas.create_image(
        1105.5,
        227.0,
        image=entry_image_1
    )
    add_waiter_entry = Entry(
        bd=0,
        bg="#FD85C6",
        fg="#000716",
        highlightthickness=0
    )
    add_waiter_entry.place(
        x=919.0,
        y=207.0,
        width=373.0,
        height=38.0
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("add_discount_entry.png"))
    entry_bg_2 = canvas.create_image(
        1105.5,
        413.0,
        image=entry_image_2
    )
    add_discount_entry = Entry(
        bd=0,
        bg="#FD85C6",
        fg="#000716",
        highlightthickness=0
    )
    add_discount_entry.place(
        x=919.0,
        y=393.0,
        width=373.0,
        height=38.0
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("unprofitable_discount.png"))
    entry_bg_3 = canvas.create_image(
        1104.0,
        866.0,
        image=entry_image_3
    )
    unprofitable_discount_entry = Text(
        font="Bfree 12",
        padx=10,
        wrap=tk.WORD,
        bd=0,
        bg="#FF0089",
        fg="#000716",
        highlightthickness=0
    )
    unprofitable_discount_entry.place(
        x=886.0,
        y=829.0,
        width=436.0,
        height=72.0
    )

    entry_image_4 = PhotoImage(
        file=relative_to_assets("calculate_profit_entry.png"))
    entry_bg_4 = canvas.create_image(
        324.0,
        485.0,
        image=entry_image_4
    )
    calculate_profit_entry = Text(
        font="Bfree 12",
        padx=10,
        wrap=tk.WORD,
        bd=0,
        bg="#FF0089",
        fg="#000716",
        highlightthickness=0
    )
    calculate_profit_entry.place(
        x=105.0,
        y=448.0,
        width=438.0,
        height=72.0
    )

    entry_image_5 = PhotoImage(
        file=relative_to_assets("valuable_waiter_entry.png"))
    entry_bg_5 = canvas.create_image(
        1104.0,
        674.0,
        image=entry_image_5
    )
    valuable_waiter_entry = Text(
        font="Bfree 12",
        padx=10,
        wrap=tk.WORD,
        bd=0,
        bg="#FF0089",
        fg="#000716",
        highlightthickness=0
    )
    valuable_waiter_entry.place(
        x=886.0,
        y=637.0,
        width=436.0,
        height=72.0
    )

    entry_image_6 = PhotoImage(
        file=relative_to_assets("popular_dish_entry.png"))
    entry_bg_6 = canvas.create_image(
        324.0,
        674.0,
        image=entry_image_6
    )
    popular_dish_entry = Text(
        font="Bfree 12",
        padx=10,
        wrap=tk.WORD,
        bd=0,
        bg="#FF0089",
        fg="#000716",
        highlightthickness=0
    )
    popular_dish_entry.place(
        x=105.0,
        y=637.0,
        width=438.0,
        height=72.0
    )

    entry_image_7 = PhotoImage(
        file=relative_to_assets("calculate_revenue_entry.png"))
    entry_bg_7 = canvas.create_image(
        324.0,
        291.0,
        image=entry_image_7
    )
    calculate_revenue_entry = Text(
        font="Bfree 12",
        padx=10,
        wrap=tk.WORD,
        bd=0,
        bg="#FF0089",
        fg="#000716",
        highlightthickness=0
    )
    calculate_revenue_entry.place(
        x=105.0,
        y=254.0,
        width=438.0,
        height=72.0
    )

    entry_image_8 = PhotoImage(
        file=relative_to_assets("popular_group_entry.png"))
    entry_bg_8 = canvas.create_image(
        324.0,
        866.0,
        image=entry_image_8
    )
    popular_group_entry = Text(
        font="Bfree 12",
        padx=10,
        wrap=tk.WORD,
        bd=0,
        bg="#FF0089",
        fg="#000716",
        highlightthickness=0
    )
    popular_group_entry.place(
        x=105.0,
        y=829.0,
        width=438.0,
        height=72.0
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("calculate_revenue.png"))
    calculate_revenue_button = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=partial(get_revenue_callback, window, connection, calculate_revenue_entry),
        relief="flat"
    )
    calculate_revenue_button.place(
        x=211.0,
        y=198.0,
        width=226.0,
        height=49.0
    )


    button_image_2 = PhotoImage(
        file=relative_to_assets("popular_dish.png"))
    popular_dish_button = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=partial(get_most_popular_dish_callback, window, connection, popular_dish_entry),
        relief="flat"
    )
    popular_dish_button.place(
        x=211.0,
        y=581.0,
        width=226.0,
        height=49.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("add_discount.png"))
    add_discount_button = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=partial(add_discount_callback, window, connection, add_discount_entry),
        relief="flat"
    )
    add_discount_button.place(
        x=991.0,
        y=449.0,
        width=226.0,
        height=49.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("calculate_profit.png"))
    calculate_profit_button = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=partial(get_profit_callback, window, connection, calculate_profit_entry),
        relief="flat"
    )
    calculate_profit_button.place(
        x=211.0,
        y=389.0,
        width=226.0,
        height=49.0
    )

    button_image_5 = PhotoImage(
        file=relative_to_assets("valuable_waiter.png"))
    valuable_waiter_button = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=partial(get_most_valuable_waiter_callback, window, connection, valuable_waiter_entry),
        relief="flat"
    )
    valuable_waiter_button.place(
        x=991.0,
        y=581.0,
        width=226.0,
        height=49.0
    )

    button_image_6 = PhotoImage(
        file=relative_to_assets("unprofitable_discount.png"))
    unprofitable_discount_button = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=partial(get_most_unprofitable_discount_callback, window, connection, unprofitable_discount_entry),
        relief="flat"
    )
    unprofitable_discount_button.place(
        x=991.0,
        y=773.0,
        width=226.0,
        height=49.0
    )

    button_image_7 = PhotoImage(
        file=relative_to_assets("popular_group.png"))
    popular_group_button = Button(
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=partial(get_most_popular_group_callback, window, connection, popular_group_entry),
        relief="flat"
    )
    popular_group_button.place(
        x=211.0,
        y=773.0,
        width=226.0,
        height=49.0
    )

    button_image_8 = PhotoImage(
        file=relative_to_assets("add_waiter.png"))
    add_waiter_button = Button(
        image=button_image_8,
        borderwidth=0,
        highlightthickness=0,
        command=partial(add_waiter_callback, window, connection, add_waiter_entry),
        relief="flat"
    )
    add_waiter_button.place(
        x=991.0,
        y=263.0,
        width=226.0,
        height=49.0
    )


    window.resizable(False, False)
    window.mainloop()
