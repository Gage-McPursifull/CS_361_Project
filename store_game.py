from tkinter import *
from tkinter.messagebox import askyesno
from tkinter import messagebox
import random
import name_gen

import get_test     # Used to pull from webscraper

# The following pulls data from the scrapper once when the game is started.
companies = ['adidas', 'asics', 'athleta', 'callaway', 'canterbury', 'lululemon athletica', 'nike', 'puma',
             'sondico', 'under armour']
store_data = {}
for company in companies:
    company_info = get_test.get_info(company)
    net_income_percent = round((company_info[0][2]/sum(company_info[0]))*100, 1)
    store_data[company] = sum(company_info[0])


MIN_ASSOCIATES = 3

window_1 = Tk()  # Tk is a class imported from tkinter that creates a blank window
window_1.title("Store Game")
window_1.geometry("1200x800")

global_actions_label = Label(window_1)
notice_label = Label(window_1, text='')


class Game:
    """The Game"""
    def __init__(self):
        self.stores = {}            # key - store id, value - store class objects
        self.year = 1               # year indicates round number. Game ends at year 10
        self.global_actions = 11
        self.year_gross_income = 0
        self.year_net_income = 0
        self.percent_net_income = 0

    def open_store(self):
        """A method that is called when a player clicks "Open a New Location". Also called when game is initialized."""
        if self.check_management() is False:
            notice_label.config(text="NOTICE: Must have a Sr Manager at every store before opening a new store.")
            return

        if store_game.global_actions >= 5:
            store = Store()
            store.setup()
            store.id = len(self.stores) + 1
            self.stores[store.id] = store
            create_store_button(store.id)
        else:
            notice_label.config(text="NOTICE: Not enough actions. Minimum: 5 global actions.")

    def check_management(self):
        """Checks all stores to see if there is a Sr Manager at each one. Return True if so, False otherwise."""
        manager = False

        for sid, store in self.stores.items():
            for eid, employee in store.employees.items():
                if employee.position == "Sr Manager":
                    manager = True
            if manager is False:
                return False
            else:
                manager = False

        return True

    def calc_income(self):
        """Calculate net and gross income for each store to find cumulative total."""
        self.year_gross_income = 0
        self.year_net_income = 0

        for sid, store in self.stores.items():
            if store.productivity <= 2.75:
                weight = 2
            elif 2.75 < store.productivity <= 4:
                weight = 1.2
            else:
                weight = 1
            store.year_gross_income = round((store.productivity * 55000)/weight, 0)
            store.year_net_income = round(store.year_gross_income - store.sum_employee_salary(), 0)
            store.calc_percent_net_income()
            self.year_gross_income += store.year_gross_income
            round(self.year_gross_income)
            self.year_net_income += store.year_net_income
        if self.year_gross_income != 0:
            self.percent_net_income = round(((self.year_net_income / self.year_gross_income) * 100), 1)

    def calc_rank(self, rank_data):
        """Calculates percent net income for a player's chain of stores. Rank is determined against real sporting good
        companies."""

        rank_string = ""
        count = 1
        rank_data["My Company"] = self.year_gross_income

        rank_data = sorted(rank_data.items(), key=lambda x: x[1], reverse=True)

        for store in rank_data:
            rank_string += str(count) + ". " + store[0] + ': $' + str(store[1]) + "\n"
            count += 1

        return rank_string

    def update_employees(self):
        """Called at the end of each year after rank is calculated. Employees who don't quit have their productivity
        updated. Quitting probabilities: Sales Associate - 50%, Jr. Manager - 20%, Sr. Manager - 10%."""

        quit_string = "Employees who quit: \n"

        for sid, store in self.stores.items():
            for eid, employee in store.employees.copy().items():
                det_quit = random.random()      # determine quit - random float between 0 and 1.
                # If det_quit is within the quit threshold, the employee is removed from its store.
                # Otherwise, their productivity is updated by up to +/- .1
                if 1 - det_quit < employee.quit_prob:
                    quit_string += "Store " + str(sid) + ": " + employee.name + " " + employee.position + "\n"
                    del store.employees[eid]
                elif employee.position != "Sr Manager":
                    if random.random() < .5:
                        employee.productivity += random.random()/10
                    else:
                        employee.productivity -= random.random()/10
                    employee.productivity = round(min(employee.productivity, 1), 2)

        return quit_string

    def update_stores(self):
        """Reset global_actions and all local_actions, reset evaluations, recalculate stores' productivities.
        global_actions will be 2 more than previous year and local_actions will be equal to number of managers in that
        store."""

        for sid, store in self.stores.items():
            store.calc_productivity()
            store.local_actions = 0
            store.evaluations = False
            for eid, employee in store.employees.items():
                if employee.leadership:
                    store.local_actions += 1

        self.global_actions = 6 + (self.year * 2)

    def go_to_next_year(self):
        """Calls on many functions to reset parameters and go to the next year in the game."""
        response = open_confirm_win("Are you sure you want to go to the next year? Doing so will cause any remaining "
                                    "actions to go unused.")
        if response is True:
            self.calc_income()
            news = self.update_employees()
            self.update_stores()
            self.year += 1
            self.check_bankrupt()
            self.check_game_end()
            year_label.config(text="Year: " + str(self.year) + " of 10")
            global_actions_label.config(text="Global actions remaining: " + str(store_game.global_actions))
            open_news_win(news)

    def check_bankrupt(self):
        """If percent net income drops below 0, the game is over."""
        if self.percent_net_income < 0:
            messagebox.showinfo("Bankrupt", "Your percent net income dropped below 0. Game Over.")
            window_1.destroy()

    def check_game_end(self):
        """"""
        if self.year == 11:
            messagebox.showinfo("Congratulations!", "You made it to year 10! Check your rank to see how you did.")


class Store:
    """Respresents a store. Contains employees which contribute to the store's stats."""
    def __init__(self):
        self.employees = {}         # key - employee id, value - employee class objects
        self.productivity = 0       # equal to the sum of all employee productivities
        self.id = 0                 # Store id
        self.local_actions = 0      # Jr and Sr managers add to local_actions. Used only for actions at this store
        self.evaluations = False
        self.year_gross_income = 0
        self.year_net_income = 0
        self.percent_net_income = 0.0
        self.employee_id = 1        # Assigned to a hired employee, then incremented

    def setup(self):
        """Setup a new store. Called by Game.open_store"""

        # Stores must start with "MIN_ASSOCIATES" Sales Associates and one Jr. Manager
        for i in range(0, MIN_ASSOCIATES):
            self.hire_employee("Sales Associate")
        self.hire_employee("Jr Manager")

        use_global_action()

    def hire_employee(self, position):
        """Add an Employee object to employees dictionary. Method called when player clicks "Hire" from store window.
        Note: employee id is not globally unique, but it is unique per store."""

        # Checks that a player isn't trying to hire too many jr/sr managers
        if self.check_manager_thresh(position) is False:
            return

        if store_game.global_actions > 0 or self.local_actions > 0:
            employee = Employee()
            employee.setup(position)                # position attributes are defined in Employee.pos_db
            employee.id = self.employee_id
            self.employees[self.employee_id] = employee
            self.employee_id += 1
            self.calc_productivity()

            self.use_action()

            if employee.leadership is not None:     # Jr and Sr managers have leadership
                self.local_actions += 1
        else:
            notice_label.config(text="NOTICE: Cannot hire employee. No more actions remaining.")

    def check_manager_thresh(self, position):
        """Stores may have a maximum of 2 Jr and 1 Sr Manager. Method checks to see if those metrics are exceeded."""
        jr = 0
        sr = 0
        for eid, employee in self.employees.items():
            if employee.position == "Jr Manager":
                jr += 1
            if employee.position == "Sr Manager":
                sr += 1

        if position == "Jr Manager" and jr == 2:
            notice_label.config(text="NOTICE: This store already has two Jr Managers.")
            return False
        elif position == "Sr Manager" and sr == 1:
            notice_label.config(text="NOTICE: This store already has one Sr Manager.")
            return False

        return True

    def confirm_hire(self, position, hire_win, store_win, store_id):
        """Called when player tries to hire employee.
        Calls open_confirm_win to confirm that the specified employee should be hired."""
        response = open_confirm_win("Are you sure you want to hire a " + position + "? Doing so will use one action.")

        if response is True:
            hire_win.destroy()
            self.hire_employee(position)
            store_win_refresh(store_win, store_id)

    def run_evaluations(self, store_win, store_id):
        """Method called when player clicks "Run Employee Evaluations". Makes each employee's productivity visible."""

        # response will be True or False depending on player selection
        response = open_confirm_win("Are you sure you want to run employee evaluations? Doing so will use one action.")

        if response is True:
            if (store_game.global_actions > 0 or self.local_actions > 0) and self.evaluations is False:
                self.evaluations = True
                self.use_action()
                store_win_refresh(store_win, store_id)

            elif self.evaluations is True:
                notice_label.config(text="NOTICE: Already ran employee evaluations for this store.")

            else:
                notice_label.config(text="NOTICE: No more actions remaining")

    def fire_employee(self, eid, store_win, store_id):
        """Called when a player tries to fire an employee. Removes Employee object from self.employees"""
        response = open_confirm_win("Are you sure you want to fire " + self.employees[eid].name +
                                    "? Doing so will use one action.")

        if response is True:
            if store_game.global_actions > 0 or self.local_actions > 0:
                del self.employees[eid]
                self.calc_productivity()
                self.use_action()
                store_win_refresh(store_win, store_id)
            else:
                notice_label.config(text="NOTICE: Cannot fire employee. No more actions remaining.")

    def calc_productivity(self):
        """Update store productivity. It is a sum of all the employee productivities in the store. Cannot exceed 5."""
        productivity = 0
        for eid, employee in self.employees.items():
            productivity += employee.productivity
        self.productivity = min(round(productivity, 2), 5)  # if productivity > 5, it instead equals 5.

    def calc_percent_net_income(self):
        """Calcuate percent net income for this store."""
        if self.year_gross_income != 0:
            self.percent_net_income = round(((self.year_net_income / self.year_gross_income) * 100), 1)

    def sum_employee_salary(self):
        """Add all employee salaries for this store. Called by Game.calc_income at the end of each year."""
        total_salary = 0

        for eid, employee in self.employees.items():
            total_salary += employee.salary

        return total_salary

    def use_action(self):
        """Uses a local action if available. Otherwise, uses a global action."""
        if self.local_actions > 0:
            self.local_actions -= 1
        else:
            use_global_action()


class Employee:
    """Represents an employee. Employees may be assigned to stores."""

    def __init__(self):
        self.position = None
        self.name = None
        self.id = 0
        self.productivity = 0
        self.leadership = None
        self.salary = 0
        self.quit_prob = 0
        self.pos_db = {"Sales Associate": {"Leadership": False, "Salary": 30000, "Quit": .30},
                       "Jr Manager": {"Leadership": True, "Salary": 45000, "Quit": .18},
                       "Sr Manager": {"Leadership": True, "Salary": 60000, "Quit": .10}}

    def setup(self, position):
        """Called by Store.hire_employee. Define employee stats based on "position"."""
        self.position = position
        self.quit_prob = self.pos_db[position]["Quit"]

        # Sr Managers do not contribute to productivity
        if position != "Sr Manager":
            self.productivity = round((random.random() + 1)/2, 2)
        self.salary = self.pos_db[position]["Salary"]

        if self.pos_db[position]["Leadership"]:
            self.leadership = round((random.random() + 1)/2, 2)

        self.name = name_gen.name_gen()


def use_global_action():
    """Use one global action. Update global action label to reflect change."""
    store_game.global_actions -= 1
    global_actions_label.config(text="Global actions remaining: " + str(store_game.global_actions))


def open_descript_win(position):
    descript_win = Toplevel(window_1)
    descript_win.geometry("500x200")
    descript = Label(descript_win)

    if position == "Sales Associate":
        descript.config(text="Basic employee type. Each store requires at least 3 Sales Associates."
                             "\n If there are fewer than three, 'overtime' is triggered."
                             "\n Salary: $30000")
    elif position == "Jr. Manager":
        descript.config(text="A step above Sales Associate."
                             "\n Contributes to leadership (increases local actions by 1) and productivty."
                             "\n Salary: $45000")
    elif position == "Sr. Manager":
        descript.config(text="A step above Jr. Manager."
                             "\n Contributes to leadership (increases local actions by 1)."
                             "\n Every store must have a Sr. Manager before a new store can be opened."
                             "\n Salary: $60000"
                             "\n May be directly hired or promoted from Sales Associate")

    descript.pack()


def open_employee_win():
    employee_win = Toplevel(window_1)
    employee_win.geometry("400x200")
    employee_win.title("View Employee Descriptions")
    bg = Canvas(employee_win, width=400, height=200)
    bg.pack()
    sal_ass = Button(bg, text="Sales Associate", command=lambda: open_descript_win("Sales Associate"))
    jr_man = Button(bg, text="Jr. Manager", command=lambda: open_descript_win("Jr. Manager"))
    sr_man = Button(bg, text="Sr. Manager", command=lambda: open_descript_win("Sr. Manager"))
    sal_ass.place(x=50, y=75)
    jr_man.place(x=170, y=75)
    sr_man.place(x=275, y=75)


def open_rank_win():
    rank_win = Toplevel(window_1)
    rank_win.geometry("400x400")
    rank_win.title("View Rank")

    rank_string = store_game.calc_rank(store_data)
    # rank_string data comes from scraper and is calculated during startup
    rank = Label(rank_win, text=rank_string)

    rank.pack()


def create_store_button(sid):
    """Create a button that represents a store."""
    store_button = Button(window_1, text="Store " + str(sid), command=lambda: open_store_win(sid))
    if sid < 12:
        store_button.place(x=(50 + (sid - 1) * 100), y=50)
    else:
        store_button.place(x=(50 + (sid - 11) * 100), y=100)


def open_store_win(store_id):
    """Create a new window displaying store info and employee info for the store corresponding to store_id."""

    store_win = Toplevel(window_1)
    store_win.geometry("800x600")
    store_win.title("Store " + str(store_id))

    store = store_game.stores[store_id]

    create_store_labels(store, store_win)
    employee_labels(store, store_win)
    create_store_buttons(store, store_win, store_id)


def employee_labels(store, store_win):
    """Create a string with relevant employee info for the store corresponding to store_id."""
    sa_count = 0
    jr_count = 0
    productivity = ""

    for eid, employee in store.employees.items():
        if store.evaluations is True:
            productivity = "    Productivity: " + str(employee.productivity)
        if employee.position == "Sales Associate":
            Label(store_win, text=employee.name + productivity).place(x=75, y=(75 + sa_count*25))
            sa_count += 1
        elif employee.position == "Jr Manager":
            Label(store_win, text=employee.name + productivity).place(x=75, y=(275 + jr_count * 25))
            jr_count += 1
        else:
            Label(store_win, text=employee.name + productivity).place(x=75, y=355)


def create_store_buttons(store, store_win, store_id):
    """Create and place all buttons to be used in store window"""
    sa_count = 0
    jr_count = 0

    Button(store_win, text="Run Employee Evaluations",
           command=lambda: store.run_evaluations(store_win, store_id)).place(x=350, y=560)
    Button(store_win, text="Hire", command=lambda: open_hire_win(store, store_win, store_id)).place(x=350, y=520)

    for eid, employee in store.employees.items():
        fire_button = Button(store_win, text="Fire",
                             command=lambda eid=eid: store.fire_employee(eid, store_win, store_id))
        if employee.position == "Sales Associate":
            fire_button.place(x=350, y=(75 + sa_count*25))
            sa_count += 1
        elif employee.position == "Jr Manager":
            fire_button.place(x=350, y=(275 + jr_count * 25))
            jr_count += 1
        else:
            fire_button.place(x=350, y=355)


def create_store_labels(store, store_win):
    """Create and place all static store labels to be used in store window."""
    Label(store_win, text="Store Productivity " + str(store.productivity)).place(x=300, y=25)
    Label(store_win, text="Local actions remaining: " + str(store.local_actions)).place(x=600, y=560)
    Label(store_win, text="Last Year's Income ").place(x=50, y=500)
    Label(store_win, text="Gross Income: $" + str(store.year_gross_income)).place(x=50, y=520)
    Label(store_win, text="Net Income: $" + str(store.year_net_income)).place(x=50, y=540)
    Label(store_win, text="Percent Net Income: " + str(store.percent_net_income) + "%").place(x=50, y=560)
    Label(store_win, text="Sales Associates").place(x=50, y=50)
    Label(store_win, text="Jr. Managers").place(x=50, y=250)
    Label(store_win, text="Sr. Manager").place(x=50, y=330)


def store_win_refresh(store_win, store_id):
    """Close store window and reopen it."""
    store_win.destroy()
    open_store_win(store_id)


def open_hire_win(store, store_win, store_id):
    """Method called when player clicks "Hire" from store window. parameter "store" is a store class object. """
    hire_win = Toplevel(window_1)
    hire_win.geometry("300x200")
    hire_win.title("Hire Employee")

    context = Label(hire_win, text="What position would you like to hire for?")

    hire_sa = Button(hire_win, text="Sales Associate",
                     command=lambda: store.confirm_hire("Sales Associate", hire_win, store_win, store_id))
    hire_jrman = Button(hire_win, text="Jr Manager",
                        command=lambda: store.confirm_hire("Jr Manager", hire_win, store_win, store_id))
    hire_srman = Button(hire_win, text="Sr Manager",
                        command=lambda: store.confirm_hire("Sr Manager", hire_win, store_win, store_id))

    context.pack()
    hire_sa.pack()
    hire_jrman.pack()
    hire_srman.pack()


def open_news_win(news):
    """Displayed at the beginning of each year. Contains information about which employees have quit."""
    news_win = Toplevel(window_1)
    news_win.geometry("400x300")
    news_win.title("Year News")
    news_label = Label(news_win, text=news)

    news_label.pack()


def open_confirm_win(message):
    """Display confirmation window with yes and no buttons. Yes returns True, no returns False."""
    response = askyesno(title="Confirmation", message=message)
    return response


store_game = Game()

next_year_button = Button(window_1, text="Go To Next Year", command=store_game.go_to_next_year)
employee_button = Button(window_1, text="View Employee Descriptions", command=open_employee_win)
rank_button = Button(window_1, text="View Rank", command=open_rank_win)
location_button = Button(window_1, text="Open a New Location", command=store_game.open_store)
global_actions_label.config(text="Global actions remaining: " + str(store_game.global_actions))

year_label = Label(window_1, text="Year " + str(store_game.year) + " of 10")


location_button.place(x=525, y=300)

rank_button.place(x=50, y=625)
employee_button.place(x=50, y=675)

notice_label.place(x=450, y=675)
global_actions_label.place(x=525, y=725)

next_year_button.place(x=1050, y=675)
year_label.place(x=1050, y=725)

store_game.open_store()

window_1.mainloop()
