from tkinter import *
from tkinter import messagebox, ttk
from config_var import *

def update_query(self,edit_page,update_id):
    response = messagebox.askyesno('UPDATE RECORD',f'ARE YOU SURE TO UPDATE RECORD FOR {update_id} ?')
    if(response):
        self.c.execute('''UPDATE employees SET
            employee_id = :employee_id,
            password = :password,
            first_name = :first_name,
            last_name = :last_name,
            sex = :sex,
            schedule_in = :schedule_in,
            schedule_out = :schedule_out

                WHERE employee_id = :update_id''',
            {
                'employee_id': employee_id_edit.get(),
                'password': password_edit.get(),
                'first_name': first_name_edit.get(),
                'last_name': last_name_edit.get(),
                'sex': sex_edit.get(),
                'schedule_in': schedule_in_edit.get(),
                'schedule_out': schedule_out_edit.get(),

                'update_id': update_id
            })
        self.c.execute("UPDATE employee_attendance SET employee_id = ? WHERE employee_id = ?", (employee_id_edit.get(), update_id))

        selected = self.tree.focus()
        self.tree.item(selected,text='',values=(employee_id_edit.get(),first_name_edit.get(),
                                                last_name_edit.get(),sex_edit.get(),
                                                schedule_in_edit.get(),schedule_out_edit.get()))

        self.connection.commit()
        print('success')
        edit_page.destroy()

def edit_record(self,page):
    try:
        record_tree = self.tree.selection()[0]
    except:
        messagebox.showinfo('Invalid', 'Please Select a Row in the Table First')
        return
    
    record = self.tree.item(record_tree)
    id = record['values'][0]
    cell_size = 35
    table_col=3
    win_size='400x300'
    
    global employee_id_edit,password_edit,first_name_edit,last_name_edit,sex_edit,schedule_in_edit,schedule_out_edit

    edit_record_page = Tk()
    edit_record_page.title('EDIT EMPLOYEE RECORD')
    edit_record_page.geometry(win_size)
    edit_record_page.config(bg=BGCOLOR)

    Label(edit_record_page,text="EMPLOYEE ID:",bg=BGCOLOR).grid(row=2,column=table_col-1,padx=10,pady=(40,0 ))
    employee_id_edit=Entry(edit_record_page, width=cell_size)
    employee_id_edit.grid(row=2, column=table_col, pady=(40, 0))

    Label(edit_record_page,text="PASSWORD:",bg=BGCOLOR).grid(row=3,column=table_col-1)
    password_edit=Entry(edit_record_page, width=cell_size)
    password_edit.grid(row=3, column=table_col)
    
    Label(edit_record_page,text="FIRST NAME:",bg=BGCOLOR).grid(row=4,column=table_col-1)
    first_name_edit=Entry(edit_record_page, width=cell_size)
    first_name_edit.grid(row=4, column=table_col)

    Label(edit_record_page,text="LAST NAME:",bg=BGCOLOR).grid(row=5,column=table_col-1)
    last_name_edit=Entry(edit_record_page,width=cell_size)
    last_name_edit.grid(row=5,column=table_col)

    Label(edit_record_page,text="SEX:",bg=BGCOLOR).grid(row=6,column=table_col-1)
    sex_edit=Entry(edit_record_page, width=cell_size)
    sex_edit.grid(row=6, column=table_col)

    Label(edit_record_page,text="SCHEDULE IN:",bg=BGCOLOR).grid(row=7,column=table_col-1)
    schedule_in_edit=Entry(edit_record_page, width=cell_size)
    schedule_in_edit.grid(row=7, column=table_col)

    Label(edit_record_page, text="SCHEDULE OUT:",bg=BGCOLOR).grid(row=8, column=table_col - 1)
    schedule_out_edit = Entry(edit_record_page, width=cell_size)
    schedule_out_edit.grid(row=8, column=table_col)



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

    
    Button(edit_record_page,text="SAVE",width=15,command=lambda:update_query(self,edit_record_page,id),bg='#AAFE92').grid(row=9,column=table_col,pady=20)
    Button(edit_record_page,text="CANCEL",width=15,command=lambda:edit_record_page.destroy(),bg='#e4bad4').grid(row=9,column=table_col-1,pady=20,padx=(35,0))
    edit_record_page.mainloop()

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
        print()
        self.tree.delete(record_tree)
        self.c.execute(f"DELETE FROM employees WHERE employee_id = '{id}'")
        self.connection.commit()
        self.c.execute(f"DELETE FROM employee_attendance WHERE employee_id = '{id}'")
        self.connection.commit()

def show_records(self, root_page):
    cell_size = 165
    mid_cell_size = 25
    win_size='1100x620'
    th_font ='Arial 12 bold'
    show_record_page = Toplevel()
    show_record_page.title('SHOW RECORDS')
    show_record_page.geometry(win_size)
    show_record_page.config(bg=BGCOLOR)
    show_record_frame=Frame(show_record_page,bg=BGCOLOR)
    show_record_frame.pack()
    Label(show_record_frame, height=3, width=600, bg=HEADER_COLOR, text='EMPLOYEE RECORDS', font=FONT).pack(pady=(0, 10))
    #for table's scrollbar
    scrollbary = Scrollbar(show_record_frame, orient=VERTICAL)

    self.tree = ttk.Treeview(show_record_frame,selectmode=BROWSE,yscrollcommand=scrollbary.set,height=20)
    scrollbary.config(command=self.tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    self.tree['columns'] = ('EMPLOYEE ID', 'FIRST NAME', 'LAST NAME', 'SEX', 'SCHEDULE IN','SCHEDULE OUT')
    self.tree.column('#0',width=0,stretch=NO)
    self.tree.column('EMPLOYEE ID',width=cell_size,minwidth=mid_cell_size,anchor=CENTER)
    self.tree.column('FIRST NAME',width=cell_size,minwidth=mid_cell_size,anchor=W)
    self.tree.column('LAST NAME',width=cell_size,minwidth=mid_cell_size,anchor=W)
    self.tree.column('SEX',width=cell_size,minwidth=mid_cell_size,anchor=CENTER)
    self.tree.column('SCHEDULE IN',width=cell_size,minwidth=mid_cell_size,anchor=CENTER)
    self.tree.column('SCHEDULE OUT',width=cell_size,minwidth=mid_cell_size,anchor=CENTER)

    self.tree.heading('#0',text='')
    self.tree.heading('EMPLOYEE ID',text='EMPLOYEE ID',anchor=CENTER)
    self.tree.heading('FIRST NAME',text='FIRST NAME',anchor=CENTER)
    self.tree.heading('LAST NAME',text='LAST NAME',anchor=CENTER)
    self.tree.heading('SEX',text='SEX',anchor=CENTER)
    self.tree.heading('SCHEDULE IN',text='SCHEDULE IN',anchor=CENTER)
    self.tree.heading('SCHEDULE OUT',text='SCHEDULE OUT',anchor=CENTER)

    
    #select all employees except for the admin
    self.c.execute("SELECT * FROM employees WHERE employee_id  != 'admin'")
    records = self.c.fetchall()        
    #insert data
    count=0
    for record in records:
        self.tree.insert(parent='',index='end',iid=count,text='',
        values=(record[0],record[2],record[3],record[4],record[5],record[6]))
        count+=1

    self.tree.pack()

    edit_btn = Button(show_record_page,image=self.edit_img,bd=0,bg=BGCOLOR,command=lambda: edit_record(self,show_record_page))
    edit_btn.place(x=50,y=525)
    delete_btn=Button(show_record_page,image=self.delete_img,bd=0,bg=BGCOLOR,command=lambda: delete_query(self))
    delete_btn.place(x=160,y=525)
    back_btn=Button(show_record_page, image=self.back_img, bd=0, bg=BGCOLOR, command=lambda: [show_record_page.destroy(), root_page.deiconify()])
    back_btn.place(x=990,y=525)

    # check if user Exit the Window Manually
    show_record_page.protocol("WM_DELETE_WINDOW", lambda: [show_record_page.destroy(), root_page.deiconify()])

    show_record_page.mainloop()