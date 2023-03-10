import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import platform
import datetime as dt


# import arabic_reshaper
# from bidi.algorithm import get_display
# from awesometkinter.bidirender import add_bidi_support

def arng_by_newest_date():
    selected_row_from_tree = myt.item(myt.focus(), 'values')

    myt['columns'] = ('id', 'client', 'product', 'price', 'quantity', 'pricesum', 'tkn_time')
    myt.column('#0', width=0, stretch=False)
    myt.column('id', width=35, anchor='center')
    myt.column('client', width=120, anchor='center')
    myt.column('product', width=230, anchor='center')
    myt.column('price', width=60, anchor='center')
    myt.column('quantity', width=60, anchor='center')
    myt.column('pricesum', width=70, anchor='center')
    myt.column('tkn_time', width=220, anchor='center')

    myt.heading('#0', text='')
    myt.heading('id', text='ID', anchor='center')
    myt.heading('client', text='Client', anchor='center')
    myt.heading('product', text='Product', anchor='center')
    myt.heading('price', text='PPU', anchor='center')
    myt.heading('quantity', text='Qnt', anchor='center')
    myt.heading('pricesum', text='Sum', anchor='center')
    myt.heading('tkn_time', text='Time', anchor='center')

    for item in myt.get_children():
        myt.delete(item)

    c.execute('select rowid,* from recof_tknpro where client = ? order by rowid desc',(selected_row_from_tree[1],))

    for rec_num, rec_rows in enumerate(c.fetchall()):
        rec_mylist = list(rec_rows)
        rec_mylist[-3] = "{:,}".format(rec_mylist[-3])

        # ca2c2c:red----Blue----ffffff:grey
        myt.tag_configure('delay_strip1', foreground='#ca2c2c', background='white')
        myt.tag_configure('delay_strip2', foreground='#ca2c2c', background='#d9d9d9')
        myt.tag_configure('cash_strip1', foreground='blue', background='white')
        myt.tag_configure('cash_strip2', foreground='blue', background='#d9d9d9')

        if delay_cash(rec_mylist[0]) == 0:
            if rec_num % 2 == 0:
                myt.insert(parent='', index=rec_num, text='', values=rec_mylist, tags='delay_strip1')
            else:
                myt.insert(parent='', index=rec_num, text='', values=rec_mylist, tags='delay_strip2')
        if delay_cash(rec_mylist[0]) == 1:
            if rec_num % 2 == 0:
                myt.insert(parent='', index=rec_num, text='', values=rec_mylist, tags='cash_strip1')
            else:
                myt.insert(parent='', index=rec_num, text='', values=rec_mylist, tags='cash_strip2')

    myt.place(x=5, y=5, height=570, width=695)

    add_new_product_but.config(text='دفع أجل', command=change_delay_to_paid)
    clients_and_rec_but.config(text='جدول العملاء', command=clients_list)




def change_delay_to_paid():
    selected_row_from_tree = myt.item(myt.focus(), 'values')
    
    if selected_row_from_tree[-1] == "0":
        
        change_dely_cash(selected_row_from_tree[0])
        
        change_client_credit(1,selected_row_from_tree[1],selected_row_from_tree[5])
        
        conn.commit()
        
        inserting_records_data()
        
    else:
        messagebox.showinfo(message="Error")


def delete_from_recof_tknpro():
    selected_row_from_tree = myt.item(myt.focus(), 'values')

    if selected_row_from_tree[-1] == '0':
        change_client_credit(1, selected_row_from_tree[1], selected_row_from_tree[-3])
    
    c.execute('DELETE FROM recof_tknpro WHERE rowid = ?', (selected_row_from_tree[0],))
    
    conn.commit()
    
    inserting_records_data()


def add_recof_takenpro():
    # فى صفحة تسجيل بند على العميل المسلسل بتاع البند بيضاف لوحده
    # واسم العميل بيكون بتاخد من الصفحة الرئيسية
    # المطلوب هنا ادخال اسم البند وكميته والسعر الاجمالى والبرنامج هيسجل سعر الواحد

    def add_prorecord():
    
        price_per_unit = int(sum_ent.get()) // int(quantity_ent.get())
        add_record_values = (real_name, proname_ent.get(), price_per_unit,
                             quantity_ent.get(),
                             sum_ent.get(), dt.datetime.now().strftime("%d-%m-%Y %H:%M"),radi.get(),)
        c.execute('INSERT INTO recof_tknpro(client,product,price,quantity,sum,tkn_time,dely_cash) '
                  'VALUES (?,?,?,?,?,?,?)', add_record_values)

        if radi.get() == 0:
            change_client_credit(0, real_name, sum_ent.get())
        else:
            pass
        
        conn.commit()
        
        proname_ent.delete(0, 'end')
        quantity_ent.delete(0, 'end')
        sum_ent.delete(0, 'end')
        # success_msg()
        
        records_list()
        
        proname_ent.focus_set()

    new_takenpro_win = tk.Tk()
    new_takenpro_win.title('Register Record')
    new_takenpro_win.geometry('410x180')

    real_name = myt.item(myt.focus(), 'values')[1]

    clientname_lab = tk.Label(new_takenpro_win, text='Client:', font=16)
    clientname_lab.grid(column=0, row=0,pady=5)
    clientname_real = tk.Label(new_takenpro_win, text=real_name, font=('calibri',16,'bold'), fg='green')
    clientname_real.grid(column=1, row=0,pady=5)

    proname_lab = tk.Label(new_takenpro_win, text='Product:', font=16, justify='right')
    proname_lab.grid(column=0, row=1,pady=5)
    proname_ent = tk.Entry(new_takenpro_win,font=15,justify='right')
    proname_ent.grid(column=1, row=1,pady=5)

    quantity_lab = tk.Label(new_takenpro_win, text='Quantity:', font=16)
    quantity_lab.grid(column=0, row=2,pady=5)
    quantity_ent = tk.Entry(new_takenpro_win,font=15,justify='right')
    quantity_ent.grid(column=1, row=2,pady=5)

    sum_lab = tk.Label(new_takenpro_win, text='Value:', font=16)
    sum_lab.grid(column=0, row=3,pady=5)
    sum_ent = tk.Entry(new_takenpro_win,font=15,justify='right')
    sum_ent.grid(column=1, row=3,pady=5)

    radi = tk.IntVar(new_takenpro_win)

    radio_delay = tk.Radiobutton(new_takenpro_win, text='Delay', variable=radi, value=0,font=18)
    radio_delay.grid(column=0, row=4,pady=5,padx=20)

    radio_cash = tk.Radiobutton(new_takenpro_win, text='Cash', variable=radi, value=1,font=18)
    radio_cash.grid(column=1, row=4,pady=5)

    reg_record_but = tk.Button(new_takenpro_win, text='Register', command=add_prorecord, width=9,font=18,height=2)
    reg_record_but.place(x=310, y=20)

    cancel_but = tk.Button(new_takenpro_win, text='Cancel', command=new_takenpro_win.destroy, width=9,font=18,height=2)
    cancel_but.place(x=310, y=90)

    # add_bidi_support(proname_ent)
    proname_ent.focus_set()


def add_new_client():
    def add_record():
        add_record_values = (name_ent.get(), money_ent.get(),)
        c.execute('INSERT INTO clients VALUES (?,?)', add_record_values)
        conn.commit()
        name_ent.delete(0, 'end')
        money_ent.delete(0, 'end')
        # success_msg()
        clients_list()
        name_ent.focus_set()

    new_client_win = tk.Tk()
    new_client_win.title('New client')
    new_client_win.geometry('360x90')

    name_lab = tk.Label(new_client_win, text='Name:', font=16)
    name_lab.grid(column=0, row=1, padx=5, pady=5)
    name_ent = tk.Entry(new_client_win,justify='right')
    name_ent.grid(column=1, row=1, padx=5, pady=5)

    money_lab = tk.Label(new_client_win, text='Money:', font=16)
    money_lab.grid(column=0, row=2, padx=5, pady=5)
    money_ent = tk.Entry(new_client_win,justify='right')
    money_ent.grid(column=1, row=2, padx=5, pady=5)

    reg_record_but = tk.Button(new_client_win, text='Register', command=add_record, width=7)
    reg_record_but.grid(column=3, row=1, padx=5, pady=5)

    cancel_but = tk.Button(new_client_win, text='Cancel', command=new_client_win.destroy, width=7)
    cancel_but.grid(column=3, row=2, padx=5, pady=5)

    name_ent.focus_set()


def change_client_credit(add_remove, client_name, credit_change):
    
    #بيزود القيمة المدخلة على حساب العميل
    if add_remove == 0:
        
        c.execute('SELECT credit FROM clients WHERE name = ?', (client_name,))
        current_credit = c.fetchone()

        new_credit = current_credit[0] + int(credit_change)
        
        c.execute('UPDATE clients SET credit = ? WHERE name = ?', (new_credit, client_name,))

    #بيطرح القيمة المدخلة من حساب العميل
    elif add_remove == 1:
        
        c.execute('SELECT credit FROM clients WHERE name = ?', (client_name,))
        current_credit = c.fetchone()
        
        new_credit = current_credit[0] - int(credit_change.replace(',', ''))
        
        c.execute('UPDATE clients SET credit = ? WHERE name = ?', (new_credit, client_name,))


def clients_list():

    myt['columns'] = ('id', 'name', 'money')
    myt.column('#0', width=0, stretch=False)
    myt.column('id', width=35, anchor='center')
    myt.column('name', width=150, anchor='center')
    myt.column('money', width=100, anchor='center')

    myt.heading('#0', text='')
    myt.heading('id', text='ID', anchor='center')
    myt.heading('name', text='Name', anchor='center')
    myt.heading('money', text='Money', anchor='center')

    inserting_clients_data()

    myt.place(x=5, y=5, height=570, width=550)
    
    add_new_product_but.config(text='تسجيل بيع بند',command=add_recof_takenpro)
    clients_and_rec_but.config(text='جدول المنتجات', command=records_list)
    clients_record_but.config(state='normal')
    add_new_client_but.config(state='normal')
    remove_record_but.config(state='disabled')



def records_list():
    myt['columns'] = ('id', 'client', 'product', 'price', 'quantity', 'pricesum', 'tkn_time')
    myt.column('#0', width=0, stretch=False)
    myt.column('id', width=35, anchor='center')
    myt.column('client', width=120, anchor='center')
    myt.column('product', width=230, anchor='center')
    myt.column('price', width=60, anchor='center')
    myt.column('quantity', width=60, anchor='center')
    myt.column('pricesum', width=70, anchor='center')
    myt.column('tkn_time', width=220, anchor='center')

    myt.heading('#0', text='')
    myt.heading('id', text='ID', anchor='center')
    myt.heading('client', text='Client', anchor='center')
    myt.heading('product', text='Product', anchor='center')
    myt.heading('price', text='PPU', anchor='center')
    myt.heading('quantity', text='Qnt', anchor='center')
    myt.heading('pricesum', text='Sum', anchor='center')
    myt.heading('tkn_time', text='Time', anchor='center')

    inserting_records_data()

    myt.place(x=5, y=5, height=570, width=695)

    add_new_product_but.config(text='دفع أجل',command=change_delay_to_paid)
    clients_and_rec_but.config(text='جدول العملاء',command=clients_list)
    clients_record_but.config(state='disabled')
    add_new_client_but.config(state='disabled')
    remove_record_but.config(state='normal')


# check if the selected record has been bought in cash or delay
def delay_cash(record_id):
    c.execute('SELECT dely_cash FROM recof_tknpro WHERE rowid = ?', (record_id,))
    return c.fetchone()[0]


#تغيير الصف(السجل) من اجل الى مدفوع
#عن طريق تغيير قيمة اخر عمود من 0 الى 1
def change_dely_cash(record_id):
    c.execute('UPDATE recof_tknpro SET dely_cash = ? WHERE rowid = ?', (1,record_id,))

def inserting_records_data():
    for item in myt.get_children():
        myt.delete(item)

    c.execute('select rowid,* from recof_tknpro order by rowid desc')

    for rec_num, rec_rows in enumerate(c.fetchall()):
        rec_mylist = list(rec_rows)
        rec_mylist[-3] = "{:,}".format(rec_mylist[-3])

        # ca2c2c:red----Blue----ffffff:grey
        myt.tag_configure('delay_strip1', foreground='#ca2c2c', background='white')
        myt.tag_configure('delay_strip2', foreground='#ca2c2c', background='#d9d9d9')
        myt.tag_configure('cash_strip1', foreground='blue', background='white')
        myt.tag_configure('cash_strip2', foreground='blue', background='#d9d9d9')

        if delay_cash(rec_mylist[0]) == 0:
            if rec_num % 2 == 0:
                myt.insert(parent='', index=rec_num, text='', values=rec_mylist, tags='delay_strip1')
            else:
                myt.insert(parent='', index=rec_num, text='', values=rec_mylist, tags='delay_strip2')
        if delay_cash(rec_mylist[0]) == 1:
            if rec_num % 2 == 0:
                myt.insert(parent='', index=rec_num, text='', values=rec_mylist, tags='cash_strip1')
            else:
                myt.insert(parent='', index=rec_num, text='', values=rec_mylist, tags='cash_strip2')


def inserting_clients_data():
    for item in myt.get_children():
        myt.delete(item)

    c.execute('select rowid,* from clients')

    for cli_num, cli_rows in enumerate(c.fetchall()):
        cli_mylist = list(cli_rows)
        cli_mylist[-1] = "{:,}".format(cli_mylist[-1])
        myt.insert(parent='', index=cli_num, text='', values=cli_mylist)


def success_msg():
    # get_arabic_display = arabic_reshaper.reshape('تمت العملية بنجاح')
    # messagebox.showinfo(title='good', message=get_display(get_arabic_display))
    messagebox.showinfo(title='good', message='تمت العملية بنجاح')


# sqlite3 activator
if platform.system() == 'Windows':
    conn = sqlite3.connect("F:/courses-videos/python-projects/egko-clients-project/clients-database.db")
else:
    conn = sqlite3.connect("/home/ahmed/PycharmProjects/egko-clients-project/clients-database.db")

c = conn.cursor()
c.execute('select rowid,* from clients')

root = tk.Tk()
root.title('Main')
root.geometry('1100x580')

# myst = ttk.Style()
# myst.theme_use('clam')

myt = ttk.Treeview(root)

clients_and_rec_but = tk.Button(root, text='جدول المنتجات', command=clients_list,font=25,width=20,height=7)
clients_and_rec_but.place(x=755, y=70)

#records_but = tk.Button(root, text='Products list', command=records_list,font=25,width=20,height=7)
#records_but.place(x=710, y=70)

add_new_product_but = tk.Button(root, text='تسجيل بيع بند', command=add_recof_takenpro)
add_new_product_but.place(x=750, y=350)

clients_record_but = tk.Button(root, text='سجلات العميل', command=arng_by_newest_date)
clients_record_but.place(x=750, y=400)

add_new_client_but = tk.Button(root, text='إضافة عميل جديد', command=add_new_client)
add_new_client_but.place(x=750, y=450)

remove_record_but = tk.Button(root, text='Remove registered record', command=delete_from_recof_tknpro, fg='red')
remove_record_but.place(x=750, y=550)

clients_list()

root.mainloop()
