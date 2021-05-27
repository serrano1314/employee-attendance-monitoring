'TESTING AREA'
# make your tests here

# import re

# def format_time_to_list(time_str):
# 	time_list = [int(i) for i in re.findall('[0-9][0-9]', time_str)]
# 	if 'PM' in time_str and time_list[0]<12:
# 		time_list[0]+=12

# 	if 'AM' in time_str and time_list[0]==12:
# 		time_list[0]-=12

# 	return time_list


# time2='12:00 AM'


# print(format_time_to_list(time2))

'old show records'

    # def show_records(self, root_page):
    #     cell_size = 22
    #     th_font ='Arial 12 bold'
    #     win_size='1100x600'
    #     table_bg_color = '#ffffff'
    #     show_record_page = Toplevel()
    #     show_record_page.title('SHOW RECORDS')
    #     show_record_page.geometry(win_size)
    #     show_record_page.config(bg=BGCOLOR)
        
    #     #select all employees except for the admin
    #     self.c.execute("SELECT * FROM employees WHERE employee_id  != 'admin'")
    #     records = self.c.fetchall()

    #     Label(show_record_page,bg=HEADER_COLOR,padx=500,pady=25,text="SHOW RECORDS").grid(row=4,column=5,columnspan=8)
    #     table_row=5
        
    #     Label(show_record_page,bg=BGCOLOR,text="EMPLOYEE ID",font=th_font,pady=10).grid(row=table_row,column=5)
    #     Label(show_record_page,bg=BGCOLOR,text="FIRST NAME ",font=th_font,pady=10).grid(row=table_row,column=6)
    #     Label(show_record_page,bg=BGCOLOR,text="LAST NAME ",font=th_font,pady=10).grid(row=table_row,column=7)
    #     Label(show_record_page,bg=BGCOLOR,text="SEX",font=th_font,pady=10).grid(row=table_row,column=8)
    #     Label(show_record_page,bg=BGCOLOR,text="SCHEDULE IN",font=th_font,pady=10).grid(row=table_row,column=9)
    #     Label(show_record_page,bg=BGCOLOR,text="SCHEDULE OUT",font=th_font,pady=10).grid(row=table_row,column=10)
        
    #     for record in records:
    #         stud_id=Label(show_record_page,text=record[0],width=cell_size,bg=table_bg_color,padx=0)
    #         stud_id.grid(row=table_row+1,column=5)

    #         first_name=Label(show_record_page,text=record[2],width=cell_size,bg=table_bg_color)
    #         first_name.grid(row=table_row+1,column=6)

    #         middle_name=Label(show_record_page,text=record[3],width=cell_size,bg=table_bg_color)
    #         middle_name.grid(row=table_row+1,column=7)

    #         last_name=Label(show_record_page,text=record[4],width=cell_size,bg=table_bg_color)
    #         last_name.grid(row=table_row+1,column=8)

    #         course=Label(show_record_page,text=record[5],width=cell_size,bg=table_bg_color)
    #         course.grid(row=table_row+1,column=9)

    #         section=Label(show_record_page,text=record[6],width=cell_size,bg=table_bg_color)
    #         section.grid(row=table_row+1,column=10)

    #         Button(show_record_page,text="EDIT",command=lambda edit_id=record[0]: self.edit_record(show_record_page,edit_id),bg='#AAFE92').grid(row=table_row+1,column=11)
    #         Button(show_record_page,text="DELETE",command=lambda del_id=record[0]: self.delete_query(show_record_page,del_id, root_page),bg='#FE9292').grid(row=table_row+1,column=12)

    #         table_row+=1

    #     self.connection.commit()

    #     Button(show_record_page, text='Go Back', width=10, command=lambda: [show_record_page.destroy(), root_page.deiconify()]).grid(row=table_row+1, column=5, pady=20)

    #     # check if user Exit the Window Manually
    #     show_record_page.protocol("WM_DELETE_WINDOW", lambda: [show_record_page.destroy(), root_page.deiconify()])

    #     show_record_page.mainloop()

    'old delete query'
    # def delete_query(self,page,record_id, root):
    # response = messagebox.askyesno('DELETE RECORD',f'ARE YOU SURE TO DELETE RECORD FOR {record_id} ?')
    # if(response):
    #     self.c.execute(f"DELETE FROM employees WHERE employee_id = '{record_id}'")
    #     self.connection.commit()         
    #     page.destroy()
    #     self.show_records(root)