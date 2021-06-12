from tkinter import *
from tkinter import messagebox, ttk
from config_var import *

def update_query(self,edit_page,update_id):
    print(password_edit.get())
    response = messagebox.askyesno('UPDATE RECORD',f'ARE YOU SURE TO UPDATE RECORD FOR {update_id} ?')
    if(response):
        self.c.execute('''UPDATE employees SET
            employee_id = :employee_id,
            password = :password,
            first_name = :first_name,
            last_name = :last_name,
            sex = :sex,
            schedule_in = :schedule_in,
            schedule_out = :schedule_out,
            work_status = :work_status

                WHERE employee_id = :update_id''',
            {
                'employee_id': employee_id_edit.get(),
                'password': password_edit.get(),
                'first_name': first_name_edit.get(),
                'last_name': last_name_edit.get(),
                'sex': sex_edit.get(),
                'schedule_in': schedule_in_edit.get(),
                'schedule_out': schedule_out_edit.get(),
                'work_status': work_status_edit.get(),

                'update_id': update_id
            })
        self.c.execute("UPDATE employee_attendance SET employee_id = ? WHERE employee_id = ?", (employee_id_edit.get(), update_id))

        selected = self.tree.focus()
        self.tree.item(selected,text='',values=(employee_id_edit.get(),first_name_edit.get(),
                                                last_name_edit.get(),sex_edit.get(),
                                                schedule_in_edit.get(),schedule_out_edit.get(),
                                                work_status_edit.get()))

        self.connection.commit()
        print('success')
        edit_page.destroy()


def edit_record(self):
    try:
        record_tree = self.tree.selection()[0]
    except:
        messagebox.showinfo('Invalid', 'Please Select a Row in the Table First')
        return

    record = self.tree.item(record_tree)
    id = record['values'][0]
    cell_size = 35
    table_col=3
    edit_page_w = 500
    edit_page_h = 300
    x = int((self.scr_w/2) - (edit_page_w/2))
    y = int((self.scr_h/2) - (edit_page_h/2))
    win_size=f'{edit_page_w}x{edit_page_h}+{x}+{y}'
    global employee_id_edit,password_edit,first_name_edit,last_name_edit,sex_edit,schedule_in_edit,schedule_out_edit,work_status_edit, hide
    hide = 1
    edit_record_page = Toplevel()
    edit_record_page.title('EDIT EMPLOYEE RECORD')
    edit_record_page.geometry(win_size)
    edit_record_page.config(bg=BGCOLOR)

    edit_record_frame = Frame(edit_record_page,bg=BGCOLOR)
    edit_record_frame.pack()

    Label(edit_record_frame,text="EMPLOYEE ID:",bg=BGCOLOR).grid(row=2,column=table_col-1,padx=10,pady=(40,0 ))
    employee_id_edit=Entry(edit_record_frame, width=cell_size)
    employee_id_edit.grid(row=2, column=table_col, pady=(40, 0))

    Label(edit_record_frame,text="PASSWORD:",bg=BGCOLOR).grid(row=3,column=table_col-1)
    password_edit=Entry(edit_record_frame, width=cell_size)
    password_edit.grid(row=3, column=table_col,sticky=W)

    password_edit['show'] = '•'

    check_box = Checkbutton(edit_record_frame,command=lambda :hides(record[1], check_box),variable=BooleanVar(),bg=BGCOLOR)
    check_box.grid(row=3, column=table_col,sticky=E)
    
    Label(edit_record_frame,text="FIRST NAME:",bg=BGCOLOR).grid(row=4,column=table_col-1)
    first_name_edit=Entry(edit_record_frame, width=cell_size)
    first_name_edit.grid(row=4, column=table_col)

    Label(edit_record_frame,text="LAST NAME:",bg=BGCOLOR).grid(row=5,column=table_col-1)
    last_name_edit=Entry(edit_record_frame,width=cell_size)
    last_name_edit.grid(row=5,column=table_col)

    Label(edit_record_frame,text="SEX:",bg=BGCOLOR).grid(row=6,column=table_col-1)
    sex_edit=Entry(edit_record_frame, width=cell_size)
    sex_edit.grid(row=6, column=table_col)

    Label(edit_record_frame,text="SCHEDULE IN:",bg=BGCOLOR).grid(row=7,column=table_col-1)
    schedule_in_edit=Entry(edit_record_frame, width=cell_size)
    schedule_in_edit.grid(row=7, column=table_col)

    Label(edit_record_frame, text="SCHEDULE OUT:",bg=BGCOLOR).grid(row=8, column=table_col - 1)
    schedule_out_edit = Entry(edit_record_frame, width=cell_size)
    schedule_out_edit.grid(row=8, column=table_col)

    Label(edit_record_frame, text="WORKING STATUS:",bg=BGCOLOR).grid(row=9, column=table_col - 1)
    work_status_edit= Entry(edit_record_frame, width=cell_size)
    work_status_edit.grid(row=9, column=table_col)



    self.c.execute(f"SELECT * FROM employees WHERE employee_id = '{id}'")
    records=self.c.fetchall()
    for record in records:
        employee_id_edit.insert(0, record[0])
        password_edit.insert(0, record[1])
        first_name_edit.insert(0, record[2])
        last_name_edit.insert(0,record[3])
        sex_edit.insert(0, record[4])
        schedule_in_edit.insert(0, record[5])
        schedule_out_edit.insert(0, record[6])
        work_status_edit.insert(0,record[7])

    
    Button(edit_record_frame,image=self.cancel_img,bd=0,command=lambda:edit_record_page.destroy(),bg=BGCOLOR).grid(row=11,column=table_col-1,pady=20,padx=(40,0))
    Button(edit_record_frame,image=self.save_img,bd=0,command=lambda :update_query(self,edit_record_page,id),bg=BGCOLOR).grid(row=11,column=table_col,pady=20,padx=(20,0))

def hides(password, checkbox):
    global hide
    if hide == 1:
        password_edit['show'] = ''
        hide= 0
    else:
        password_edit['show'] = '•'
        hide = 1

def delete_query(self):
    try:
        record_tree = self.tree.selection()[0]
    except:
        messagebox.showinfo('Invalid', 'Please Select a Row in the Table First')
        return

    record = self.tree.item(record_tree)
    id = record['values'][0]
    response = messagebox.askyesno('DELETE RECORD',f'Delete Record for [{id}] ?')
    if(response):
        self.tree.delete(record_tree)
        self.c.execute(f"DELETE FROM employees WHERE employee_id = '{id}'")
        self.connection.commit()
        self.c.execute(f"DELETE FROM employee_attendance WHERE employee_id = '{id}'")
        self.connection.commit()


def show_records(self, root_page):
    cell_size = 150
    mid_cell_size = 25
    global hidden
    hidden = 0
    show_record_page = Toplevel()
    show_record_page.title('SHOW RECORDS')
    show_record_page.geometry(self.WINDOW_SIZE)
    show_record_page.config(bg=BGCOLOR)
    show_record_frame=Frame(show_record_page,bg=BGCOLOR)
    show_record_frame.pack()
    Label(show_record_frame, height=3, width=600, bg=HEADER_COLOR, text='EMPLOYEE RECORDS', font=FONT).pack(pady=(0, 10))
    #for table's scrollbar
    scrollbary = Scrollbar(show_record_frame, orient=VERTICAL)
    # hide password

    self.tree = ttk.Treeview(show_record_frame,selectmode=BROWSE,yscrollcommand=scrollbary.set,height=20)
    scrollbary.config(command=self.tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    self.tree['columns'] = ('EMPLOYEE ID', 'FIRST NAME', 'LAST NAME', 'SEX', 'SCHEDULE IN','SCHEDULE OUT','WORK STATUS')
    self.tree.column('#0',width=0,stretch=NO)
    self.tree.column('EMPLOYEE ID',width=cell_size,minwidth=mid_cell_size,anchor=CENTER)
    self.tree.column('FIRST NAME',width=cell_size,minwidth=mid_cell_size,anchor=W)
    self.tree.column('LAST NAME',width=cell_size,minwidth=mid_cell_size,anchor=W)
    self.tree.column('SEX',width=cell_size-50,minwidth=mid_cell_size,anchor=CENTER)
    self.tree.column('SCHEDULE IN',width=cell_size,minwidth=mid_cell_size,anchor=CENTER)
    self.tree.column('SCHEDULE OUT',width=cell_size,minwidth=mid_cell_size,anchor=CENTER)
    self.tree.column('WORK STATUS',width=cell_size-50,minwidth=mid_cell_size,anchor=CENTER)

    self.tree.heading('#0',text='')
    self.tree.heading('EMPLOYEE ID',text='EMPLOYEE ID',anchor=CENTER,command=lambda _col='EMPLOYEE ID': self.treeview_sort_column(self.tree, _col, False))
    self.tree.heading('FIRST NAME',text='FIRST NAME',anchor=CENTER,command=lambda _col='FIRST NAME': self.treeview_sort_column(self.tree, _col, False))
    self.tree.heading('LAST NAME',text='LAST NAME',anchor=CENTER,command=lambda _col='LAST NAME': self.treeview_sort_column(self.tree, _col, False))
    self.tree.heading('SEX',text='SEX',anchor=CENTER,command=lambda _col='SEX': self.treeview_sort_column(self.tree, _col, False))
    self.tree.heading('SCHEDULE IN',text='SCHEDULE IN',anchor=CENTER,command=lambda _col='SCHEDULE IN': self.treeview_sort_column(self.tree, _col, False))
    self.tree.heading('SCHEDULE OUT',text='SCHEDULE OUT',anchor=CENTER,command=lambda _col='SCHEDULE OUT': self.treeview_sort_column(self.tree, _col, False))
    self.tree.heading('WORK STATUS',text='STATUS',anchor=CENTER,command=lambda _col='WORK STATUS': self.treeview_sort_column(self.tree, _col, False))

    
    #select all employees except for the admin
    self.c.execute("SELECT * FROM employees WHERE employee_id  != 'admin'")
    records = self.c.fetchall()     
    self.number_of_emp = len(records)
    #insert data
    count=0
    for record in records:
        self.tree.insert(parent='',index='end',iid=count,text='',
        values=(record[0],record[2],record[3],record[4],record[5],record[6],record[7]))
        count+=1

    
    self.tree.bind('<Double-1>', lambda event, s=self: edit_record(s))
    self.tree.bind('<F2>', lambda event, s=self: edit_record(s))
    self.tree.bind('<Delete>', lambda event, s=self: delete_query(s))
    self.tree.pack()

    edit_btn = Button(show_record_page,image=self.edit_img,bd=0,bg=BGCOLOR,command=lambda: edit_record(self))
    edit_btn.place(x=50,y=525)
    delete_btn=Button(show_record_page,image=self.delete_img,bd=0,bg=BGCOLOR,command=lambda: delete_query(self))
    delete_btn.place(x=160,y=525)
    back_btn=Button(show_record_page, image=self.back_img, bd=0, bg=BGCOLOR, command=lambda: [show_record_page.destroy(), root_page.deiconify()])
    back_btn.place(x=900,y=525)

    # check if user Exit the Window Manually
    show_record_page.protocol("WM_DELETE_WINDOW", lambda: [show_record_page.destroy(), root_page.deiconify()])

    show_record_page.mainloop()