# Imports
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from datetime import datetime
import sqlite3

WINDOW_SIZE = '800x580'
FONT = ('Verdana', 15)
BGCOLOR='#EFEFEF'
HEADER_COLOR='#7EE5FF'

class Main:
    def __init__(self, main_page):
        # Student info initialization
        self.student_id = 0
        self.first_name = ''
        self.middle_name = ''
        self.last_name = ''
        self.course = ''
        self.section = ''

        # Time Initialization
        self.time_label = 0

        # Creating database & Table & connecting
        self.connection = sqlite3.connect('database.db')

        # Creating Cursor to the Database
        self.c = self.connection.cursor()
        try:
            # Creating Table
            self.c.execute("""CREATE TABLE students(
                    student_id text,
                    first_name text,
                    middle_name text,
                    last_name text,
                    course text,
                    section text
            )""")
            # Apply Changes to the Database
            self.connection.commit()

        except sqlite3.OperationalError:
            print('Table already made')

        # Application Logo
        self.app_logo = ImageTk.PhotoImage(Image.open('system daw eh.png').resize((150, 150), Image.ANTIALIAS))
        Label(main_page, image=self.app_logo, bg='#FAF1E6').place(x=325, y=50)

        # User name Entry
        Label(main_page, text='Username', bg='#FAF1E6').place(x=335, y=200)
        self.username = Entry(main_page, width=20)
        self.username.place(x=335, y=225)

        # Password Entry
        Label(main_page, text='Password', bg='#FAF1E6').place(x=335, y=275)
        self.password = Entry(main_page, width=20)
        self.password.place(x=335, y=300)

        # Log in Button
        login_button = Button(main_page, text='Login', width=10, bg='#E4EFE7', command=lambda: self.menu(main_page))
        login_button.place(x=355, y=340)

        # Exit Button
        exit_button = Button(main_page, text='Exit ', width=10,  bg='#E4EFE7', command=lambda: [main_page.destroy(), self.connection.close()])
        exit_button.place(x=355, y=385)

    def menu(self, main_page):
        if self.username.get() == '' and self.password.get() == '':
            # Hide Main Window
            main_page.withdraw()
            self.username.delete(0, END)
            self.password.delete(0, END)

            # Create Menu Window
            menu_page = Toplevel()
            menu_page.title('Student Attendance Monitoring System')
            menu_page.config(bg='#FAF1E6')
            menu_page.geometry(WINDOW_SIZE)
            menu_page.resizable(0, 0)

            # Current Time Label
            self.time_label = Label(menu_page, bg='#FAF1E6',font=FONT)
            self.time_label.place(x=500, y=10)
            self.current_time()

            button_h=4
            button_w=15

            # Logo
            Label(menu_page, image=self.app_logo, bg='#FAF1E6').place(x=580, y=150)

            # Add Button
            Button(menu_page, text='Add Record', bg='#FFC9C9', font=FONT, width=button_w, height=button_h, command=lambda: [menu_page.withdraw(), self.add_record(menu_page)]).place(x=80, y=100)

            # View Report Button
            Button(menu_page, text='View Report', bg='#FFFB78', font=FONT, width=button_w, height=button_h).place(x=80, y=230)

            # View Record Button
            Button(menu_page, text='View Record', bg='#8BFFBD', font=FONT, width=button_w, height=button_h, command=self.show_records).place(x=295, y=230)

            # Attendance
            Button(menu_page, text='Attendance', bg='#FF82E6', font=FONT, width=button_w, height=button_h).place(x=295, y=100)

            # Cancel Button
            Button(menu_page, text='Log Out', bg='#E4EFE7',command=lambda: [menu_page.destroy(), main_page.deiconify()]).place(x=50, y=500)

            # check if the Exit th Window Manually
            menu_page.protocol("WM_DELETE_WINDOW", lambda: [menu_page.destroy(), main_page.deiconify()])

            menu_page.mainloop()
        else:
            error = Label(main_page, text='Invalid Username or Password', fg='white', bg='#da7f8f', relief=RAISED)
            error.place(x=315, y=420)
            error.after(3000, error.destroy)

    def add_record(self, menu_page):
        # Create Window
        add_record_page = Toplevel()
        add_record_page.title('Add Record')
        add_record_page.geometry(WINDOW_SIZE)
        add_record_page.config(bg='#FAF1E6')

        # Getting the Student Id
        Label(add_record_page, text='STUDENT ID:', bg='#FAF1E6').place(x=150, y=50)
        self.student_id = Entry(add_record_page, width=40)
        self.student_id.place(x=250, y=50)

        # Getting the First Name
        Label(add_record_page, text='FIRST NAME: ', bg='#FAF1E6').place(x=150, y=150)
        self.first_name = Entry(add_record_page, width=40)
        self.first_name.place(x=250, y=150)

        # Getting the Middle Name
        Label(add_record_page, text='MIDDLE NAME: ', bg='#FAF1E6').place(x=150, y=200)
        self.middle_name = Entry(add_record_page, width=40)
        self.middle_name.place(x=250, y=200)

        # Getting the Last Name
        Label(add_record_page, text='LAST NAME: ', bg='#FAF1E6').place(x=150, y=250)
        self.last_name = Entry(add_record_page, width=40)
        self.last_name.place(x=250, y=250)

        # Getting the Course
        Label(add_record_page, text='COURSE: ', bg='#FAF1E6').place(x=150, y=300)
        self.course = Entry(add_record_page, width=40)
        self.course.place(x=250, y=300)

        # Getting the Section
        Label(add_record_page, text='SECTION: ', bg='#FAF1E6').place(x=150, y=350)
        self.section = Entry(add_record_page, width=40)
        self.section.place(x=250, y=350)

        # Cancel Button
        Button(add_record_page, text='Cancel', width=10, bg='#E4EFE7', command=lambda: [add_record_page.destroy(), menu_page.deiconify()]).place(x=300, y=400)

        # Save Button
        Button(add_record_page, text='Save', bg='#E4EFE7', width=10, command=lambda: [self.adding_record(), add_record_page.destroy(), menu_page.deiconify()]).place(x=400, y=400)

        # check if user Exit the Window Manually
        add_record_page.protocol("WM_DELETE_WINDOW", lambda: [add_record_page.destroy(), menu_page.deiconify()])

        add_record_page.mainloop()

    def adding_record(self):
        # adding records to the database
        self.c.execute(f"""INSERT INTO students VALUES(
        '{self.student_id.get()}',
        '{self.first_name.get()}',
        '{self.middle_name.get()}',
        '{self.last_name.get()}',
        '{self.course.get()}',
        '{self.section.get()}'
        )""")
        # Apply Changes to the Database
        self.connection.commit()

    def update_query(self,page,edit_page,update_id):

        response = messagebox.askyesno('UPDATE RECORD',f'ARE YOU SURE TO UPDATE RECORD FOR {update_id} ?')
        if(response):
            self.c.execute('''UPDATE students SET
                student_id = :student_id,
                first_name = :first_name,
                middle_name = :middle_name,
                last_name = :last_name,
                course = :course,
                section = :section

                WHERE student_id = :update_id''',
                {
                    'student_id':stud_id_edit.get(),
                    'first_name':first_name_edit.get(),
                    'middle_name':middle_name_edit.get(),
                    'last_name':last_name_edit.get(),
                    'course':course_edit.get(),
                    'section':section_edit.get(),
                    'update_id':update_id

                })
                
            self.connection.commit()
            print('success')
            page.destroy()
            edit_page.destroy()
            self.show_records()


    def edit_record(self,page,record_id):
        cell_size = 35
        table_col=3
        win_size='400x300'
        
        global stud_id_edit,first_name_edit,middle_name_edit,last_name_edit,course_edit,section_edit

        edit_record_page = Tk()
        edit_record_page.title('EDIT STUDENT RECORD')
        edit_record_page.geometry(win_size)
        edit_record_page.config(bg=BGCOLOR)
        Label(edit_record_page,text="STUDENT ID:").grid(row=2,column=table_col-1,padx=10,pady=(40,0 ))
        stud_id_edit=Entry(edit_record_page,width=cell_size)
        stud_id_edit.grid(row=2,column=table_col,pady=(40,0 ))

        Label(edit_record_page,text="FIRST NAME:").grid(row=3,column=table_col-1)
        first_name_edit=Entry(edit_record_page,width=cell_size)
        first_name_edit.grid(row=3,column=table_col)
        
        Label(edit_record_page,text="MIDDLE NAME:").grid(row=4,column=table_col-1)
        middle_name_edit=Entry(edit_record_page,width=cell_size)
        middle_name_edit.grid(row=4,column=table_col)

        Label(edit_record_page,text="LAST NAME:").grid(row=5,column=table_col-1)
        last_name_edit=Entry(edit_record_page,width=cell_size)
        last_name_edit.grid(row=5,column=table_col)

        Label(edit_record_page,text="COURSE:").grid(row=6,column=table_col-1)
        course_edit=Entry(edit_record_page,width=cell_size)
        course_edit.grid(row=6,column=table_col)

        Label(edit_record_page,text="SECTION:").grid(row=7,column=table_col-1)
        section_edit=Entry(edit_record_page,width=cell_size)
        section_edit.grid(row=7,column=table_col)

        self.c.execute(f"SELECT * FROM students WHERE student_id = '{record_id}'")
        records=self.c.fetchall()
        
        
        for record in records:
            stud_id_edit.insert(0,record[0])
            first_name_edit.insert(0,record[1])
            middle_name_edit.insert(0,record[2])
            last_name_edit.insert(0,record[3])
            course_edit.insert(0,record[4])
            section_edit.insert(0,record[5])

        
        Button(edit_record_page,text="SAVE",width=15,command=lambda id=record_id:self.update_query(page,edit_record_page,id),bg='#AAFE92').grid(row=8,column=table_col,pady=20)
        Button(edit_record_page,text="CANCEL",width=15,command=lambda:edit_record_page.destroy(),bg='#FE9292').grid(row=8,column=table_col-1,pady=20,padx=(35,0))
        edit_record_page.mainloop()

    def delete_query(self,page,record_id):
        response = messagebox.askyesno('DELETE RECORD','ARE YOU SURE TO DELETE THIS RECORD?')
        if(response):
            self.c.execute(f"DELETE FROM students WHERE student_id = '{record_id}'")
            self.connection.commit()         
            page.destroy()
            self.show_records()


    def show_records(self):
        cell_size = 22
        th_font ='Arial 12 bold'
        win_size='1100x600'
        table_bg_color = '#ffffff'
        show_record_page = Tk()
        show_record_page.title('SHOW RECORDS')
        show_record_page.geometry(win_size)
        show_record_page.config(bg=BGCOLOR)
        
        self.c.execute("SELECT * FROM students")
        records = self.c.fetchall()

        Label(show_record_page,bg=HEADER_COLOR,padx=500,pady=25,text="SHOW RECORDS").grid(row=4,column=5,columnspan=8)
        table_row=5
        
        Label(show_record_page,bg=BGCOLOR,text="STUDENT ID",font=th_font,pady=10).grid(row=table_row,column=5)
        Label(show_record_page,bg=BGCOLOR,text="FIRST NAME ",font=th_font,pady=10).grid(row=table_row,column=6)
        Label(show_record_page,bg=BGCOLOR,text="MIDDLE NAME ",font=th_font,pady=10).grid(row=table_row,column=7)
        Label(show_record_page,bg=BGCOLOR,text="LAST NAME ",font=th_font,pady=10).grid(row=table_row,column=8)
        Label(show_record_page,bg=BGCOLOR,text="COURSE",font=th_font,pady=10).grid(row=table_row,column=9)
        Label(show_record_page,bg=BGCOLOR,text="SECTION",font=th_font,pady=10).grid(row=table_row,column=10)
        
        for record in records:
            stud_id=Label(show_record_page,text=record[0],width=cell_size,bg=table_bg_color,padx=0)
            stud_id.grid(row=table_row+1,column=5)

            first_name=Label(show_record_page,text=record[1],width=cell_size,bg=table_bg_color)
            first_name.grid(row=table_row+1,column=6)

            middle_name=Label(show_record_page,text=record[2],width=cell_size,bg=table_bg_color)
            middle_name.grid(row=table_row+1,column=7)

            last_name=Label(show_record_page,text=record[3],width=cell_size,bg=table_bg_color)
            last_name.grid(row=table_row+1,column=8)

            course=Label(show_record_page,text=record[4],width=cell_size,bg=table_bg_color)
            course.grid(row=table_row+1,column=9)

            section=Label(show_record_page,text=record[5],width=cell_size,bg=table_bg_color)
            section.grid(row=table_row+1,column=10)

            Button(show_record_page,text="EDIT",command=lambda edit_id=record[0]: self.edit_record(show_record_page,edit_id),bg='#AAFE92').grid(row=table_row+1,column=11)
            Button(show_record_page,text="DELETE",command=lambda del_id=record[0]: self.delete_query(show_record_page,del_id),bg='#FE9292').grid(row=table_row+1,column=12)

            table_row+=1


        self.connection.commit()
        show_record_page.mainloop()

    def current_time(self):
        date_time_now = datetime.now()
        date_time_now = date_time_now.strftime('%I:%M:%S %p  %B %d, %Y')
        self.time_label.config(text=date_time_now)
        self.time_label.after(200, self.current_time)


root = Tk()
root.title('Student Attendance Monitoring System')
root.geometry(WINDOW_SIZE)
root.config(bg='#FAF1E6')
root.resizable(0, 0)
main = Main(root)
root.mainloop()
