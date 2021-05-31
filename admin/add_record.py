from tkinter import *
from tkinter import messagebox

from config_var import *

def add_record(self, menu_page):
    # Create Window
    global morning, night
    add_record_page = Toplevel()
    add_record_page.title('Add Record')
    add_record_page.geometry('600x580')
    add_record_page.config(bg=BGCOLOR)
    morning = StringVar()
    night = StringVar()
    Label(add_record_page, height=3, width=400, bg=HEADER_COLOR, text='Add Record', font=FONT).pack(pady=(0, 10))

    add_record_frame = Frame(add_record_page, bg=BGCOLOR)
    add_record_frame.pack()

    # Getting the Employee Id
    Label(add_record_frame, text='EMPLOYEE ID:', bg=BGCOLOR).grid(sticky='W', row=0, column=1, pady=(10, 0), padx=10)
    self.employee_id = Entry(add_record_frame, width=40)
    self.employee_id.grid(row=0, column=2, pady=(10, 0), columnspan=2)

    # Getting the password
    Label(add_record_frame, text='PASSWORD: ', bg=BGCOLOR).grid(sticky='W',row=1, column=1, pady=(10, 0), padx=10)
    self.password = Entry(add_record_frame, width=40)
    self.password.grid(row=1, column=2, pady=(10, 0), columnspan=2)

    # Getting the First Name
    Label(add_record_frame, text='FIRST NAME: ', bg=BGCOLOR).grid(sticky='W',row=2, column=1, pady=(10, 0), padx=10)
    self.first_name = Entry(add_record_frame, width=40)
    self.first_name.grid(row=2, column=2, pady=(10, 0), columnspan=2)

    # Getting the Last Name
    Label(add_record_frame, text='LAST NAME: ', bg=BGCOLOR).grid(sticky='W',row=3, column=1, pady=(10, 0), padx=10)
    self.last_name = Entry(add_record_frame, width=40)
    self.last_name.grid(row=3, column=2, pady=(10, 0), columnspan=2)

    # Sex
    Label(add_record_frame, text='SEX: ', bg=BGCOLOR).grid(sticky='W',row=4, column=1, pady=(10, 0), padx=10)
    self.sex.set('MALE')
    option = OptionMenu(add_record_frame, self.sex, 'MALE', 'FEMALE')
    option.grid(sticky='W',row=4, column=2, pady=(10, 0), columnspan=2)

    # Schedule
    Label(add_record_frame, text='SCHEDULE', bg=BGCOLOR, width=10).grid(row=5, column=2, pady=20, columnspan=2)

    # IN
    Label(add_record_frame, text='IN:', bg=BGCOLOR).grid(sticky='W', row=6, column=1)
    self.schedule_in = Entry(add_record_frame, width=10)
    self.schedule_in.grid(row=6, column=2, sticky='W')
    morning.set('AM')
    option_morning = OptionMenu(add_record_frame, morning, 'AM', 'PM')
    option_morning.grid(sticky='W', row=6, column=3, pady=(10, 0))


    # Out
    Label(add_record_frame, text='OUT:', bg=BGCOLOR).grid(sticky='W', row=7, column=1)
    self.schedule_out = Entry(add_record_frame, width=10)
    self.schedule_out.grid(sticky='W', row=7, column=2)
    night.set('PM')
    option_night = OptionMenu(add_record_frame, night, 'AM', 'PM')
    option_night.grid(sticky='W', row=7, column=3, pady=(10, 0))


    # Cancel Button
    Button(add_record_frame, text='Cancel', width=10,  bg='#e4bad4', command=lambda: [add_record_page.destroy(), menu_page.deiconify()]).grid(row=8, column=2, pady=(20, 0))

    # Save Button
    Button(add_record_frame, text='Save', bg='#AAFE92', width=10, command=lambda: [adding_record(self,add_record_page, menu_page)]).grid(row=8, column=3, pady=(20, 0))

    # check if user Exit the Window Manually
    add_record_page.protocol("WM_DELETE_WINDOW", lambda: [add_record_page.destroy(), menu_page.deiconify()])

    add_record_page.mainloop()

def unique_id(self, id):
    self.c.execute(f'SELECT employee_id FROM employees WHERE employee_id = "{id.get()}"')
    result = self.c.fetchall()
    if len(result) <= 0 and id.get() != '':
        return True
    self.connection.commit()

def adding_record(self, adding_page, menu):
    # adding records to the database

    #validation for time format, can't explain further XD
    if ':' in self.schedule_in.get():
        self.schedule_in = f"{self.schedule_in.get()} {morning.get()}"
    else:
        self.schedule_in = f"{self.schedule_in.get()}:00 {morning.get()}"

    if ':' in self.schedule_out.get():
        self.schedule_out = f"{self.schedule_out.get()} {night.get()}"
    else:
        self.schedule_out = f"{self.schedule_out.get()}:00 {night.get()}"

    if len(self.schedule_in) < 8:
        self.schedule_in = '0'+self.schedule_in

    if len(self.schedule_out) < 8:
        self.schedule_out = '0'+self.schedule_out
        
    if unique_id(self,self.employee_id):
        self.c.execute(f"""INSERT INTO employees VALUES(
        '{self.employee_id.get()}',
        '{self.password.get()}',
        '{self.first_name.get()}',
        '{self.last_name.get()}',
        '{self.sex.get()}',
        '{self.schedule_in}',
        '{self.schedule_out}'
        )""")
        # Apply Changes to the Database
        self.connection.commit()
        adding_page.destroy()
        menu.deiconify()
    else:
        messagebox.showerror('Error', 'Student Id Already Exist or Invalid Input')
        
