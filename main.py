# Imports
from admin.show_record import *
from admin.attendance_record import *
from admin.add_record import *
from admin.view_report import *
from config_var import *
from employee.employees import *
from employee.time_in_out import *

from sqlite3.dbapi2 import Row
from tkinter import *
from tkinter import messagebox, ttk

from PIL import ImageTk, Image
from datetime import datetime, date
import sqlite3


class Main:
    def __init__(self):
        # Root window creation
        root = Tk()
        root.title('Employee Attendance Monitoring System')
        
        self.scr_w = root.winfo_screenwidth() # width of the screen
        self.scr_h = root.winfo_screenheight() # height of the screen
        x = int((self.scr_w/2) - (app_w/2))
        y = int((self.scr_h/2) - (app_h/2))
        self.WINDOW_SIZE = f'{app_w}x{app_h}+{x}+{y}'
        root.geometry(self.WINDOW_SIZE)
        
        root.title('Employee Attendance Monitoring System')
        root.config(bg=BGCOLOR)
        root.resizable(False, False)

        # Employee Information Initialization
        self.employee_id = ''
        self.password = ''
        self.first_name = ''
        self.last_name = ''
        self.sex = StringVar()
        self.schedule_in = ''
        self.schedule_out = ''
        # Creating database& Table & connecting
        self.connection = sqlite3.connect('database employee.db')

        # Creating Cursor to the Database
        self.c = self.connection.cursor()
        # Creating Table

        try:
            self.c.execute("""CREATE TABLE employees(
                                employee_id text,
                                password text,
                                first_name text,
                                last_name text,
                                sex text,
                                schedule_in,
                                schedule_out,
                                work_status text,
                               )""")
            self.connection.commit()

        except sqlite3.OperationalError:
            print('Table already made')

        #create table for employee attendance
        try:
            self.c.execute("""CREATE TABLE employee_attendance(
                                employee_id text,
                                attendance_date text,
                                time_in text,
                                status text
                               )""")
            self.connection.commit()

        except sqlite3.OperationalError:
            print('Table for attendance already made')

        else:
            # Creating admin account
            # self.c.execute(f"""INSERT INTO employees VALUES(
            # 'admin',
            # '1234',
            # 'Steven',
            # 'Serrano',
            # 'MALE',
            # 'MANAGER',
            # 'MANAGER'
            # )""")
            # self.connection.commit()
            pass

        # App Logo
        self.app_logo = ImageTk.PhotoImage(Image.open('logo.png').resize((180, 180), Image.ANTIALIAS))

        #button imagess
        self.cancel_img = ImageTk.PhotoImage(Image.open("btn/cancel_btn.png").resize((btn_w, btn_h), Image.ANTIALIAS))
        self.delete_img = ImageTk.PhotoImage(Image.open("btn/delete_btn.png").resize((btn_w, btn_h), Image.ANTIALIAS))
        self.edit_img = ImageTk.PhotoImage(Image.open("btn/edit_btn.png").resize((btn_w, btn_h), Image.ANTIALIAS))
        self.exit_img = ImageTk.PhotoImage(Image.open("btn/exit_btn.png").resize((btn_w, btn_h+5), Image.ANTIALIAS))
        self.login_img = ImageTk.PhotoImage(Image.open("btn/login_btn.png").resize((btn_w, btn_h+5), Image.ANTIALIAS))
        self.logout_img = ImageTk.PhotoImage(Image.open("btn/logout_btn.png").resize((btn_w, btn_h), Image.ANTIALIAS))
        self.save_img = ImageTk.PhotoImage(Image.open("btn/save_btn.png").resize((btn_w, btn_h), Image.ANTIALIAS))
        self.back_img = ImageTk.PhotoImage(Image.open("btn/back_btn.png").resize((btn_h, btn_h), Image.ANTIALIAS))


        # Opening root window
        self.starting(root)

    def starting(self, root):
        global username, password
        # Creating frame to center widgets
        login_bg = ImageTk.PhotoImage(Image.open('bg/login_bg.png').resize((1000, 580), Image.ANTIALIAS))
        # login_img = ImageTk.PhotoImage(Image.open('bts_biot/login_btn.png').resize((80, 30), Image.ANTIALIAS))
        # exit_img = ImageTk.PhotoImage(Image.open('bts_biot/exit_btn.png').resize((80, 30), Image.ANTIALIAS))
        login_bg_lbl = Label(root,image=login_bg)
        login_bg_lbl.place(x=0,y=0)
        # main_frame = Frame(root)
        # main_frame.pack()

        
        # Application Logo
        # Label(main_frame, image=self.app_logo, bg=BGCOLOR).grid(row=0, column=1,pady=(50,0))

        # User name Entry
        # Label(root, text='Username/ID', bg=BGCOLOR).grid(row=1, column=1, pady=(20, 10), padx=(50, 180))
        username = Entry(root, width=30, bd=0)
        username.pack(pady=(260,50))

        # Password Entry
        # Label(root, text='Password', bg=BGCOLOR).grid(row=3, column=1,pady=(20, 10), padx=(50, 180))
        password = Entry(root, width=30, show="*",bd=0)
        password.pack(pady=(0,30))

        # Log in Button
        login_button = Button(root, image=self.login_img, border=0,bg='#FFFFFF', command=lambda: [self.menu(root)])
        login_button.pack(pady=5)

        # Exit Button
        exit_button = Button(root, image=self.exit_img, border=0,bg='#FFFFFF', command=lambda: [root.destroy(), self.connection.close()])
        exit_button.pack()

        # Hover ek ek
        login_button.bind("<Enter>", self.enter)
        login_button.bind("<Leave>", self.exit)
        exit_button.bind("<Enter>", self.enter)
        exit_button.bind("<Leave>", self.exit)

        # pressing Enter key will trigger the menu function, same what login button does
        global temp_root
        temp_root=root
        password.bind('<Return>',self.pressed_enter)
        username.bind('<Return>',self.pressed_enter)
        
        root.mainloop()

    def pressed_enter(self,e):
        self.menu(temp_root)

    def enter(self, e):
        e.widget['background'] = '#e1e5ea'

    def exit(self, e):
        e.widget['background'] = BGCOLOR

    def menu(self, root):
        # Checking if the Username exist
        self.c.execute(f"SELECT * FROM employees WHERE employee_id = '{username.get()}'")
        content = self.c.fetchone()
        self.connection.commit()

        if content != None and username.get() != '' and password != '':
            # Checking if it is an admin account
            if username.get() == 'admin' and password.get() == content[1]:
                # Hide Main Window
                root.withdraw()
                username.delete(0, END)
                password.delete(0, END)

                # Create Menu Window
                menu_page = Toplevel()
                menu_page.title('Employee Attendance Monitoring System')
                menu_page.config(bg=BGCOLOR)
                menu_page.geometry(self.WINDOW_SIZE)

                # CREATING FRAME TO CENTER WIDGETS
                menu_frame = Frame(menu_page, bg=BGCOLOR)
                menu_frame.pack()

                # Current Time Label
                time_label = Label(menu_frame, bg=BGCOLOR,font=FONT)
                time_label.grid(row=0, column=3, pady=20)
                self.current_time(time_label)

                button_h=110
                button_w=250

                # Logo
                Label(menu_frame, image=self.app_logo, bg=BGCOLOR).grid(row=1, column=3, rowspan=2,pady=(50,0))

                # Add Button
                add_record_img = ImageTk.PhotoImage(Image.open("btn/add_record_btn.png").resize((button_w, button_h), Image.ANTIALIAS))
                add_button = Button(menu_frame, image=add_record_img, bg=BGCOLOR, border=0,command=lambda: [menu_page.withdraw(), add_record(self,menu_page)])
                add_button.grid(row=1, column=1, pady=(50,10), padx=10)

                # View Report Button
                view_report_img = ImageTk.PhotoImage(Image.open('btn/view_report_btn.png').resize((button_w, button_h), Image.ANTIALIAS))
                view_report_button = Button(menu_frame, image=view_report_img, bg=BGCOLOR, border=0,command=lambda: [menu_page.withdraw(), view_report(self,menu_page)])
                view_report_button.grid(row=1, column=2, pady=(50,10), padx=10)

                # View Record Button
                view_record_img = ImageTk.PhotoImage(Image.open('btn/view_record_btn.png').resize((button_w, button_h), Image.ANTIALIAS))
                view_button = Button(menu_frame, image=view_record_img, bg=BGCOLOR, border=0,command=lambda: [menu_page.withdraw(), show_records(self,menu_page)], relief=RAISED)
                view_button.grid(row=2, column=1, pady=2, padx=10)

                # Attendance
                attendance_img = ImageTk.PhotoImage(Image.open('btn/attendance_btn.png').resize((button_w, button_h), Image.ANTIALIAS))
                attendance_button = Button(menu_frame, image=attendance_img, bg=BGCOLOR, border=0, command=lambda: [attendance_record(self,menu_page, "", ""), menu_page.withdraw()])
                attendance_button.grid(row=2, column=2, pady=2, padx=10)

                # logout Button
                Button(menu_frame, image=self.logout_img, bg=BGCOLOR,bd=0,command=lambda: [menu_page.destroy(), root.deiconify()]).grid(row=3, column=1,padx=10,pady=20,sticky=W)

                # check if the Exit th Window Manually
                menu_page.protocol("WM_DELETE_WINDOW", lambda: [menu_page.destroy(), root.deiconify()])

                # Hover ek ek
                add_button.bind("<Enter>", self.enter)
                add_button.bind("<Leave>", self.exit)
                view_report_button.bind("<Enter>", self.enter)
                view_report_button.bind("<Leave>", self.exit)
                view_button.bind("<Enter>", self.enter)
                view_button.bind("<Leave>", self.exit)
                attendance_button.bind("<Enter>", self.enter)
                attendance_button.bind("<Leave>", self.exit)
                menu_page.mainloop()
            elif username.get() != 'admin' and content[0] == username.get() and content[1] == password.get():
                # Hide Main Window
                root.withdraw()
                username.delete(0, END)
                password.delete(0, END)

                # THIS IS AN EMPLOYEE ACCOUNT
                self.employee_page(root, content[0])
            else:
                messagebox.showwarning('Warning', 'Invalid Password')
        else:
            messagebox.showwarning('Warning', 'Invalid Password')

    def employee_page(self, root, id):
        # Fetch employee profile
        self.c.execute(f"SELECT * FROM employees WHERE employee_id = '{id}'")
        content = self.c.fetchone()
        # Create Employee  Window
        employee_menu_page = Toplevel()
        employee_menu_page.title('Employee Attendance Monitoring System')
        employee_menu_page.config(bg=BGCOLOR)
        emp_page_w = 600
        emp_page_h = 500
        x = int((self.scr_w/2) - (emp_page_w/2))
        y = int((self.scr_h/2) - (emp_page_h/2))
        employee_menu_page.geometry(f'{emp_page_w}x{emp_page_h}+{x}+{y}')
        employee_menu_page.resizable(False, False)

        time_in_img = ImageTk.PhotoImage(Image.open("btn/button_time-in.png").resize((200, 66), Image.ANTIALIAS))
        time_out_img = ImageTk.PhotoImage(Image.open("btn/button_time-out.png").resize((200, 66), Image.ANTIALIAS))
        view_record_img = ImageTk.PhotoImage(Image.open("btn/button_view-records.png").resize((150, 40), Image.ANTIALIAS))
        edit_profile_img = ImageTk.PhotoImage(Image.open("btn/button_edit-profile.png").resize((150, 40), Image.ANTIALIAS))
        change_pass_img = ImageTk.PhotoImage(Image.open("btn/button_change-password.png").resize((150, 40), Image.ANTIALIAS))

        Label(employee_menu_page, height=3, width=400, bg=HEADER_COLOR, text='EMPLOYEE', font=FONT).pack(pady=(0, 10))

        employee_menu_frame = Frame(employee_menu_page, bg=BGCOLOR)
        employee_menu_frame.pack()

        # Header
        Label(employee_menu_frame, text='WELCOME,', bg=BGCOLOR, font=FONT).grid(sticky='W', row=0, column=0,
                                                                                  columnspan=2)
        Label(employee_menu_frame, text=f'{content[2].upper()} {content[3].upper()}', bg=BGCOLOR, font=FONT).grid(sticky='W', row=1, column=1, padx=(0,5))
        
        Label(employee_menu_frame, text=f'YOUR SCHEDULE: {content[5]} to {content[6]}', bg=BGCOLOR,).grid(sticky='W', row=2, column=0, pady=(5, 20),padx=5,
                                                                                  columnspan=2)

        # time and date today
        emp = Label(employee_menu_frame, bg=BGCOLOR, font=('Verdana', 10), width=40)
        emp.grid(row=3, column=1, columnspan=2)
        self.current_time(emp)

        # time in button
        Button(employee_menu_frame, image=time_in_img, border=0, bg=BGCOLOR,
               font=('Verdana', 10),command=lambda: time_in_query(self, id)).grid(sticky='W', row=4, column=1, rowspan=2, pady=10, padx=20)

        # time out button
        Button(employee_menu_frame, image=time_out_img,border=0, bg=BGCOLOR,
               font=('Verdana', 10), command=lambda: time_out_query(self, id)).grid(sticky='W', row=6, column=1, pady=10, rowspan=2, padx=20)

        # View Records Button
        Button(employee_menu_frame,image=view_record_img, bg=BGCOLOR, border=0, command=lambda: employee_records(self, content[0])).grid(sticky='S', row=4, column=2,
                                                                                      pady=10, padx=20)

        # Edit Profile Button
        Button(employee_menu_frame, image=edit_profile_img, bg=BGCOLOR, border=0,
               command=lambda: [edit_profile(self, content[0], root,employee_menu_page)]).grid(sticky='N', row=5, column=2,
                                                                                         pady=10, padx=20)

        # Edit Password Button
        Button(employee_menu_frame, image=change_pass_img, bg=BGCOLOR, border=0, command=lambda: edit_password(self, id,employee_menu_page)).grid(sticky='N', row=6, column=2,
                                                                                         pady=10, padx=20)
                                                                            
        Button(employee_menu_frame, image=self.logout_img, bg=BGCOLOR,border=0, command=lambda: [employee_menu_page.destroy(), root.deiconify()]).grid(row=7, column=2)
        # check if the Exit th Window Manually
        employee_menu_page.protocol("WM_DELETE_WINDOW", lambda: [employee_menu_page.destroy(), root.deiconify()])

        employee_menu_page.mainloop()

    def current_time(self, time_label):
        date_time_now = datetime.now()
        date_time_now = date_time_now.strftime('%A %I:%M %p  %B %d, %Y')
        time_label.config(text=date_time_now)
        time_label.after(200, self.current_time, time_label)

    def treeview_sort_column(self,tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda _col=col: self.treeview_sort_column(tv, _col, not reverse))

        
if __name__ == '__main__':
    main = Main()

