from tkinter import *
import random


class Game:
    """The Game"""

    def __init__(self):
        self.stores = []
        self.year = 1
        self.global_actions = 10


class Store:
    """Store"""

    def __init__(self):
        self.employees = []
        self.productivity = 0

    def hire_employee(self, position):
        """"""
        employee = Employee()
        employee.setup(position)
        self.employees.append(employee)


class Employee:
    """Employee"""

    def __init__(self):
        self.position = None
        self.name = "John Doe"
        self.id = 0
        self.productivity = 0
        self.leadership = None
        self.salary = 0

    def setup(self, position):
        """"""
        info = self.position_database(position)

        self.position = position
        self.productivity = round((random.random() + 1)/2, 3)
        self.salary = info["Salary"]

        if info["Leadership"]:
            self.leadership = round((random.random() + 1)/2, 3)

    def position_database(self, position):
        pos_db = {"Sales Associate": {"Leadership": False, "Salary": 30000},
                  "Jr Manager": {"Leadership": True, "Salary": 45000},
                  "Sr Manager": {"Leadership": True, "Salary": 60000}}

        return pos_db[position]


def open_descript_win(position):
    descript_win = Toplevel(window_1)
    descript_win.geometry("600x400")

    if position == "Sales Associate":
        descript = Label(descript_win, text="Basic employee type. Each store requires at least 3 Sales Associates."
                                            "\n If there are fewer than three, 'overtime' is triggered."
                                            "\n Salary: $30000"
                                            "\n May be directly hired only")
    elif position == "Jr. Manager":
        descript = Label(descript_win, text="Basic employee type. Each store requires at least 3 Sales Associates."
                                            "\n If there are fewer than three, 'overtime' is triggered."
                                            "\n Salary: $45000"
                                            "\n May be directly hired or promoted from Sales Associate")

    descript.pack()


def open_employee_win():
    employee_win = Toplevel(window_1)
    employee_win.geometry("800x600")
    employee_win.title("View Employee Descriptions")
    bg = Canvas(employee_win, width=800, height=600)
    bg.pack()
    sal_ass = Button(bg, text="Sales Associate", command=lambda: open_descript_win("Sales Associate"))
    jr_man = Button(bg, text="Jr. Manager", command=lambda: open_descript_win("Jr. Manager"))
    sr_man = Button(bg, text="Sr. Manager")
    re_man = Button(bg, text="Regional Manager")
    ad_rep = Button(bg, text="Ad Rep")
    ad_man = Button(bg, text="Ad Manager")
    web_dev = Button(bg, text="Web Developer")
    web_man = Button(bg, text="Web Manager")
    sal_ass.place(x=100, y=100)
    jr_man.place(x=250, y=100)
    sr_man.place(x=400, y=100)
    re_man.place(x=550, y=100)
    ad_rep.place(x=400, y=150)
    ad_man.place(x=550, y=150)
    web_dev.place(x=400, y=200)
    web_man.place(x=550, y=200)


def open_rank_win():
    rank_win = Toplevel(window_1)
    rank_win.geometry("800x600")
    rank_win.title("View Rank")

    rank_example = Label(rank_win, text="Company            Percent Net Profit"
                                        "\n1. Nike              6.8%"
                                        "\n2. Addias            6.3%"
                                        "\n3. My Company        5.9%"
                                        "\n4. Reebok            5.7%"
                                        "\n.                    ."
                                        "\n.                    ."
                                        "\n.                    .")

    rank_example.pack()


window_1 = Tk()  # Tk is a class imported from tkinter that creates a blank window
window_1.title("Store Game")
window_1.geometry("1200x800")


def main():

    store_game = Game()

    rules_button = Button(window_1, text="View Basic Rules")
    employee_button = Button(window_1, text="View Employee Descriptions", command=open_employee_win)
    rank_button = Button(window_1, text="View Rank", command=open_rank_win)
    location_button = Button(window_1, text="Open a New Location")

    rules_button.pack(side=BOTTOM)
    employee_button.pack(side=BOTTOM)
    rank_button.pack(side=LEFT)
    location_button.pack(side=TOP)

    window_1.mainloop()


if __name__ == "__main__":
    main()
