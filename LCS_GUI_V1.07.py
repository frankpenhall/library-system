from tkinter import *
from tkinter import font
import tkinter.messagebox
import sqlite3
import datetime


class LCSApp(tkinter.Tk):
    freeStaffID = 20000
    freePatronID = 200
    freeBookID = 50000

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkinter.font.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Library Circulation System V2.0")
        self.geometry("1920x1080")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, AdminHomePage, ManageStaffPage, BookManagerPage, LibrarianHomePage, BookTransactionPage, ManagePatronPage, PatronHomePage, BookSearchPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()

    def lower_frame(self, page_name):
        frame = self.frames[page_name]
        tkinter.Tk.lower(frame)

    def get_frame(self, page_name):
        frame = self.frames[page_name]
        return frame


class LoginPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        welcome_label = Label(self, text="Welcome to J.F.K. Library!", font=tkinter.font.Font(family='Helvetica', weight="bold", size=20, slant="italic"))

        # Staff Login Widgets
        self.user_label = Label(self, text="Username")
        self.pass_label = Label(self, text="Password")
        self.user_entry = Entry(self)
        self.pass_entry = Entry(self, show="*")
        forgot_user_button = Button(self, text="Forgot Username",
                                    command=lambda: self.forgot_user())
        forgot_pass_button = Button(self, text="Forgot Password",
                                    command=lambda: self.forgot_pass())
        login_button = Button(self, text="Login",
                              command=lambda: self.login())

        # Add staff login widgets to grid
        welcome_label.grid(row=0, columnspan=3, padx=(825, 0), pady=(10, 0))
        self.user_label.grid(row=1, sticky=E, pady=(20, 0))
        self.pass_label.grid(row=2, sticky=E)
        self.user_entry.grid(row=1, column=1, pady=(20, 0))
        self.pass_entry.grid(row=2, column=1)
        login_button.grid(row=3, column=1)
        forgot_user_button.grid(row=4, column=1)
        forgot_pass_button.grid(row=5, column=1)

        # Guest Login Widgets
        guest_label = Label(self, text="Guests Enter Here", font = tkinter.font.Font(family='Helvetica', size=14))
        guest_button = Button(self, text="Guest Entry",
                              command=lambda: controller.show_frame("PatronHomePage"))

        # Add Guest Widgets to grid
        guest_label.grid(row=1, column=2, padx=(50, 0), pady=(20, 0))
        guest_button.grid(row=2, column=2, padx=(50, 0))
        self.grid_columnconfigure(0, minsize=850)

    def login(self):
        self.conn = sqlite3.connect('library.db') # creates connection to the database
        self.c = self.conn.cursor() # creates a cursor
        # sql statement to select the username and password from the staff table in the database
        # if the user inputs a username and password that is found in the database, then login works
        login_check = ("SELECT * FROM staff WHERE user = (?) AND pass = (?)")
        self.c.execute(login_check, [(self.user_entry.get()), (self.pass_entry.get())])
        result = self.c.fetchall()
        if result:
            print('Logged In')  # in the database, each employee is designated a 0 or a 1
            name = result[0][0] + " " + result[0][1]
            if result[0][5] == 0:  # if there is a 0, then the employee is a librarian
                temp = "Logged in as: " + name
                LibrarianHomePage.set_active_user(self.controller.get_frame("LibrarianHomePage"), temp)
                self.controller.show_frame("LibrarianHomePage")

            elif result[0][5] == 1:  # if there is a 1, then the employee is a admin
                temp = "Logged in as: " + name
                AdminHomePage.set_active_user(self.controller.get_frame("AdminHomePage"), temp)
                self.controller.show_frame("AdminHomePage")
        else:
            tkinter.messagebox.showerror(title="Error", message="Invalid Username or Password")
        self.user_entry.delete(0, END)
        self.pass_entry.delete(0, END)
        self.conn.commit()
        self.conn.close()

    def forgot_user(self):
        self.forgot_user_window = Tk()
        self.forgot_user_window.title('Forgot Username')
        self.forgot_user_window.geometry("400x200")
        self.phone_number_label = Label(self.forgot_user_window, text="Phone Number")
        self.staff_id_label = Label(self.forgot_user_window, text="Staff ID")
        self.phone_number_entry = Entry(self.forgot_user_window)
        self.staff_id_entry = Entry(self.forgot_user_window)
        find_user_button = Button(self.forgot_user_window, text="Submit",
                                    command=lambda: self.get_user())

        self.phone_number_label.grid(row=1, sticky=E)
        self.staff_id_label.grid(row=2, sticky=E)
        self.phone_number_entry.grid(row=1, column=1)
        self.staff_id_entry.grid(row=2, column=1)
        find_user_button.grid(row=4, column=1)

    def get_user(self):
        self.conn = sqlite3.connect('library.db') # creates connection to the database
        self.c = self.conn.cursor() # creates a cursor
        find_user = ("SELECT * FROM staff WHERE staff_id = (?) AND phone_number = (?)")
        self.c.execute(find_user, [(self.staff_id_entry.get()), (self.phone_number_entry.get())])
        result = self.c.fetchall()
        self.forgot_user_window.destroy()

        if len(result) > 0:
            tkinter.messagebox.showinfo(title=None, message="Your username: " + str(result[0][2]))
        else:
            tkinter.messagebox.showerror(title="Error", message="Info does not match records. Try again.")

        # self.phone_number_entry.delete(0, END)
        # self.staff_id_entry.delete(0, END)
        self.conn.commit()
        self.conn.close()

    def forgot_pass(self):
        self.forgot_pass_window = Tk()
        self.forgot_pass_window.title('Forgot Password')
        self.forgot_pass_window.geometry("400x200")
        self.user_label = Label(self.forgot_pass_window, text="Username")
        self.staff_id_label = Label(self.forgot_pass_window, text="Staff ID")
        self.user_entry = Entry(self.forgot_pass_window)
        self.staff_id_entry = Entry(self.forgot_pass_window)
        find_pass_button = Button(self.forgot_pass_window, text="Submit",
                                    command=lambda: self.get_pass())

        self.user_label.grid(row=1, sticky=E)
        self.staff_id_label.grid(row=2, sticky=E)
        self.user_entry.grid(row=1, column=1)
        self.staff_id_entry.grid(row=2, column=1)
        find_pass_button.grid(row=4, column=1)

    def get_pass(self):
        self.conn = sqlite3.connect('library.db') # creates connection to the database
        self.c = self.conn.cursor() # creates a cursor
        get_pass_check = ("SELECT * FROM staff WHERE staff_id = (?) AND user = (?)")
        self.c.execute(get_pass_check, [(self.staff_id_entry.get()), (self.user_entry.get())])
        result = self.c.fetchall()
        self.forgot_pass_window.destroy()

        if len(result) > 0:
            tkinter.messagebox.showinfo(title=None, message="Your password: " + str(result[0][3]))
        else:
            tkinter.messagebox.showerror(title="Error", message="Info does not match records. Try again.")

        self.conn.commit()
        self.conn.close()


# Home Pages
class AdminHomePage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        sign_out_button = Button(self, text="Sign Out", height=2, width=20,
                                 command=lambda: controller.show_frame("LoginPage"))
        home_label = Label(self, text="Administrator Home", font=tkinter.font.Font(family='Helvetica', weight="bold", size=20, slant="italic"))
        self.active_user_label = Label(self, text="", font=tkinter.font.Font(family='Helvetica', size=14, slant="italic"))

        manage_books_button = Button(self, text="Mange Books",  height=8, width=20, bg="SkyBlue1",
                                     command=lambda: controller.show_frame("BookManagerPage"))
        manage_staff_button = Button(self, text="Mange Staff",  height=8, width=20, bg="SkyBlue1",
                                     command=lambda: controller.show_frame("ManageStaffPage"))
        book_search_button = Button(self, text="Book Search",  height=8, width=20, bg="SkyBlue1",
                                    command=lambda: controller.show_frame("BookSearchPage"))

        # Set up Grid Placements
        sign_out_button.grid(row=0, column=0)
        home_label.grid(row=0, column=0, columnspan=5, padx=(715, 0), pady=(50, 0))
        self.active_user_label.grid(row=1, column=1, columnspan=5, padx=(560, 0))

        manage_books_button.grid(row=2, column=2, padx=(550, 0), pady=(70, 0))
        manage_staff_button.grid(row=2, column=3, padx=(50, 0), pady=(70, 0))
        book_search_button.grid(row=2, column=4, padx=(50, 0), pady=(70, 0))

    def set_active_user(self, user_name):
        self.active_user_label.config(text=user_name)


class LibrarianHomePage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        sign_out_button = Button(self, text="Sign Out", height=2, width=20,
                                 command=lambda: controller.show_frame("LoginPage"))
        home_label = Label(self, text="Librarian Home", font=tkinter.font.Font(family='Helvetica', weight="bold", size=20, slant="italic"))
        self.active_user_label = Label(self, text="Signed in as: ", font=tkinter.font.Font(family='Helvetica', size=14, slant="italic"))

        manage_books_button = Button(self, text="Book Transaction", height=8, width=20, bg="SkyBlue1",
                                     command=lambda: controller.show_frame("BookTransactionPage"))
        manage_patron_button = Button(self, text="Mange Patrons", height=8, width=20, bg="SkyBlue1",
                                      command=lambda: controller.show_frame("ManagePatronPage"))
        book_search_button = Button(self, text="Book Search", height=8, width=20, bg="SkyBlue1",
                                    command=lambda: controller.show_frame("BookSearchPage"))

        # Set up Grid Placements
        sign_out_button.grid(row=0, column=0)
        home_label.grid(row=0, column=0, columnspan=5, padx=(715, 0), pady=(50, 0))
        self.active_user_label.grid(row=1, column=1, columnspan=5, padx=(560, 0))

        manage_books_button.grid(row=2, column=2, padx=(550, 0), pady=(70, 0))
        manage_patron_button.grid(row=2, column=3, padx=(50, 0), pady=(70, 0))
        book_search_button.grid(row=2, column=4, padx=(50, 0), pady=(70, 0))

    def set_active_user(self, user_name):
        self.active_user_label.config(text=user_name)


class PatronHomePage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        back_button = Button(self, text="Back",
                             command=lambda: self.go_back())
        home_label = Label(self, text="Guest Home", font=tkinter.font.Font(family='Helvetica', weight="bold", size=20, slant="italic"))
        book_search_button = Button(self, text="Book Search",
                                    command=lambda: controller.show_frame("BookSearchPage"))
        card_label = Label(self, text="Card Number")
        self.card_entry = Entry(self)
        look_account_button = Button(self, text="Look Up Account",
                                     command=lambda: self.find_account())

        # List Box to show search Results
        results_frame = Frame(self)
        scroll_bar = Scrollbar(results_frame, orient=VERTICAL)
        self.search_results = Listbox(results_frame, yscrollcommand=scroll_bar.set, width=100)
        scroll_bar.config(command=self.search_results.yview)
        scroll_bar.pack(side=RIGHT, fill=Y)
        self.search_results.pack(side=LEFT, fill=BOTH, expand=1)

        # Set up Grid Placements
        back_button.grid(row=0, column=0)
        home_label.grid(row=0, column=1, columnspan=6, padx=(580, 0), pady=(10, 0))

        book_search_button.grid(row=2, column=1, padx=(629, 0), pady=(20, 0))

        card_label.grid(row=2, column=2, sticky=E, padx=(198, 0), pady=(20, 0))
        self.card_entry.grid(row=2, column=3, pady=(20, 0))
        look_account_button.grid(row=2, column=4, pady=(20, 0))
        results_frame.grid(row=3, column=1, columnspan=6, padx=(630, 0), pady=(10, 0))

    def find_account(self):
        self.search_results.delete(0, END) # clears the list box from previous query
        self.conn = sqlite3.connect('library.db') # creates connection to the database
        self.c = self.conn.cursor() # creates a cursor
        # executes a sql statement to find a patron in the database based on the card number
        self.c.execute("SELECT * FROM patrons WHERE card_number = (?)", (self.card_entry.get(),))
        self.patron = self.c.fetchone() # variable to catch the query

        if self.patron is None:
            tkinter.messagebox.showerror(title="Error",
                                         message="No Account Found. Please check card number.")
            return

        name = "Name: " + self.patron[0] + " " + self.patron[1]
        phone = "Phone Number: " + self.patron[2]
        fines = "Fines Owed: " + str(self.patron[5])
        self.search_results.insert(END, name)
        self.search_results.insert(END, phone)
        self.search_results.insert(END, fines)
        self.search_results.insert(END, "Books Checked Out: ")

        self.c.execute("SELECT * FROM books WHERE owner = (?)", [(self.card_entry.get())])
        books = self.c.fetchall()

        for row in books:
            if row is not None:
                date_time_obj = datetime.datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S.%f')
                if row[5] == 2:
                    slot = row[0] + "     " + "Held Until: " + " " + date_time_obj.strftime("%d %b %Y")
                else:
                    slot = row[0] + "     " + "Due: " + " " + date_time_obj.strftime("%d %b %Y")
                self.search_results.insert(END, slot)

        self.conn.commit()  # Commits changes to the database if there were changes
        self.conn.close()  # closes the connection to the database

    def go_back(self):
        self.card_entry.delete(0, END)
        self.search_results.delete(0, END)
        self.controller.show_frame("LoginPage")


class BookSearchPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        back_button = Button(self, text="Back",
                             command=lambda: self.go_back())

        home_label = Label(self, text="Library Book Search", font=tkinter.font.Font(family='Helvetica', weight="bold", size=20, slant="italic"))
        title_label = Label(self, text="Title")
        author_label = Label(self, text="Author")
        subject_label = Label(self, text="Subject")

        self.title_entry = Entry(self)
        self.author_entry = Entry(self)
        self.subject_entry = Entry(self)
        search_button = Button(self, text="Search",
                               command=lambda: self.do_search())

        # List Box to show search Results
        results_frame = Frame(self)
        scroll_bar = Scrollbar(results_frame, orient=VERTICAL)
        self.search_results = Listbox(results_frame, yscrollcommand=scroll_bar.set, width=100)
        scroll_bar.config(command=self.search_results.yview)
        scroll_bar.pack(side=RIGHT, fill=Y)
        self.search_results.pack(side=LEFT, fill=BOTH, expand=1)

        # Set up Grid Placements
        back_button.grid(row=0, column=0)
        home_label.grid(row=0, column=1, columnspan=5, padx=(650, 0), pady=(10, 0))
        title_label.grid(row=1, column=1, sticky=E, padx=(800, 0), pady=(20, 0))
        author_label.grid(row=2, column=1, sticky=E)
        subject_label.grid(row=3, column=1, sticky=E)

        self.title_entry.grid(row=1, column=2, pady=(20, 0))
        self.author_entry.grid(row=2, column=2)
        self.subject_entry.grid(row=3, column=2)
        search_button.grid(row=4, column=2, pady=(15, 0))
        results_frame.grid(row=5, column=1, columnspan=5, padx=(700, 0), pady=(15, 0))

    def go_back(self):
        self.title_entry.delete(0, END)
        self.author_entry.delete(0, END)
        self.subject_entry.delete(0, END)
        self.search_results.delete(0, END)
        self.controller.lower_frame("BookSearchPage")

    def do_search(self):
        self.search_results.delete(0, END)  # clears the list box from previous search
        self.conn = sqlite3.connect('library.db')  # connects to the database
        self.c = self.conn.cursor() # creates a cursor
        # executes a sql query to the database, selecting book(s) according to the inputs
        self.c.execute("SELECT * FROM books WHERE title = (?) OR author = (?) OR subject = (?)", (self.title_entry.get(), self.author_entry.get(), self.subject_entry.get()))
        self.results = self.c.fetchall() # variable catches the books from the query

        if len(self.results) == 0:
            tkinter.messagebox.showerror(title="Error", message="No Results Found. Please try a different search.")
            return

        box_index = 0;
        for book in self.results: # for loop to insert the books into the list box
            color = 'green'
            status = "Available"

            if book[5] == 1:
                status = "Checked Out"
                color='red'
            elif book[5] == 2:
                status = "On Hold"
                color='blue'

            slot = book[0] + " , " + book[1] + " , " + book[2] + " , " + str(book[3]) + " , " + "Status: " + status
            self.search_results.insert(END, slot)
            self.search_results.itemconfig(box_index, {'fg': color})
            box_index += 1

        self.conn.commit()
        self.conn.close()

        # Add results to list box or throw error No such book found


# Librarian-Specific Pages
class ManagePatronPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        back_button = Button(self, text="Back",
                             command=lambda: self.go_back())
        self.home_label = Label(self, text="Manage Patrons", font=controller.title_font)

        self.first_name_label = Label(self, text="First Name")
        self.last_name_label = Label(self, text="Last Name")
        self.card_number_label = Label(self, text="Card Number")
        self.phone_number_label = Label(self, text="Phone Number")
        self.address_label = Label(self, text="Address")

        self.first_name_entry = Entry(self)
        self.last_name_entry = Entry(self)
        self.card_number_entry = Entry(self)
        self.phone_number_entry = Entry(self)
        self.address_entry = Entry(self)
        submit_button = Button(self, text="Submit",
                               command=lambda: self.do_submit())
        # Set up Drop Down Menu
        self.clicked = StringVar()
        self.clicked.trace('w', self.change_view)
        drop = OptionMenu(self, self.clicked, "Add Patron", "Update Phone Number", "Delete Patron")
        self.clicked.set("Select Option")

        # Set up Grid Placements
        back_button.grid(row=0, column=0)
        self.home_label.grid(row=0, column=1, columnspan=6, padx=(800, 0), pady=(10, 10))
        self.first_name_label.grid(row=1, column=2, sticky=E, padx=(800, 0))
        self.last_name_label.grid(row=2, column=2, sticky=E)
        self.card_number_label.grid(row=3, column=2, sticky=E, padx=(800, 0))
        self.phone_number_label.grid(row=4, column=2, sticky=E)
        self.address_label.grid(row=5, column=2, sticky=E)

        self.first_name_entry.grid(row=1, column=3, sticky=W)
        self.last_name_entry.grid(row=2, column=3, sticky=W)
        self.card_number_entry.grid(row=3, column=3, sticky=W)
        self.phone_number_entry.grid(row=4, column=3, sticky=W)
        self.address_entry.grid(row=5, column=3, sticky=W)
        drop.grid(row=6, column=3, sticky=W)
        submit_button.grid(row=7, column=3, sticky=W)

    def go_back(self):
        self.first_name_entry.delete(0, END)
        self.last_name_entry.delete(0, END)
        self.card_number_entry.delete(0, END)
        self.phone_number_entry.delete(0, END)
        self.controller.show_frame("LibrarianHomePage")

    def change_view(self, *args):
        # Hides Widgets based on the drop down option selected
        if self.clicked.get() == "Add Patron":
            print("Add Patron selected")
            self.first_name_label.grid()
            self.first_name_entry.grid()
            self.last_name_label.grid()
            self.last_name_entry.grid()
            self.card_number_label.grid_remove()
            self.card_number_entry.grid_remove()
            self.phone_number_label.grid()
            self.phone_number_label.config(text="Phone Number")
            self.phone_number_entry.grid()
            self.address_label.grid()
            self.address_entry.grid()

        elif self.clicked.get() == "Update Phone Number":
            print("Update Phone Number Selected")
            self.first_name_label.grid_remove()
            self.first_name_entry.grid_remove()
            self.last_name_label.grid_remove()
            self.last_name_entry.grid_remove()
            self.card_number_label.grid()
            self.card_number_entry.grid()
            self.phone_number_label.grid()
            self.phone_number_label.config(text="New Phone Number")
            self.phone_number_entry.grid()
            self.address_label.grid_remove()
            self.address_entry.grid_remove()

        elif self.clicked.get() == "Delete Patron":
            print("Delete Patron Selected")
            self.first_name_label.grid_remove()
            self.first_name_entry.grid_remove()
            self.last_name_label.grid_remove()
            self.last_name_entry.grid_remove()
            self.card_number_label.grid()
            self.card_number_entry.grid()
            self.phone_number_label.grid_remove()
            self.phone_number_entry.grid_remove()
            self.address_label.grid_remove()
            self.address_entry.grid_remove()


    def do_submit(self):
        if self.clicked.get() == "Add Patron":
            first = self.first_name_entry.get()
            last = self.last_name_entry.get()
            phone = self.phone_number_entry.get()
            address = self.address_entry.get()
            if(first != "") and (last != "") and (phone != "") and (address != ""):
                msg = "Ensure information is correct and hit YES to add patron\n" + \
                      "First name: " + first + "\n" + \
                      "Last name: " + last + "\n" + \
                      "Phone Number: " + phone + "\n" + \
                      "Address: " + address + "\n"

                if tkinter.messagebox.askquestion(title="Confirm Info", message=msg) == "yes":
                    self.add_patron()
            else:
                tkinter.messagebox.showerror(title="Error", message="Please Fill all fields to add Patron")

        elif self.clicked.get() == "Delete Patron":
            # Deleting a patron from the database
            self.conn = sqlite3.connect('library.db')
            self.c = self.conn.cursor()
            self.c.execute("SELECT * FROM patrons WHERE card_number = (?)", (self.card_number_entry.get(),))
            account = self.c.fetchone()
            self.c.execute("SELECT owner FROM books WHERE owner = (?)", (self.card_number_entry.get(),))
            books_due = self.c.fetchall()
            self.conn.commit()
            self.conn.close()
            if account is None:
                tkinter.messagebox.showerror(title="Error",
                                             message="Patron Account Not Found.")
                return

            if len(books_due) == 0 and account[5] <= 0.01:
                msg = "Are you sure you wish to delete " + account[0] + " " + account[1] + "'s account?"
                if tkinter.messagebox.askquestion(title="Confirm Delete", message=msg) == "yes":
                    self.delete_patron()
            else:
                tkinter.messagebox.showerror(title="Error",
                                             message="Please Return All books and pay all fines before deleting account")

        elif self.clicked.get() == "Update Phone Number":
            self.conn = sqlite3.connect('library.db')
            self.c = self.conn.cursor()
            self.c.execute("SELECT card_number FROM patrons WHERE card_number = (?)", (self.card_number_entry.get(),))
            result = self.c.fetchall()
            self.conn.commit()
            self.conn.close()

            if result:
                self.update_phone_number()
            else:
                tkinter.messagebox.showerror(title="Error", message="Patron Account Not Found")

    def add_patron(self):
        self.conn = sqlite3.connect('library.db')
        self.c = self.conn.cursor()
        self.c.execute("INSERT INTO patrons VALUES (?,?,?,?,?,?)", (
        self.first_name_entry.get(), self.last_name_entry.get(), self.phone_number_entry.get(),
        self.address_entry.get(), self.controller.freePatronID, 0.00))
        self.c.execute("SELECT * FROM patrons")
        self.controller.freePatronID += 1
        tkinter.messagebox.showinfo(title="Success", message="Patron Account Added Successfully\n" + "Card Number: " + str(self.controller.freePatronID -1))
        self.first_name_entry.delete(0, END)
        self.last_name_entry.delete(0, END)
        self.phone_number_entry.delete(0, END)
        self.address_entry.delete(0, END)
        self.conn.commit()
        self.conn.close()

    def delete_patron(self):
        self.conn = sqlite3.connect('library.db')
        self.c = self.conn.cursor()
        delete_patron = ("DELETE FROM patrons WHERE card_number = (?)")
        self.c.execute(delete_patron, [(self.card_number_entry.get())])
        tkinter.messagebox.showinfo(title="Success", message="Patron Account Deleted Successfully")
        self.conn.commit()
        self.conn.close()

    def update_phone_number(self):
        self.conn = sqlite3.connect('library.db')
        self.c = self.conn.cursor()
        update_patron = ("UPDATE patrons SET phone_number = (?) WHERE card_number = (?)")
        self.c.execute(update_patron, [(self.phone_number_entry.get()), (self.card_number_entry.get())])
        tkinter.messagebox.showinfo(title="Success", message="Patron phone number updated successfully")
        self.conn.commit()
        self.conn.close()


class BookTransactionPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        back_button = Button(self, text="Back",
                             command=lambda: self.go_back())

        home_label = Label(self, text="Book Transaction", font=tkinter.font.Font(family='Helvetica', weight="bold", size=20, slant="italic"))
        patron_id_label = Label(self, text="Patron ID")
        book_id_label = Label(self, text="Book ID")

        self.patron_id_entry = Entry(self)
        self.book_id_entry = Entry(self)
        submit_button = Button(self, text="Submit",
                               command=lambda: self.do_submit())

        self.clicked = StringVar()
        self.clicked.set("Select An Option")
        drop = OptionMenu(self, self.clicked, "Check Out", "Check In", "Place Hold")

        # Set up Grid Placements
        back_button.grid(row=0, column=0)
        home_label.grid(row=0, column=1, columnspan=6, padx=(830, 0), pady=(10, 0))

        patron_id_label.grid(row=1, column=2, sticky=E, padx=(800, 0), pady=(20, 0))
        book_id_label.grid(row=2, column=2, sticky=E, padx=(800, 0))

        self.patron_id_entry.grid(row=1, column=3, pady=(20, 0))
        self.book_id_entry.grid(row=2, column=3)

        drop.grid(row=3, column=3, pady=(10, 0))
        submit_button.grid(row=4, column=3, pady=(5, 0))

    def go_back(self):
        self.patron_id_entry.delete(0, END)
        self.book_id_entry.delete(0, END)
        self.controller.show_frame("LibrarianHomePage")

    def do_submit(self):
        if(self.patron_id_entry.get() == "") or (self.book_id_entry.get() == ""):
            tkinter.messagebox.showerror(title="Error",
                                         message="Please Fill all fields.")
            return

        if self.clicked.get() == "Check Out":
            self.check_out()
        elif self.clicked.get() == "Check In":
            self.check_in()
        elif self.clicked.get() == "Place Hold":
            self.place_hold()

    def check_out(self):
        patronID = self.patron_id_entry.get()  #int(self.patron_id_entry.get())
        bookID = self.book_id_entry.get()
        new_date = datetime.datetime.now() + datetime.timedelta(days=21)

        self.conn = sqlite3.connect('library.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM patrons WHERE card_number = (?)", [(patronID)])
        self.patron = self.c.fetchone()  # variable to catch the query
        self.c.execute("SELECT * FROM books WHERE book_id = (?)", [(bookID)])
        self.book = self.c.fetchone()
        # Patron Checks
        if self.patron is None:
            tkinter.messagebox.showerror(title="Error",
                                         message="Patron Not Found. Please Check Account Number.")
            return
        elif self.patron[5] > 5.0:
            tkinter.messagebox.showerror(title="Error",
                                         message="Patron owes fines over $5.00. Please pay fines before borrowing.")
            return
        # Book Checks
        if self.book is None:
            tkinter.messagebox.showerror(title="Error",
                                         message="Book Not Found. Please Check Book ID.")
            return
        elif self.book[5] == 1:
            tkinter.messagebox.showerror(title="Error",
                                         message="Book Already Checked Out. Please check in book before loaning.")
            return
        elif self.book[5] == 2 and self.book[7] == patronID:
            tkinter.messagebox.showerror(title="Error",
                                         message="Patron already has this book on hold.")
            return
        elif self.book[5] == 2 and self.book[7] != patronID:
            tkinter.messagebox.showerror(title="Error",
                                         message="Book is on hold. Only holder can check out this material.")
            return

        self.c.execute("UPDATE books SET checked_out = (?), due_date = (?), owner = (?) WHERE book_id = (?)", [(1), (new_date), (patronID), (bookID)])
        self.conn.commit()
        self.conn.close()
        tkinter.messagebox.showinfo(title="Success", message="Book Checked Out Successfully. \n Due: " + new_date.strftime("%d %b %Y"))

    def check_in(self):
        patronID = self.patron_id_entry.get() # int (self.patron_id_entry.get())
        bookID = self.book_id_entry.get()
        temp_date = datetime.datetime.now()

        self.conn = sqlite3.connect('library.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM patrons WHERE card_number = (?)", [(patronID)])
        self.patron = self.c.fetchone()  # variable to catch the query
        self.c.execute("SELECT * FROM books WHERE book_id = (?)", [(bookID)])
        self.book = self.c.fetchone()

        # Patron Checks
        if self.patron is None:
            tkinter.messagebox.showerror(title="Error",
                                         message="Patron Not Found. Please Check Account Number.")
            return
        # Book Checks
        if self.book is None:
            tkinter.messagebox.showerror(title="Error",
                                         message="Book Not Found. Please Check Book ID.")
            return
        elif self.book[7] != patronID:
            tkinter.messagebox.showerror(title="Error",
                                         message="Book is not Checked Out to this Patron. Please check Patron ID.")
            return

        self.c.execute("UPDATE books SET checked_out = (?), due_date = (?), owner = (?) WHERE book_id = (?)",
                       [(0), (temp_date), (-1), (bookID)])

        self.conn.commit()
        self.conn.close()
        tkinter.messagebox.showinfo(title="Success",
                                    message="Book Checked In Successfully. \n Fines Owed: " + str(self.patron[5]))

    def place_hold(self):
        patronID = self.patron_id_entry.get() # int(self.patron_id_entry.get())
        bookID = self.book_id_entry.get()
        temp_date = datetime.datetime.now() + datetime.timedelta(days=21)

        self.conn = sqlite3.connect('library.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM patrons WHERE card_number = (?)", [(patronID)])
        self.patron = self.c.fetchone()  # variable to catch the query
        self.c.execute("SELECT * FROM books WHERE book_id = (?)", [(bookID)])
        self.book = self.c.fetchone()

        # Patron Checks
        if self.patron is None:
            tkinter.messagebox.showerror(title="Error",
                                         message="Patron Not Found. Please Check Account Number.")
            return
        # Book Checks
        if self.book is None:
            tkinter.messagebox.showerror(title="Error",
                                         message="Book Not Found. Please Check Book ID.")
            return
        elif self.book[5] == 1:
            tkinter.messagebox.showerror(title="Error",
                                         message="Book is currently checked out. It must be returned before holding.")
            return
        elif self.book[5] == 2:
            tkinter.messagebox.showerror(title="Error",
                                         message="Book is currently on hold. Please wait for hold to expire.")
            return

        self.c.execute("UPDATE books SET checked_out = (?), due_date = (?), owner = (?) WHERE book_id = (?)",
                       [(2), (temp_date), (patronID), (bookID)])

        self.conn.commit()
        self.conn.close()
        tkinter.messagebox.showinfo(title="Success",
                                    message="Book Placed on hold. \n Held until: " + temp_date.strftime("%d %b %Y"))


# Admin Specific Pages
class ManageStaffPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        back_button = Button(self, text="Back",
                             command=lambda: self.go_back())

        home_label = Label(self, text="Manage Staff", font=controller.title_font)
        first_name_label = Label(self, text="First Name")
        last_name_label = Label(self, text="Last Name")
        address_label = Label(self, text="Address")
        phone_number_label = Label(self, text="Phone Number")
        instruct_label = Label(self, text="Add Staff: Fill All fields and click submit \n"
                                          "Update Contact: Enter the first and last name and the new info and submit \n"
                                          "Delete Staff: Enter First and Last Name and click submit")

        self.first_name_entry = Entry(self)
        self.last_name_entry = Entry(self)
        self.address_entry = Entry(self)
        self.phone_number_entry = Entry(self)
        # Is Admin Check Box
        self.admin_var = IntVar() # will be 1 if is admin is checked, 0 if unchecked
        self.is_admin = Checkbutton(self, text="Is Administrator", variable=self.admin_var)

        submit_button = Button(self, text="Submit",
                               command=lambda: self.do_submit())

        self.clicked = StringVar()
        drop = OptionMenu(self, self.clicked, "Add Staff", "Update Contact Info", "Delete Staff")

        # Set up Grid Placements
        back_button.grid(row=0, column=0)
        home_label.grid(row=0, column=1)
        first_name_label.grid(row=1, column=0, sticky=E)
        last_name_label.grid(row=2, column=0, sticky=E)
        address_label.grid(row=3, column=0, sticky=E)
        phone_number_label.grid(row=4, column=0, sticky=E)
        instruct_label.grid(row=0, column=2)

        self.first_name_entry.grid(row=1, column=1)
        self.last_name_entry.grid(row=2, column=1)
        self.address_entry.grid(row=3, column=1)
        self.phone_number_entry.grid(row=4, column=1)
        self.is_admin.grid(row=5, column=1)
        drop.grid(row=6, column=1)
        submit_button.grid(row=7, column=1)

    def go_back(self):
        self.first_name_entry.delete(0, END)
        self.last_name_entry.delete(0, END)
        self.address_entry.delete(0, END)
        self.phone_number_entry.delete(0, END)
        self.controller.show_frame("AdminHomePage")

    def do_submit(self):
        tkinter.messagebox.showerror(title="Error", message="Staff not found")
        # Query and Update DB


class BookManagerPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        back_button = Button(self, text="Back",
                             command=lambda: self.go_back())
        header_label = Label(self, text="Book Manager", font=tkinter.font.Font(family='Helvetica', weight="bold", size=20, slant="italic"))

        title_label = Label(self, text="Title")
        author_label = Label(self, text="Author")
        subject_label = Label(self, text="Subject")
        isbn_label = Label(self, text="ISBN")

        self.title_entry = Entry(self)
        self.author_entry = Entry(self)
        self.subject_entry = Entry(self)
        self.isbn_entry = Entry(self)
        add_button = Button(self, text="Add Book",
                            command=lambda: self.do_add())
        self.id_label = Label(self, text="Book ID")
        self.id_entry = Entry(self)
        self.delete_button = Button(self, text="Delete Book",
                                    command=lambda: self.do_delete())

        # Set up Grid Placements
        back_button.grid(row=0, column=0)
        header_label.grid(row=0, column=1, columnspan=8, padx=(800, 0), pady=(10, 0))

        # Add Book Column
        title_label.grid(row=1, column=2, sticky=E, padx=(750, 0), pady=(20, 0))
        author_label.grid(row=2, column=2, sticky=E)
        subject_label.grid(row=3, column=2, sticky=E)
        isbn_label.grid(row=4, column=2, sticky=E)

        self.title_entry.grid(row=1, column=3, pady=(20, 0))
        self.author_entry.grid(row=2, column=3)
        self.subject_entry.grid(row=3, column=3)
        self.isbn_entry.grid(row=4, column=3)
        add_button.grid(row=5, column=3, pady=(10, 0))

        # Delete Book Column
        self.id_label.grid(row=1, column=4, sticky=E, padx=(30, 0), pady=(20, 0))
        self.id_entry.grid(row=1, column=5, sticky=W, pady=(20, 0))
        self.delete_button.grid(row=2, column=5)

    def go_back(self):
        self.title_entry.delete(0, END)
        self.author_entry.delete(0, END)
        self.subject_entry.delete(0, END)
        self.isbn_entry.delete(0, END)
        self.id_entry.delete(0, END)
        self.controller.show_frame("AdminHomePage")

    def do_add(self):
        self.conn = sqlite3.connect('library.db')
        self.c = self.conn.cursor()

        title =  self.title_entry.get()
        author = self.author_entry.get()
        subject = self.subject_entry.get()
        isbn = self.isbn_entry.get()
        temp_date = datetime.datetime.now()

        if self.title_entry.get() == "" or self.author_entry.get() == "" or self.isbn_entry.get() == "" or self.subject_entry.get() == "":
            tkinter.messagebox.showerror(title="Error", message="One or more fields are empty!")
            return

        msg1 = "Are you sure you wish to add this book:\n" + "Title: " + title + "\nAuthor: " + author + "\nSubject: " + subject + "\nISBN: " + isbn
        if tkinter.messagebox.askquestion(title="Confirm Delete", message=msg1) == "yes":
            self.c.execute("INSERT INTO books VALUES (?,?,?,?,?,?,?,?)", (title, author, subject, isbn,
                                                                          self.controller.freeBookID, 0, temp_date, -1))
            self.controller.freeBookID += 1
            # Display book title  and new ID success
            self.c.execute("SELECT * FROM books WHERE book_id = (?)", [(self.controller.freeBookID - 1)])
            print(self.controller.freeBookID)
            book = self.c.fetchone()
            msg2 = book[0] + " has been added successfully!\n" + "Book ID: " + str(book[4])

            tkinter.messagebox.showinfo(title="Success", message=msg2)
        self.conn.commit()
        self.conn.close()

    def do_delete(self):
        self.conn = sqlite3.connect('library.db')
        self.c = self.conn.cursor()
        id = self.id_entry.get()
        self.c.execute("SELECt * FROM books WHERE book_id = (?)", [(id)])
        book = self.c.fetchone()

        if self.id_entry.get() == "":
            tkinter.messagebox.showerror(title="Error", message="Please enter a Book ID")
            return

        elif book is None:
            tkinter.messagebox.showerror(title="Error", message="Book Not Found. Please Check Book ID.")
            return

        msg = "Are you sure you wish to delete:\n" + book[0]
        if tkinter.messagebox.askquestion(title="Confirm Delete", message=msg) == "yes":
            delete_book = ("DELETE FROM books WHERE book_id = (?)")
            self.c.execute(delete_book, [(id)])
            # Confirm Delete Success
            tkinter.messagebox.showinfo(title="Success", message="The book has been deleted successfully!")
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    app = LCSApp()
    app.mainloop()
