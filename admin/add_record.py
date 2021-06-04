from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

from config_var import *

def add_record(self, menu_page):
    # Create Window
    BGCOLOR='#ffffff'
    add_record_page = Toplevel()
    add_record_page.title('Add Record')
    add_record_page.geometry('600x580')
    add_record_page.config(bg=BGCOLOR)

    # Label(add_record_page, height=3, width=400, bg=HEADER_COLOR, text='Add Record', font=FONT).pack(pady=(0, 10))
    add_record_bg_img = PhotoImage(file='bg/add_record_bg.png')
    Label(add_record_page,image=add_record_bg_img).place(x=0,y=0)

    add_record_frame = Frame(add_record_page,bg=BGCOLOR)
    add_record_frame.pack(pady=(110,0))

    # Getting the Employee Id
    Label(add_record_frame, text='EMPLOYEE ID:', bg=BGCOLOR).grid(sticky='W', row=0, column=1, padx=10)
    self.employee_id = Entry(add_record_frame, width=40)
    self.employee_id.grid(row=0, column=2, pady=(10, 0), columnspan=2)

    # Getting the password
    Label(add_record_frame, text='PASSWORD: ', bg=BGCOLOR).grid(sticky='W',row=1, column=1, padx=10)
    self.password = Entry(add_record_frame, width=40)
    self.password.grid(row=1, column=2, pady=(10, 0), columnspan=2)

    # Getting the First Name
    Label(add_record_frame, text='FIRST NAME: ', bg=BGCOLOR).grid(sticky='W',row=2, column=1, padx=10)
    self.first_name = Entry(add_record_frame, width=40)
    self.first_name.grid(row=2, column=2, pady=(10, 0), columnspan=2)

    # Getting the Last Name
    Label(add_record_frame, text='LAST NAME: ', bg=BGCOLOR).grid(sticky='W',row=3, column=1, padx=10)
    self.last_name = Entry(add_record_frame, width=40)
    self.last_name.grid(row=3, column=2, pady=(10, 0), columnspan=2)

    # Sex
    sex_options = ['MALE','FEMALE']
    Label(add_record_frame, text='SEX: ', bg=BGCOLOR).grid(sticky='W',row=4, column=1, padx=10)
    self.sex = ttk.Combobox(add_record_frame,value=sex_options,width=10,state="readonly",)
    self.sex.grid(sticky='W',row=4, column=2, pady=(10, 0), columnspan=2)
    self.sex.current(0)

    # Schedule
    Label(add_record_frame, text='SCHEDULE', bg=BGCOLOR, width=10).grid(row=5, column=1, pady=20, columnspan=3)


    hr_options = ['01','02','03','04','05','06','07','08','09','11','12']
    min_options = ['00','15','30','45']
    period_options = ['AM','PM']

    # IN
    in_row = 6
    Label(add_record_frame, text='IN:', bg=BGCOLOR).grid(row=in_row, column=1)
    self.schedule_in_hr = ttk.Combobox(add_record_frame, value=hr_options, width=3,state="readonly",background='#ffffff')
    self.schedule_in_hr.current(0)
    self.schedule_in_hr.grid(row=in_row, column=2, sticky='W')
    Label(add_record_frame,text=":",bg=BGCOLOR).grid(row=in_row, column=2,padx=2)
    self.schedule_in_min = ttk.Combobox(add_record_frame, value=min_options, width=3)
    self.schedule_in_min.current(0)
    self.schedule_in_min.grid(row=in_row, column=2, sticky='E')

    self.in_period = ttk.Combobox(add_record_frame, value=period_options,width=5,state="readonly")
    self.in_period.current(0)
    self.in_period.grid(sticky='W', row=6, column=3,padx=10)


    # Out
    out_row = in_row+1
    Label(add_record_frame, text='OUT:', bg=BGCOLOR).grid(row=out_row, column=1,pady=10)
    self.schedule_out_hr = ttk.Combobox(add_record_frame, value=hr_options, width=3,state="readonly")
    self.schedule_out_hr.current(0)
    self.schedule_out_hr.grid(row=out_row, column=2, sticky='W')
    Label(add_record_frame,text=":",bg=BGCOLOR).grid(row=out_row, column=2,padx=2)
    self.schedule_out_min = ttk.Combobox(add_record_frame, value=min_options, width=3)
    self.schedule_out_min.current(0)
    self.schedule_out_min.grid(row=out_row, column=2, sticky='E')
    
    self.out_period = ttk.Combobox(add_record_frame, value=period_options,width=5,state="readonly")
    self.out_period.current(0)
    self.out_period.grid(sticky='W', row=out_row, column=3,padx=10)


    # Cancel Button
    Button(add_record_frame, image=self.cancel_img, bd=0, bg=BGCOLOR, command=lambda: [add_record_page.destroy(), menu_page.deiconify()]).grid(row=8, column=1, padx=(20,0), pady=(35,0))

    # Save Button
    Button(add_record_frame, image=self.save_img, bd=0, bg=BGCOLOR, command=lambda: [adding_record(self,add_record_page, menu_page)]).grid(row=8, column=3, pady=(35,0))

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

    try:
        in_min=int(self.schedule_in_min.get())
        out_min=int(self.schedule_out_min.get())
        if(in_min>=60 or out_min>=60):
            messagebox.showerror('INVALID','Invalid Minute! \nMust less than 60')
            return

    except:
        messagebox.showerror('INVALID','Invalid Minute! \nMust contain only numbers')
        return

    self.schedule_in = f'{self.schedule_in_hr.get()}:{self.schedule_in_min.get()} {self.in_period.get()}'

    self.schedule_out = f'{self.schedule_out_hr.get()}:{self.schedule_out_min.get()} {self.out_period.get()}'

    if unique_id(self,self.employee_id):
        self.c.execute(f"""INSERT INTO employees VALUES(
        '{self.employee_id.get()}',
        '{self.password.get()}',
        '{self.first_name.get()}',
        '{self.last_name.get()}',
        '{self.sex.get()}',
        '{self.schedule_in}',
        '{self.schedule_out}',
        'active'
        )""")
        # Apply Changes to the Database
        
        self.connection.commit()
        response = messagebox.askyesno('Successfully added in the Database','Success! Register Another Employee?')
        if(not response):
            adding_page.destroy()
            menu.deiconify()
            return
        
        self.employee_id.delete(0,'end')
        self.password.delete(0,'end')
        self.first_name.delete(0,'end')
        self.last_name.delete(0,'end')


    else:
        messagebox.showerror('Error', 'Student Id Already Exist or Invalid Input')
        
