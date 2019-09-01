# Author: Andrew white
# Complete Date: 30/03/2019
# Title: Hours Bank Program
# Description: This program allow the user to record the amount of hours their employees decides to 'bank' rather than
# get paid for immediatley. This means at busy times the employee can work extra hours that they can then get paid for
# at less busy times, allowing their income to remain steady.
# Method: This program uses a tkinter user interface for the user to drive. The data is stored in a database.

# import libraries from Tkinter
from tkinter import Tk, Label, Button, Listbox, END, Toplevel, Entry, Frame, font, Radiobutton, IntVar, StringVar, messagebox, Scrollbar
import dbFunctionsV2

# The base way to create an event driven program is using Class' so that is what this program does.
# class HoursBankGUI is the main Class and defines the main window of the GUI

class HoursBankGUI():
    def __init__(self, window):
        # define the window
        self.window = window
        window.title("Hours Banker")
        # define the size of the main window
        window.geometry('{}x{}'.format(700, 500))

        self.window.grid_rowconfigure(1, weight = 1)
        self.window.grid_columnconfigure(0, weight = 1)
        # pretends the window from being resized
        self.window.resizable(0,0)

        # font test
        # appHighlightFont = font.Font(family='Helvetica', size=12, weight='bold')

        # define the panels ##############################################################################
        # LEFT PANEL
        # This panel houses the list box which allows the user to select the employee
        self.leftFrame = Frame(self.window, bg = "white", width = 300, height = 500, pady = 3, borderwidth = 1, relief = "solid")
        self.leftFrame.grid(row = 0, sticky ="nsw")
        # keep the frame the same size even if the widgets chnage size
        self.leftFrame.grid_propagate(False)
        # label
        self.listLabel = Label(self.leftFrame, text = "Select User", bg = "white", font = "Ariel")
        self.listLabel.grid(row = 0, sticky = "nwe")
        # Listbox
        self.list_box = Listbox(self.leftFrame, width = 23, height = 18, bg = "white", font = ("Ariel", 14))
        self.list_box.grid(row = 1, sticky = "wes", padx = 10, pady = 20)
        # scroll Bar
        self.scrollbar = Scrollbar(self.leftFrame)
        self.list_box.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.list_box.yview)
        self.scrollbar.grid(column=2, row = 1, sticky="ns")
        # fire an event when a employee in the list box is selected
        self.list_box.bind('<<ListboxSelect>>', self.showDetailsLive)

        # RIGHT PANEL TOP
        # When a user clicks on an employee in the employee list box then their details will be shown in the panel
        self.rightFrame1 = Frame(self.window, bg = "white", width = 400, height = 300, relief = "solid", borderwidth = 1, padx = 20, pady = 5)
        self.rightFrame1.grid(row = 0, sticky = "ne")
        # keep the frame the same size even if the widgets change size
        self.rightFrame1.grid_propagate(False)

        # Label Widgets for the right top Frame
        self.details_title = Label(self.rightFrame1, text="Employee Details", font = "Ariel", bg = "white")
        self.details_title.grid(row = 0, column = 0, columnspan = 4, sticky="nw")
        self.name_label = Label(self.rightFrame1, text="Name", font = "Arial", bg = "white")
        self.name_label.grid(row = 3, column = 1, sticky = "w")
        self.ID_label = Label(self.rightFrame1, text="ID", font = "Arial", bg = "white")
        self.ID_label.grid(row = 2, column = 1, sticky = "w")
        self.Rate_label = Label(self.rightFrame1, text="Rate", font = "Arial", bg = "white")
        self.Rate_label.grid(row = 4, column = 1, sticky = "w")
        self.Hol_Rate_label = Label(self.rightFrame1, text="Holiday Rate", font = "Arial", bg = "white")
        self.Hol_Rate_label.grid(row = 5, column = 1, sticky = "w")
        self.Banked_Hours_label = Label(self.rightFrame1, text="Banked Hours", font = "Arial", bg = "white")
        self.Banked_Hours_label.grid(row=6, column=1, sticky = "w")
        self.Banked_Salary_label = Label(self.rightFrame1, text="Banked Salary", font = "Arial", bg = "white")
        self.Banked_Salary_label.grid(row = 7, column = 1, sticky = "w")

        # RIGHT BOTTOM PANEL
        # This panel contains the buttons the user can select to perform operations on the employees data
        self.rightFrame2 = Frame(self.window, bg = "white", width = 400, height = 200)
        self.rightFrame2.grid(row = 0, sticky = "se")
        # organises the grid of the panel to look good
        self.rightFrame2.grid_propagate(False) #Stops the frame resizing to widget
        self.rightFrame2.grid_columnconfigure(0, weight = 1)
        self.rightFrame2.grid_columnconfigure(1, weight = 1)
        self.rightFrame2.grid_rowconfigure(0, weight = 1)
        self.rightFrame2.grid_rowconfigure(1, weight = 1)
        self.rightFrame2.grid_rowconfigure(2, weight = 1)

        # Define the buttons of the bottom right panel
        self.add_user_button = Button(self.rightFrame2, text="New Employee", font = "Arial", relief = "groove", command=self.addTodB)
        self.add_user_button.grid(row = 0, column = 0, sticky = "nsew")
        self.add_hours_button = Button(self.rightFrame2, text="Add Hours", font = "Arial", relief = "groove", command=lambda: self.ChangeHours(False))
        self.add_hours_button.grid(row = 0, column = 1,  sticky = "nsew")
        self.delete_employee_button = Button(self.rightFrame2, text="Delete Employee", relief = "groove", font = "Arial", command=self.deleteUser)
        self.delete_employee_button.grid(row = 1, column = 0, sticky = "nsew")
        self.edit_user_info_bt = Button(self.rightFrame2, text="Edit Employee", relief = "groove", font = "Arial", command=self.editEmployeeDetials)
        self.edit_user_info_bt.grid(row = 1, column = 1, sticky = "nsew")
        self.remove_hours_btn = Button(self.rightFrame2, text="Remove Hours", relief = "groove", font = "Arial", command=lambda: self.ChangeHours(True))
        self.remove_hours_btn.grid(row = 2, column = 0, sticky = "nsew")

        self.number = 0

        # check if there are any employees in the database
        # if there is not then display no employees in the list list_box
        # If there are then display the employees
        dbList = dbFunctionsV2.getAllUsers()
        print(dbList)
        if len(dbList) > 0:
            # lets get a list of employees and display them
            self.viewAll()
            self.list_box.selection_set(0)
            self.showDetails(self.list_box.curselection()[0])
        else:
            self.list_box.insert(END, "No Employees in Database")

    # When a item in the list is clicked then show the data in the RIGHT TOP FRAME
    def showDetailsLive(self, event):
        # get list item number
        index = self.list_box.curselection()[0]
        # pass to showDetails function
        self.showDetails(index)

    # gets the information of the employee selected in the listbox and loads it into the right panel
    def showDetails(self, index):
        #get tme employee details from the selection
        name = self.names[index]
        ID = self.IDs[index]
        rate = self.rates[index]
        hol_rate = self.hol_rate[index]
        banked_hours = self.banked_hours[index]
        banked_salary = round(self.banked_salary[index], 2)
        #note event is passed but is not needed
        print("Hello dynamic label")
        try:
            # if the labels have already been created than destroy them so that another employees details can be
            # displayed
            self.employee_name.destroy()
            self.employee_ID.destroy()
            self.employee_rate.destroy()
            self.employee_hol_rate.destroy()
            self.employee_banked_hours.destroy()
            self.employee_banked_salary.destroy()
            print("Destroyed")
            # Now display the newly selected employees details in the right top panel
            # name
            self.employee_name = Label(self.rightFrame1, text=name, font = "Ariel", bg = "white")
            self.employee_name.grid(row = 3, column = 2, sticky = "w")
            # ID
            self.employee_ID = Label(self.rightFrame1, text=ID, font = "Ariel", bg = "white")
            self.employee_ID.grid(row = 2, column = 2, sticky = "w")
            # Rate
            self.employee_rate = Label(self.rightFrame1, text="£ {} per hour".format(rate), font = "Ariel", bg = "white")
            self.employee_rate.grid(row = 4, column = 2, sticky = "w")
            # holiday Hours
            self.employee_hol_rate = Label(self.rightFrame1, text="£ {} per hour".format(hol_rate), font = "Ariel", bg = "white")
            self.employee_hol_rate.grid(row = 5, column = 2, sticky = "w")
            # non holiday hours
            self.employee_banked_hours = Label(self.rightFrame1, text=banked_hours, font = "Ariel", bg = "white")
            self.employee_banked_hours.grid(row = 6, column = 2, sticky = "w")
            # total hours
            self.employee_banked_salary = Label(self.rightFrame1, text="£ {}".format(banked_salary), font = "Ariel", bg = "white")
            self.employee_banked_salary.grid(row = 7, column = 2, sticky = "w")

        except:
            # If it the first employee to be selected since the program was opened then you do not need to deastroy the
            # labels
            print("First Time")
            # name
            self.employee_name = Label(self.rightFrame1, text=name, font = "Ariel", bg = "white")
            self.employee_name.grid(row = 3, column = 2, sticky = "w")
            # ID
            self.employee_ID = Label(self.rightFrame1, text=ID, font = "Ariel", bg = "white")
            self.employee_ID.grid(row = 2, column = 2, sticky = "w")
            # Rate
            self.employee_rate = Label(self.rightFrame1, text="£ {} per hour".format(rate), font = "Ariel", bg = "white")
            self.employee_rate.grid(row = 4, column = 2, sticky = "w")
            # holiday Hours
            self.employee_hol_rate = Label(self.rightFrame1, text="£ {} per hour".format(hol_rate), font = "Ariel", bg = "white")
            self.employee_hol_rate.grid(row = 5, column = 2, sticky = "w")
            # non holiday hours
            self.employee_banked_hours = Label(self.rightFrame1, text=banked_hours, font = "Ariel", bg = "white")
            self.employee_banked_hours.grid(row = 6, column = 2, sticky = "w")
            # total hours
            self.employee_banked_salary = Label(self.rightFrame1, text="£ {}".format(banked_salary), font = "Ariel", bg = "white")
            self.employee_banked_salary.grid(row = 7, column = 2, sticky = "w")

    # When a window that has been previously called by the user e.g. new employee has been closed this function is
    # called. It grabs all the employees from the database and displays them in the list box (especially good if a new
    # employee has just been added). It then sets the previous selection in the listbox to the current selction and
    # grabs the data from the database and displays it in the top right panel
    def destroyTest(self, event):
        print("Testing Destroyed")
        self.viewAll()
        # self.showDetails(True)
        self.showDetails(self.currentSelectionIndex)
        self.list_box.select_set(self.currentSelectionIndex)

    # This function calls to the database and gets all the employee data from the database. It then puts thsi information
    # into lists, it then creates a list of lists and returns that to the caller
    def getLatestData(self):
        usersList = dbFunctionsV2.getAllUsers()
        self.names = []
        self.IDs = []
        self.rates = []
        self.hol_rate = []
        self.banked_hours = []
        self.banked_salary = []
        # put that into some List
        for a in usersList:
            self.names.append(a[1])
            self.IDs.append(a[0])
            self.rates.append(a[2])
            self.hol_rate.append(a[3])
            self.banked_hours.append(a[4])
            self.banked_salary.append(a[5])

        return (self.names, self.IDs, self.rates, self.hol_rate, self.banked_hours, self.banked_salary)

    # This function displays all the employees in the database into the list box
    def viewAll(self):
        # clear the list first
        self.list_box.delete(0, END)
        # get a list of the users from the database
        self.getLatestData()
        # the emumerate function gets the index from the list value, this index
        # is then used to get the corresponding ID value
        # This loop puts the employee name and ID into the list box for the user to select
        for (i, e) in enumerate(self.names):
            self.list_box.insert(END, "{} {}".format(self.IDs[i], e))

    # function that was used for some basic testing
    def add(self):
        self.number = self.number + 1
        #print(self.number)

    # function that was used for some basic testing
    def printNumber(self):
        return self.number

    # This function is called when the new Employee button is pressed in the bottom right panel
    def addTodB(self):
        # Get the value from the list_box
        selected = self.list_box.curselection()
        if selected:
            print(selected)
            for index in selected:
                print(self.list_box.get(index))
                name = self.list_box.get(index)
        else:
            name = "No Name"

        print("Open New Window")

        # Toplevel creates a window dependent on the Tk window
        root = Toplevel(self.window)
        # creates an instance of the UGUI class which opens the window to add an new employee
        userUpdateGUI = UGUI(root, name)
        # When the new employee window is closed the destroyNewUserWindow function is called
        root.bind("<Destroy>", self.destroyNewUserWindow)

    # When the add new employee window is closed this function is called
    # It selects the last employee in the listbox, which should be the new user and then shows their details
    def destroyNewUserWindow(self, message):
        self.viewAll()
        # self the last last item in the list which is the new users
        self.list_box.selection_set(len(self.names)-1)
        print(len(self.names))
        self.showDetails(self.list_box.curselection()[0])

    # This functions deletes the employee that is selected in the listbox
    def deleteUser(self):
        print("Are you sure???")
        # get the ID of the current employee selected
        currentID = str(self.IDs[self.list_box.curselection()[0]])
        # check is the user meant to hit the cancel button
        answer = messagebox.askyesno("Delete","Are you user you want to delete employee {}?".format(currentID))
        # if the user does not want to delete the user than exit without deleting
        if not answer:
            return
        # call the database delete function passing the employee to be deleted ID
        dbFunctionsV2.deleteUser(currentID)
        # display the updated list of employees
        self.viewAll()
        # if there are no employees left in the database need to blank the details labels in the
        # right top panel
        print("Length of ID Array: ", len(self.IDs))
        if len(self.IDs) == 0:
            self.employee_name.destroy()
            self.employee_ID.destroy()
            self.employee_rate.destroy()
            self.employee_hol_rate.destroy()
            self.employee_banked_hours.destroy()
            self.employee_banked_salary.destroy()
        else:
            # select first item in list
            self.list_box.selection_set(0)
            # show data for current selection
            self.showDetails(self.list_box.curselection()[0])

    # this function is called when the employee details are to be editted
    def editEmployeeDetials(self):
        # get the details of the current selected employee
        BankedHours = float(self.banked_hours[self.list_box.curselection()[0]])
        BankedSalary = float(self.banked_salary[self.list_box.curselection()[0]])
        currentID = self.IDs[self.list_box.curselection()[0]]
        rate = float(self.rates[self.list_box.curselection()[0]])
        hol_rate = float(self.hol_rate[self.list_box.curselection()[0]])
        currentName = self.names[self.list_box.curselection()[0]]
        root = Toplevel(self.window)
        # create an instance of the editEmployeeDetails class and pass the employees details to it
        # this will launch an edit employee window for the user
        newWindow = editEmployeeDetails(root, currentID, currentName, rate, hol_rate)
        # save the position of the current selected employee in the list box
        self.currentSelectionIndex = self.list_box.curselection()[0]
        # When the window for the edit employee is closed run detroyTest function
        root.bind("<Destroy>", self.destroyTest)

    def finish(self):
        self.window.destroy()

    # this function is called when the user wants to add or subtract hours from the employees Hours Bank.
    # when the add hours button is pressed this function is called with remove = False, if the remove hours
    # button is pressed then remove = True.
    def ChangeHours(self, remove):
        # get the data for the selected employee
        BankedHours = float(self.banked_hours[self.list_box.curselection()[0]])
        BankedSalary = float(self.banked_salary[self.list_box.curselection()[0]])
        currentID = self.IDs[self.list_box.curselection()[0]]
        rate = float(self.rates[self.list_box.curselection()[0]])
        hol_rate = float(self.hol_rate[self.list_box.curselection()[0]])
        #if remove True then remove hours, if false then add hours
        # open a new window
        root = Toplevel(self.window)
        # create an instance of the class ChnageHoursWindow where the change hours window is launched
        ChangeHours = ChangeHoursWindow(root, BankedHours, BankedSalary, currentID, rate, hol_rate, remove)
        # have the slection in the list box that the user make`
        self.currentSelectionIndex = self.list_box.curselection()[0]
        # when the window to change hours is destroyed run the destroyTest function
        root.bind("<Destroy>", self.destroyTest)


# This Class is for the Add Employee Window

class UGUI():

    def __init__(self, master, name):
        print("New Class")
        # define the window
        self.window = master
        self.window.title("New User")
        self.window.configure(background="white")
        self.window.configure(padx=10)
        self.window.configure(borderwidth = 1, relief = "solid")
        self.window.geometry('{}x{}'.format(280, 230))
        # fix the height and width of the grid
        self.window.grid_columnconfigure(0, weight = 1)
        self.window.grid_columnconfigure(1, weight = 1)
        self.window.grid_rowconfigure(0, weight = 1)
        self.window.grid_rowconfigure(1, weight = 1)
        self.window.grid_rowconfigure(2, weight = 1)
        self.window.grid_rowconfigure(4, weight = 1)
        self.window.grid_rowconfigure(5, weight = 1)
        self.window.grid_rowconfigure(6, weight = 1)
        self.window.grid_rowconfigure(7, weight = 1)

        # Labels of the window
        self.label_ID = Label(self.window, text="ID", bg = "white", font = ("Ariel", 12)).grid(row=0, column=0, sticky = "w")
        self.label_name = Label(self.window, text="Name", bg = "white", font = ("Ariel", 12)).grid(row=1, column=0, sticky = "w")
        self.label_rate = Label(self.window, text="Rate (£/hr)", bg = "white",font = ("Ariel", 12)).grid(row=2, column=0, sticky = "w")
        self.label_hol_rate = Label(self.window, text="Holiday Rate (£/hr)", bg = "white",font = ("Ariel", 12)).grid(row=3, column=0, sticky = "w")
        self.label_banked_hours = Label(self.window, text="Banked Hours", bg = "white",font = ("Ariel", 12)).grid(row=4, column=0, sticky = "w")
        self.label_banked_salary = Label(self.window, text="Banked Salary (£)", bg = "white",font = ("Ariel", 12)).grid(row=5, column=0, sticky = "w")

        #validation for Entry Boxes
        val = ValidationFunction()
        valName = self.window.register(val.alpha_space)
        rateVal = self.window.register(val.rateCheck)
        hourVal = self.window.register(val.hoursCheck)
        # Entry Boxes
        self.input_ID = Entry(self.window, borderwidth = 1, relief = "solid")
        self.input_ID.grid(row=0, column =1)
        self.input_name = Entry(self.window, borderwidth = 1, relief = "solid")
        self.input_name.configure(validate="key", validatecommand=(valName,'%P'))
        self.input_name.grid(row=1, column =1)
        self.input_rate = Entry(self.window, borderwidth = 1, relief = "solid", validate="key", validatecommand=(rateVal,'%P'))
        self.input_rate.grid(row=2, column =1)
        self.input_hol_rate = Entry(self.window, borderwidth = 1, relief = "solid", validate="key", validatecommand=(rateVal,'%P'))
        self.input_hol_rate.grid(row=3, column =1)
        self.input_banked_hours = Entry(self.window, borderwidth = 1, relief = "solid", validate="key", validatecommand=(hourVal,'%P'))
        self.input_banked_hours.grid(row=4, column =1)
        self.input_banked_salary = Entry(self.window, borderwidth = 1, relief = "solid", validate="key", validatecommand=(hourVal,'%P'))
        self.input_banked_salary.grid(row=5, column =1)
        # Button that when clicked creates the employee
        self.update_button = Button(self.window, text = "Create User", command=self.create, relief = "groove", font = ("Ariel",12))
        self.update_button.grid(row=6, column=0, columnspan = 2, sticky="nswe")

        # messagebox.showinfo("Please Enter all data", "TEST TEST TEST")

    def create(self):
        # This function is called when the user clicks on the create user button
        # first ensure that there is data in every field of the window
        if len(self.input_ID.get()) == 0 or len(self.input_name.get()) == 0 or len(self.input_rate.get()) == 0 or len(self.input_hol_rate.get()) == 0 or len(self.input_banked_hours.get()) == 0 or len(self.input_banked_salary.get()) == 0:
            messagebox.showwarning("Please Enter all data", "Please ensure that all entry boxes are filled, data has not been submitted", parent = self.window)
        else:
            # connect to the database and then check is a table exists
            dbFunctionsV2.connect()
            # connect to the database and add the employee to the database table with the information entered in the window
            dbFunctionsV2.addUser(self.input_ID.get(), self.input_name.get(), self.input_rate.get(), self.input_hol_rate.get(), self.input_banked_hours.get(), self.input_banked_salary.get())
            self.window.destroy()


# This class is used to open a window where current employees holiday and normal rates can be editted

class editEmployeeDetails():
    def __init__(self, master, importedID, importedName, importedRate, importedHolRate):
        self.ID = importedID
        # define the windows parameters
        self.name = importedName
        self.window = master
        # setup the grid configuration of the window
        # ensures the rows and columns are the correct size
        self.window.grid_columnconfigure(0, weight = 1)
        self.window.grid_columnconfigure(1, weight = 1)
        self.window.grid_rowconfigure(0, weight = 1)
        self.window.grid_rowconfigure(1, weight = 1)
        self.window.grid_rowconfigure(2, weight = 1)
        self.window.grid_rowconfigure(4, weight = 1)
        self.window.configure(bg = "white", padx = 10, borderwidth = 1, relief = "solid")
        self.window.geometry('{}x{}'.format(290, 160))
        self.window.title("Edit Employee Info")

        # Fixed labels
        self.ID_label = Label(self.window, text="ID", font = ("Ariel",12), bg = "White")
        self.ID_label.grid(row=0, column=0, sticky="w")

        self.Name_label = Label(self.window, text="Name", font = ("Ariel",12), bg = "White")
        self.Name_label.grid(row=1, column=0, sticky="w")

        self.rate_label = Label(self.window, text="Rate (£/hr)", font = ("Ariel",12), bg = "White")
        self.rate_label.grid(row=2, column =0, sticky="w")

        self.hol_rate_label = Label(self.window, text="Holiday Rate (£/hr)", font = ("Ariel",12), bg = "White")
        self.hol_rate_label.grid(row=3, column =0, sticky="w")

        # Dynamic named labels. Text changes depending on employee
        self.ID_l = Label(self.window, text=self.ID, font = ("Ariel",12), bg = "White")
        self.ID_l.grid(row=0, column=1, sticky="w")

        self.Name_l = Label(self.window, text=self.name, font = ("Ariel",12), bg = "White")
        self.Name_l.grid(row=1, column=1, sticky="w")

        # Validation of Both Rate Entry Boxs
        # Create an instance of the ValidationFunction Class
        val = ValidationFunction()
        # TCL wrapper around python function
        # val.rateCheck is a method from the ValidationFunction Class
        # set up the validation check of the rates entry boxes. This check will ensure that only numbers and one deciimal point are included
        rateVal = self.window.register(val.rateCheck)

        # entry boxs for rates. Includes the validate = key option, key means, run validation when any keystroke recorded
        # validate command is the command to pass the keystroke too to validate
        self.rate_entry = Entry(self.window, bg = "White" , borderwidth = 1, relief = "solid", validate = "key", validatecommand = (rateVal,'%P'))
        self.rate_entry.grid(row=2, column =1)
        self.hol_rate_entry = Entry(self.window, bg = "White", borderwidth = 1, relief = "solid", validate = "key", validatecommand = (rateVal,'%P'))
        self.hol_rate_entry.grid(row=3, column =1)

        # adds value into entry box
        self.hol_rate_entry.insert(END, importedHolRate)
        self.rate_entry.insert(END, importedRate)

        self.btn_update = Button(self.window, text="Update", command=self.edit_employee_details, font = ("Ariel",12), relief = "groove")
        self.btn_update.grid(row=4 , column = 0, columnspan = 2, sticky="we")



    # When the update button is pressed update the employee data in the database with the information in the Entry Boxes
    def edit_employee_details(self):
        # If there is no information in the Entry Boxes, throw error and do not proceed
        if len(self.rate_entry.get()) == 0 or len(self.hol_rate_entry.get()) == 0:
            messagebox.showwarning("Please Enter all data", "Please ensure that all entry boxes are filled, data has not been submitted", parent = self.window)
        else:
            # get the information the user has entered
            WindowID = self.ID
            WindowRate = float(self.rate_entry.get())
            WindowHolRate = float(self.hol_rate_entry.get())
            # update the database with that information
            dbFunctionsV2.editEmployee(WindowID, WindowRate, WindowHolRate)
            # quit out of that window
            self.window.destroy()

# This function is used to add or remove the amount of hours Banked and the amount of salary owed.

class ChangeHoursWindow():
# Sets up the properties of the window
    def __init__(self, master, importedBankedHours, importedBankedSalary, importedID, importedRate, importedHolRate, remove):
        # Get the employees data from the passed parameters
        self.banked_hours = importedBankedHours
        self.banked_salary = importedBankedSalary
        self.rate = importedRate
        self.hol_rate = importedHolRate
        self.ID = importedID
        self.window = master
        # Define the windows visuals and the layout of the grid
        self.window.configure(bg = "white", padx = 10, borderwidth = 1, relief = "solid")
        self.window.grid_columnconfigure(0, weight = 1)
        self.window.grid_columnconfigure(1, weight = 1)
        self.window.grid_rowconfigure(0, weight = 1)
        self.window.grid_rowconfigure(1, weight = 1)

        # This class is called when the program wants to add or remove hours from the employees HoursBank. This is affects
        # the layout and contents of the window
        if remove == True:
            # if hours are to be removed then use these settings to layout window
            self.window.geometry('{}x{}'.format(350, 100))
            self.window.title("Remove Hours")
            self.HoursToAdd = Label(self.window, text="Hours to Remove", bg = "White", font = ("Ariel", 12)).grid(row=0, column=0, sticky="w")
            self.window.configure(pady = 10)
        else:
            # if hours are to be added then use these settings to layout the window
            self.window.geometry('{}x{}'.format(350, 150))
            self.window.title("Add Hours")
            self.HoursToAdd = Label(self.window, text="Hours to Add", bg = "White", font = ("Ariel", 12)).grid(row=0, column=0, sticky="w")
            self.radioHeader = Label(self.window, text="Choice to add Holiday or non Holiday hours", bg = "White", font = ("Ariel", 12)).grid(row=1, column = 0, sticky="we", columnspan =2)
            # code to create the radio buttons
            options = ["Normal", "Holiday"]
            arrayOfRadioButtons = []
            # Tk variable
            self.v = IntVar()
            for ind, buttonName in enumerate(options,1):
                    arrayOfRadioButtons.append(Radiobutton(master, text=buttonName, padx = 20, variable = self.v, value=ind, bg = "White", font = ("Ariel", 12)))
                    arrayOfRadioButtons[ind-1].grid(row=2, column = ind -1 )

        # Use this entry box to enter the number of hours
        self.NewHours = Entry(self.window, borderwidth = 1, relief = "solid", font = ("Ariel", 12))
        self.NewHours.grid(row=0, column = 1, sticky="ew")
        # validate Entry
        # val is an instance of the ValidationFunction Class
        # val.rateCheck is a method from the ValidationFunction Class
        val = ValidationFunction()
        valCheck = self.window.register(val.hoursCheck)
        # set up the validation check of the NewHours Entry box. This check will ensure that only numbers and one deciimal point are included
        self.NewHours.configure(validate="key", validatecommand = (valCheck,'%P'))

        # options for window configure depending if its an add or remove window
        if remove == False:
            # for adding hours
            self.update_button = Button(self.window, text = "Add Hours", relief = "groove", font = "Ariel", command= lambda: self.ChangeHours(remove))
            self.update_button.grid(row=3, column=0, columnspan = 2, sticky = "we")
            self.window.grid_rowconfigure(2, weight = 1)
            self.window.grid_rowconfigure(3, weight = 1)
        else:
            # for removing hours
            self.update_button = Button(self.window, text = "Remove Hours", relief = "groove", font = ("Ariel", 12), command= lambda: self.ChangeHours(remove))
            self.update_button.grid(row=2, column=0, columnspan = 2, sticky = "nswe")

    # this fucntion is called when the add or remove hours button is pressed
    def ChangeHours(self, remove):
        # check to see if any hours are in the add hours entry box
        if len(self.NewHours.get()) == 0:
            messagebox.showwarning("Hours", "No hours have been entered, data has not been submitted", parent = self.window)
        else:
            print("Entered Hours ", self.NewHours.get())
            print(remove)
            # If the window is to add hours
            if remove == False:
                self.choice = self.v.get()
                #hours to be added are normal (not in holidays) hours
                if self.choice == 1:
                    print("Normal Hours","Test")
                    # add to the banked hours total
                    self.banked_hours += float(self.NewHours.get())
                    # calculate the new banked Salary total. Multiple the hours by the normal hourly rate and then
                    # add to the previous banked Salary
                    self.banked_salary = self.banked_salary + (float(self.NewHours.get())*self.rate)
                elif self.choice == 2:
                    print("Holiday Holiday")
                    # If the hours to be added are Holiday Hours
                    # Add the new hours to the hours total
                    self.banked_hours += float(self.NewHours.get())
                    # Multiple the hours by the holiday rate and then add them to the current Banked Salary total
                    self.banked_salary = self.banked_salary + (float(self.NewHours.get())*self.hol_rate)
                    print (self.banked_hours)
                    print (self.banked_salary)
                else:
                    # if no hours option has been selected
                    print("No Selection Made")
                    messagebox.showinfo("Warning", "Please Select Holiday or Normal")
            else:
                if float(self.NewHours.get()) > self.banked_hours:
                    messagebox.showinfo("Banked Hours", "There are not enough hours in the bank to remove specified hours, no changes have been made, please try again")
                    self.window.destroy()
                else:
                    # if the hours are to be removed
                    # Divide the Banked salary by the banked hours to get an average rate per hour
                    averageRate = self.banked_salary / self.banked_hours
                    # Multiple the average hourly rate by the hours to be removed to calculate the salary to remove
                    salaryReduction = averageRate * float(self.NewHours.get())
                    # calculate the new salary in the bank
                    self.banked_salary = self.banked_salary - salaryReduction
                    # subtract the banked hours by the hours entered in the entry box
                    self.banked_hours -= float(self.NewHours.get())
                    RoundedSalaryReduction = round(salaryReduction, 2)
                    # Display how much is to be paid to the employee after the banked hours have been removed
                    messagebox.showinfo("Salary Owed", "Money to be paid: £{}".format(RoundedSalaryReduction))
                    # update the employees database records with the new BankedHours and BankedSalary
            dbFunctionsV2.addHours(self.ID, self.banked_hours, self.banked_salary)
            self.window.destroy()

# This class contains all of the Entry box validation functions for the program

class ValidationFunction():

    # method is used to ensure that the input to the entry box is a letter or a space
    def alpha_space(self, data):
        print(data[-1])
        # check the last character typed in by the keyboard. If the key is a letter or a space then allow it to be entered
        if data[-1].isalpha() or data[-1].isspace():
            return True
        # if any other character is typed then dont allow it to be entered
        else:
            return False

    # mehtod is used to ensure that the rates entered are all numberic and have only one '.'
    def rateCheck(self, data):
        # if more than 1 '.' entered dont allow it to be displayed
        if data.count('.') > 1:
            return False
        # if the entry is greater than 0
        if len(data) > 0:
        # if the last character typed is a number or '.' (only one allowed) and the total entry string length is <6 then
        # validate
            if (data[-1].isnumeric() or data[-1] == ".") and len(data) < 6:
                return True
            else:
                return False
        else:
            return True

    # mehtod to check that the hours entry is numerical and has at the most one '.' character
    def hoursCheck(self, data):
        if data.count('.') > 1:
            return False
        if len(data) > 0:
            if (data[-1].isnumeric() or data[-1] == "."):
                return True
            else:
                return False
        else:
            return True


# main loop
# create a database if one doesnt Exist
dbFunctionsV2.connect()
# initialise Tkinter
window = Tk()
# open a main GUI window
my_gui = HoursBankGUI(window)
# run program
window.mainloop()
