from tkinter import *
from tkinter.messagebox import askyesno
import random
import get_test     # Used to pull from webscraper

# The following pulls data from the scrapper once when the game is started.
stores = ['adidas', 'asics', 'athleta', 'callaway', 'canterbury', 'lululemon athletica', 'nike', 'puma',
          'sondico', 'under armour']
count = 1
store_data = {}
rank_string = ''
for store in stores:
    net_income_percent = round((get_test.get_info(store)[0][2]/sum(get_test.get_info(store)[0]))*100, 1)
    store_data[store] = net_income_percent

store_data = sorted(store_data.items(), key=lambda x: x[1], reverse=True)

for store in store_data:
    rank_string += str(count) + ". " + store[0] + ': ' + str(store[1]) + "%\n"
    count += 1
#   #   #   #

MIN_ASSOCIATES = 3

window_1 = Tk()  # Tk is a class imported from tkinter that creates a blank window
window_1.title("Store Game")
window_1.geometry("1200x800")

global_actions_label = Label()
notice_label = Label(window_1, text='')


class Game:
    """The Game"""

    def __init__(self):
        self.stores = {}
        self.year = 1
        self.global_actions = 10

    def open_store(self):
        """"""
        if store_game.global_actions >= 5:
            store = Store()
            store.setup()
            store.id = len(self.stores) + 1
            self.stores[store.id] = store
            create_store_button(store.id)
        else:
            notice_label.config(text="NOTICE: Not enough actions. Minimum: 5 global actions.")


class Store:
    """Store"""

    def __init__(self):
        self.employees = {}
        self.productivity = 0
        self.id = 0
        self.local_actions = 0
        self.evaluations = False

    def hire_employee(self, position):
        """Add an Employee object to the employees dictionary. id is the key and employee object is the value.
        Note: employee id is not globally unique, but it is unique per store."""
        if store_game.global_actions > 0 or self.local_actions > 0:
            employee = Employee()
            employee.setup(position)
            employee.id = len(self.employees) + 1
            self.employees[employee.id] = employee
            self.calc_productivity()

            if self.local_actions > 0:
                self.local_actions -= 1
            else:
                store_game.global_actions -= 1
                global_actions_label.config(text="Global actions remaining: " + str(store_game.global_actions))
        else:
            notice_label.config(text="NOTICE: No more actions remaining.")

    def calc_productivity(self):
        """Update store productivity. It is a sum of all the employee productivities in the store."""
        productivity = 0
        for eid, employee in self.employees.items():
            productivity += employee.productivity
        self.productivity = round(productivity, 2)

    def setup(self):
        """Setup a new store. It must start with three Sales Associates and a Jr. Manager."""

        for i in range(0, MIN_ASSOCIATES):
            self.hire_employee("Sales Associate")
        self.hire_employee("Jr Manager")
        store_game.global_actions -= 1
        global_actions_label.config(text="Global actions remaining: " + str(store_game.global_actions))
        self.local_actions += 1

    def run_evaluations(self, store_win, store_id):
        """"""
        response = open_confirm_win("Are you sure you want to run employee evaluations? Doing so will use one action.")

        if response is True:
            if (store_game.global_actions > 0 or self.local_actions > 0) and self.evaluations is False:
                self.evaluations = True
                if self.local_actions > 0:
                    self.local_actions -= 1
                else:
                    store_game.global_actions -= 1
                    global_actions_label.config(text="Global actions remaining: " + str(store_game.global_actions))
                store_win.destroy()
                open_store_win(store_id)
            elif self.evaluations is True:
                notice_label.config(text="NOTICE: Already ran employee evaluations for this store.")
            else:
                notice_label.config(text="NOTICE: No more actions remaining")
        else:
            return


class Employee:
    """Employee"""

    def __init__(self):
        self.position = None
        self.name = "John Doe"
        self.id = 0
        self.productivity = 0
        self.leadership = None
        self.salary = 0
        self.pos_db = {"Sales Associate": {"Leadership": False, "Salary": 30000},
                       "Jr Manager": {"Leadership": True, "Salary": 45000},
                       "Sr Manager": {"Leadership": True, "Salary": 60000}}

    def setup(self, position):
        """"""
        info = self.pos_db[position]

        self.position = position
        self.productivity = round((random.random() + 1)/2, 2)
        self.salary = info["Salary"]

        if info["Leadership"]:
            self.leadership = round((random.random() + 1)/2, 2)


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

    # rank_string data comes from scraper an it calculated during startup
    rank_example = Label(rank_win, text=rank_string)

    rank_example.pack()


def create_store_button(sid):
    store_button = Button(window_1, text="Store " + str(sid), command=lambda: open_store_win(sid))
    store_button.pack()


def open_store_win(store_id):
    store_win = Toplevel(window_1)
    store_win.geometry("800x600")
    store_win.title("Store " + str(store_id))
    store = store_game.stores[store_id]
    employees = store.employees
    employee_info = ""
    for eid, employee in employees.items():
        employee_info += "Name: " + employee.name
        employee_info += "  Position: " + employee.position + "\n"
        if store.evaluations:
            employee_info += "      Productivity: " + str(employee.productivity) + "\n"
    store_info = Label(store_win, text="Store Productivity " + str(store.productivity) + "\n"
                       + employee_info)
    action_label = Label(store_win, text="Local actions remaining: " + str(store.local_actions))
    run_evals_button = Button(store_win, text="Run Employee Evaluations",
                              command=lambda: store.run_evaluations(store_win, store_id))
    store_info.pack()
    run_evals_button.pack(side=BOTTOM)
    action_label.pack(side=BOTTOM)


def open_confirm_win(message):
    response = askyesno(title="Confirmation", message=message)


    # wait = IntVar()
    #
    # confirm_win = Toplevel(window_1)
    # confirm_win.geometry("300x200")
    # confirm_win.title("Confirmation")
    # confirm_mess = Label(confirm_win, text=message)
    # confirm_mess.pack()
    #
    # no = Button(confirm_win, text="No", command=confirm_win.destroy)
    # yes = Button(confirm_win, text="Yes", command=lambda: wait.set(1))
    # no.pack(side=BOTTOM)
    # yes.pack(side=BOTTOM)
    #
    # yes.wait_variable(wait)
    return response


store_game = Game()

rules_button = Button(window_1, text="View Basic Rules")
employee_button = Button(window_1, text="View Employee Descriptions", command=open_employee_win)
rank_button = Button(window_1, text="View Rank", command=open_rank_win)
location_button = Button(window_1, text="Open a New Location", command=store_game.open_store)
global_actions_label = Label(window_1, text="Global actions remaining: " + str(store_game.global_actions))

rules_button.pack(side=BOTTOM)
employee_button.pack(side=BOTTOM)
global_actions_label.pack(side=BOTTOM)
rank_button.pack(side=LEFT)
location_button.pack(side=TOP)
notice_label.pack(side=BOTTOM)

store_game.open_store()

window_1.mainloop()


# if __name__ == "__main__":
#     main()
