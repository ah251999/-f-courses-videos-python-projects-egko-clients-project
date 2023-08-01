import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import datetime as dt

# import arabic_reshaper
# from bidi.algorithm import get_display
# from awesometkinter.bidirender import add_bidi_support


def pay_button_window():

    def pay_function():
        selected_row_from_tree = myt.item(myt.focus(), 'values')
        change_client_credit(1,selected_row_from_tree[1],pay_entry.get())
        conn.commit()
        inserting_clients_data()

    pay_window = tk.Tk()
    pay_window.title('تخصيم')

    pay_label = tk.Label(pay_window, text=':المبلغ', font=('bold',16))
    pay_label.grid(row=0,column=2,padx=5,pady=5)

    pay_entry = tk.Entry(pay_window,font=('bold',16),width=10)
    pay_entry.grid(row=0,column=1,padx=5,pady=5)

    pay_button= tk.Button(pay_window, text='تخصيم', command=pay_function,font=('bold',16))
    pay_button.grid(row=1,column=1,padx=5,pady=5)

    clear_pay_button= tk.Button(pay_window, text='مسح', command=lambda: pay_entry.delete(0,'end'),font=('bold',16))
    clear_pay_button.grid(row=0,column=0,padx=5,pady=5)

    cancel_pay_button= tk.Button(pay_window, text='إلغاء', command=pay_window.destroy,font=('bold',16))
    cancel_pay_button.grid(row=1,column=0,padx=5,pady=5)


def clear_search():

    frst_wrd_ent.delete(0,'end')

    sec_wrd_ent.delete(0,'end')

    if cli_n:
        inserting_records_data(cli_n,None,None)
    else:
        inserting_records_data(None,None,None)

def arng_client_by_latest_rowid():
    try:
        selected_row_from_tree = myt.item(myt.focus(), 'values')

        global cli_n
        cli_n = selected_row_from_tree[1]

        records_list(cli_n)
    except AttributeError:
        myt_messsage(0)
    except IndexError:
        myt_message(0)


"""def change_delay_to_paid():

    if myt_message(1):

        if len(myt.selection()) == 1:

            selected_row_from_tree = myt.item(myt.focus(), 'values')
        
            if selected_row_from_tree[-1] == "0":
            
                change_dely_cash(selected_row_from_tree[0])
            
                change_client_credit(1,selected_row_from_tree[1],selected_row_from_tree[5])
            
                conn.commit()
            
            else:
                messagebox.showinfo(message="Error")

        else:
            for i in myt.selection():

                selected_row_from_tree = myt.item(i, 'values')

        
                if selected_row_from_tree[-1] == "0":
            
                    change_dely_cash(selected_row_from_tree[0])
            
                    change_client_credit(1,selected_row_from_tree[1],selected_row_from_tree[5])
            
                    conn.commit()
                
                else:
                    messagebox.showinfo(message="Error")

        inserting_records_data(None,None,None)

    else:
        pass"""


def delete_from_recof_tknpro():

    if myt_message(2):

        if len(myt.selection()) == 1:

            selected_row_from_tree = myt.item(myt.focus(), 'values')

            change_client_credit(1, selected_row_from_tree[1], selected_row_from_tree[-2])
            
            c.execute('DELETE FROM recof_tknpro WHERE rowid = ?', (selected_row_from_tree[0],))
            
            conn.commit()
            
        else:

            for i in myt.selection():

                selected_row_from_tree = myt.item(i, 'values')

                change_client_credit(1, selected_row_from_tree[1], selected_row_from_tree[-2])
                
                c.execute('DELETE FROM recof_tknpro WHERE rowid = ?', (selected_row_from_tree[0],))
                
                conn.commit()
            
        inserting_records_data(None,None,None)
        
    else:
        pass


def add_recof_takenpro():
    try:
        # فى صفحة تسجيل بند على العميل المسلسل بتاع البند بيضاف لوحده
        # واسم العميل بيكون بتاخد من الصفحة الرئيسية
        # المطلوب هنا ادخال اسم البند وكميته والسعر الاجمالى والبرنامج هيسجل سعر الواحد

        def add_prorecord():
            price_per_unit = float(sum_ent.get()) // float(quantity_ent.get())
            """add_record_values = (real_name, proname_ent.get(), price_per_unit,
                             quantity_ent.get(),
                             sum_ent.get(), dt.datetime.now().strftime("%d-%m-%Y %H:%M"),radi.get(),)
            c.execute('INSERT INTO recof_tknpro(client,product,price,quantity,sum,tkn_time,dely_cash) '
                  'VALUES (?,?,?,?,?,?,?)', add_record_values)"""

            add_record_values = (real_name, proname_ent.get(), price_per_unit,
                             quantity_ent.get(),
                             sum_ent.get(), dt.datetime.now().strftime("%d-%m-%Y %H:%M"),)
            c.execute('INSERT INTO recof_tknpro(client,product,price,quantity,sum,tkn_time) '
                  'VALUES (?,?,?,?,?,?)', add_record_values)
                  
                  
            change_client_credit(0, real_name, sum_ent.get())
            
            conn.commit()
        
            proname_ent.delete(0, 'end')
            quantity_ent.delete(0, 'end')
            sum_ent.delete(0, 'end')
        
            records_list(None)
        
            proname_ent.focus_set()
        
        real_name = myt.item(myt.focus(), 'values')[1]
        
        new_takenpro_win = tk.Tk()
        new_takenpro_win.title('تسجيل بيع بند')
        
        clientname_lab = tk.Label(new_takenpro_win, text=':العميل', font=16)
        clientname_lab.grid(row=0,column=2,pady=5)
        clientname_real = tk.Label(new_takenpro_win, text=real_name, font=('bold',20), fg='green',justify='right')
        clientname_real.grid(row=0,column=1,pady=5)

        proname_lab = tk.Label(new_takenpro_win, text=':المنتج', font=16, justify='right')
        proname_lab.grid(row=1,column=2,pady=5)
        proname_ent = tk.Entry(new_takenpro_win,font=15,width=25,justify='right')
        proname_ent.grid(row=1,column=1,pady=5)

        quantity_lab = tk.Label(new_takenpro_win, text=':الكمية', font=16)
        quantity_lab.grid(row=2,column=2,pady=5)
        quantity_ent = tk.Entry(new_takenpro_win,font=15,justify='right',width=5)
        quantity_ent.grid(row=2,column=1,pady=5)

        sum_lab = tk.Label(new_takenpro_win, text=':الاجمالى', font=16)
        sum_lab.grid(row=3,column=2,pady=5)
        sum_ent = tk.Entry(new_takenpro_win,font=15,justify='right',width=5)
        sum_ent.grid(row=3,column=1,pady=5)

        """radi = tk.IntVar(new_takenpro_win)

        radio_delay = tk.Radiobutton(new_takenpro_win, text='آجل', variable=radi, value=0,font=18)
        radio_delay.grid(row=4,column=2,pady=5)

        radio_cash = tk.Radiobutton(new_takenpro_win, text='نقدا', variable=radi, value=1,font=18)
        radio_cash.grid(row=4,column=1,pady=5)"""
        
        reg_record_but = tk.Button(new_takenpro_win, text='تسجيل', command=add_prorecord,width=5,font=('Bold',16),height=2)
        reg_record_but.grid(row=5,column=2,pady=5,padx=12)

        cancel_but = tk.Button(new_takenpro_win, text='إلغاء', command=new_takenpro_win.destroy,width=5,font=('Bold',16),height=2)
        cancel_but.grid(row=5,column=1,pady=5)

        # add_bidi_support(proname_ent)
        proname_ent.focus_set()
    except AttributeError:
        myt_message(0)
    except IndexError:
        myt_message(0)



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
    new_client_win.title('تسجيل عميل جديد')

    name_lab = tk.Label(new_client_win, text=':الاسم', font=('Bold',16))
    name_lab.grid(column=2, row=1, padx=5, pady=5)
    name_ent = tk.Entry(new_client_win,justify='right',font=('Bold',16))
    name_ent.grid(column=1, row=1, padx=5, pady=5)

    money_lab = tk.Label(new_client_win, text=':الآجل', font=('Bold',16))
    money_lab.grid(column=2, row=2, padx=5, pady=5)
    money_ent = tk.Entry(new_client_win,justify='right',font=('Bold',16))
    money_ent.grid(column=1, row=2, padx=5, pady=5)

    reg_record_but = tk.Button(new_client_win, text='تسجيل', command=add_record, font=('Bold',16))
    reg_record_but.grid(column=0, row=1, padx=5, pady=5)

    cancel_but = tk.Button(new_client_win, text='إلغاء', command=new_client_win.destroy, font=('Bold',16))
    cancel_but.grid(column=0, row=2, padx=5, pady=5)

    name_ent.focus_set()


def change_client_credit(add_remove, client_name, credit_change):
    
    #بيزود القيمة المدخلة على حساب العميل
    if add_remove == 0:
        
        c.execute('SELECT credit FROM clients WHERE name = ?', (client_name,))
        current_credit = c.fetchone()

        new_credit = current_credit[0] + float(credit_change)
        
        c.execute('UPDATE clients SET credit = ? WHERE name = ?', (new_credit, client_name,))

    #بيطرح القيمة المدخلة من حساب العميل
    elif add_remove == 1:
        
        c.execute('SELECT credit FROM clients WHERE name = ?', (client_name,))
        current_credit = c.fetchone()
        
        new_credit = current_credit[0] - float(credit_change.replace(',', ''))
        
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

    #myt.place(x=5, y=5, height=570, width=550)
    myt_frame.place(x=5, y=5, height=570, width=550)

    myst.configure('Treeview',rowheight=50)

    show_current_table_lab.config(text='العملاء')
    add_new_product_but.config(text='تسجيل بيع بند',command=add_recof_takenpro,state='normal')
    clients_and_rec_but.config(text='جدول البنود', command=lambda: records_list(None))
    clients_record_but.config(state='normal')
    add_new_client_but.config(state='normal')
    remove_record_but.config(text='تخصيم', command=pay_button_window, fg='black')
    search_frame.place_forget()
    main_notebook.place(x=700,y=200)
    global cli_n
    cli_n = None


def records_list(vari_for_insert):
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

    inserting_records_data(vari_for_insert,None,None)

    #myt.place(x=5, y=5, height=570, width=695)
    myt_frame.place(x=5, y=5, height=570, width=695)

    myst.configure('Treeview',rowheight=30)

    show_current_table_lab.config(text='البنود')
    add_new_product_but.config(state='disabled')
    clients_and_rec_but.config(text='جدول العملاء',command=clients_list)
    clients_record_but.config(state='disabled')
    add_new_client_but.config(state='disabled')
    remove_record_but.config(text='إزالة(مرتجع) بند',
            command=delete_from_recof_tknpro, fg='red',font=('bold',15))
    search_frame.place(x=750,y=400)
    main_notebook.place_forget()


# check if the selected record has been bought in cash or delay
"""def delay_cash(record_id):
    c.execute('SELECT dely_cash FROM recof_tknpro WHERE rowid = ?', (record_id,))
    return c.fetchone()[0]"""


#تغيير الصف(السجل) من اجل الى مدفوع
#عن طريق تغيير قيمة اخر عمود من 0 الى 1
"""def change_dely_cash(record_id):
    c.execute('UPDATE recof_tknpro SET dely_cash = ? WHERE rowid = ?', (1,record_id,))"""

def inserting_records_data(client_name,frst_wrd,sec_wrd):
    for item in myt.get_children():
        myt.delete(item)


    if client_name and frst_wrd:
        c.execute("select rowid, * from recof_tknpro where client = ?"
                  " and product like ? and product like ?",(client_name,'%' + frst_wrd + '%','%' + sec_wrd + '%',))
    elif not client_name and frst_wrd:
        c.execute("select rowid, * from recof_tknpro where product like ? and product like ?",
                  ('%' + frst_wrd + '%','%' + sec_wrd + '%',))
    elif client_name and not frst_wrd:
        c.execute('select rowid,* from recof_tknpro where client = ? order by rowid desc', (client_name,))
    else:
        c.execute('select rowid,* from recof_tknpro order by rowid desc')

    for rec_num, rec_rows in enumerate(c.fetchall()):
        rec_mylist = list(rec_rows)
        rec_mylist[-2] = "{:,}".format(rec_mylist[-2])

        # ca2c2c:red----Blue----ffffff:grey
        """myt.tag_configure('delay_strip1', foreground='#ca2c2c', background='white')
        myt.tag_configure('delay_strip2', foreground='#ca2c2c', background='#d9d9d9')"""
        myt.tag_configure('cash_strip1', foreground='blue', background='white')
        myt.tag_configure('cash_strip2', foreground='blue', background='#d9d9d9')

        """if delay_cash(rec_mylist[0]) == 0:
            if rec_num % 2 == 0:
                myt.insert(parent='', index=rec_num, text='', values=rec_mylist, tags='delay_strip1')
            else:
                myt.insert(parent='', index=rec_num, text='', values=rec_mylist, tags='delay_strip2')
        if delay_cash(rec_mylist[0]) == 1:
            if rec_num % 2 == 0:
                myt.insert(parent='', index=rec_num, text='', values=rec_mylist, tags='cash_strip1')
            else:
                myt.insert(parent='', index=rec_num, text='', values=rec_mylist, tags='cash_strip2')"""
        
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


def myt_message(condi):
    # get_arabic_display = arabic_reshaper.reshape('تمت العملية بنجاح')
    # messagebox.showinfo(title='good', message=get_display(get_arabic_display))
    if condi == 0:
        tk.messagebox.showwarning(title='!انتبه', message='.الرجاء اختيار عميل من الجدول')
    elif condi == 1:
        tk.messagebox.askyesno(title='!انتبه', message='تأكيد على دفع الآجل؟')
        return True
    elif condi == 2:
        tk.messagebox.askyesno(title='!انتبه', message='هل انت متأكد من حذف البند/البنود؟')
        return True




# sqlite3 activator
conn = sqlite3.connect("clients-database.db")

c = conn.cursor()
c.execute('select rowid,* from clients')

cli_n = None

root = tk.Tk()
root.title('Main')
root.geometry('1100x580')

#إطار الجدول
#=======================================================================
myst = ttk.Style()

# تعديل حجم باب notebook(tabs)
#=======================================================================
current = myst.theme_use()

myst.theme_settings(current, {"TNotebook.Tab": {"configure": {"padding": [15, 15]}}})
#=======================================================================

myt_frame = tk.Frame(root)

myt_scrollbar = ttk.Scrollbar(myt_frame,orient=tk.VERTICAL)
myt_scrollbar.pack(side='right',fill='both')

myt = ttk.Treeview(myt_frame,yscrollcommand=myt_scrollbar.set)
myt.pack(side='left',fill='both',expand=1)

myt_scrollbar.configure(command=myt.yview)
#=======================================================================

#إطار الزراير الرئيسية
#=======================================================================
clients_and_rec_but = tk.Button(root, text='جدول البنود',font=('Bold',25))
clients_and_rec_but.place(x=890,y=12)

clients_record_but = tk.Button(root, text='سجل العميل', command=arng_client_by_latest_rowid,font=('bold',20))
clients_record_but.place(x=720,y=23)
 
show_current_table_lab = tk.Label(root, text='العملاء', font=('Bold',45),fg='green',justify='right')
show_current_table_lab.place(x=840, y=110)

#records_but = tk.Button(root, text='Products list', command=records_list,font=25,width=20,height=7)
#records_but.place(x=710, y=70)
#=======================================================================

#إطار البحث
#=======================================================================
search_frame = tk.LabelFrame(root,text='بحث بكلمتين',labelanchor='ne',font=('Bold',15))

frst_wrd_lab = tk.Label(search_frame,text=':الكلمة الأولى',justify='right',font=('Bold',15))
frst_wrd_lab.grid(row=0,column=2,pady=3)

sec_wrd_lab = tk.Label(search_frame,text=':الكلمة الثانية',justify='right',font=('Bold',15))
sec_wrd_lab.grid(row=1,column=2,pady=3)

frst_wrd_ent = tk.Entry(search_frame,justify='right',font=('Bold',15),width=12)
frst_wrd_ent.grid(row=0,column=1,pady=3)

sec_wrd_ent = tk.Entry(search_frame,justify='right',font=('Bold',15),width=12)
sec_wrd_ent.grid(row=1,column=1,pady=3)

search_but = tk.Button(search_frame,text='بحث',font='Bold',width=3,command=lambda: inserting_records_data(cli_n,frst_wrd_ent.get()
                                                                                      ,sec_wrd_ent.get()))
search_but.grid(row=0,column=0,pady=3,padx=3)

clear_but = tk.Button(search_frame,text='مسح المدخلات',font='Bold',command=clear_search)
clear_but.grid(row=1,column=0,pady=3,padx=3)
#=======================================================================

#إطار الزراير الاساسية
#(تحت العنوان)
#=======================================================================
but_frame = tk.Frame(root)
but_frame.place(x=840,y=200)

add_new_product_but = tk.Button(but_frame, text='تسجيل بيع بند', command=add_recof_takenpro,font=('bold',15))
add_new_product_but.grid(row=1,column=0,pady=6)

#anc_ri_but is shortname for add new client and remove item button
add_new_client_but = tk.Button(but_frame, text='إضافة عميل جديد', command=add_new_client,font=('bold',15))
add_new_client_but.grid(row=2,column=0,pady=6)

remove_record_but = tk.Button(but_frame, text='تخصيم', command=pay_button_window,font=('bold',15))
remove_record_but.grid(row=3,column=0,pady=6)
#=======================================================================


# قائمة الابواب
#=======================================================================
    
main_notebook = ttk.Notebook(root)

anp_frame = tk.Frame(main_notebook,height=300,width=380)
anp_frame.pack(fill='both',expand=True)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#try:
# فى صفحة تسجيل بند على العميل المسلسل بتاع البند بيضاف لوحده
# واسم العميل بيكون بتاخد من الصفحة الرئيسية
# المطلوب هنا ادخال اسم البند وكميته والسعر الاجمالى والبرنامج هيسجل سعر الواحد

def add_prorecord():
    
    real_name = myt.item(myt.focus(), 'values')[1]

    price_per_unit = float(sum_ent.get()) // float(quantity_ent.get())

    add_record_values = (real_name, proname_ent.get(), price_per_unit,
                     quantity_ent.get(),
                     sum_ent.get(), dt.datetime.now().strftime("%d-%m-%Y %H:%M"),)
    c.execute('INSERT INTO recof_tknpro(client,product,price,quantity,sum,tkn_time) '
          'VALUES (?,?,?,?,?,?)', add_record_values)
          
          
    change_client_credit(0, real_name, sum_ent.get())
    
    conn.commit()

    proname_ent.delete(0, 'end')
    quantity_ent.delete(0, 'end')
    sum_ent.delete(0, 'end')

    records_list(None)

    proname_ent.focus_set()
    
clientname_lab = tk.Label(anp_frame, text=':العميل', font=16)
clientname_lab.grid(row=0,column=2,pady=5)
clientname_real = tk.Label(anp_frame, text='اسم العميل', font=('bold',20), fg='green',justify='right')
clientname_real.grid(row=0,column=1,pady=5)

def testy(event):
    clientname_real.config(text=myt.item(myt.focus(), 'values')[1])

myt.bind('<<TreeviewSelect>>', testy)


def lolo(event):
    clientname_real.config(text='اسم العميل')
    for i in myt.selection():
        myt.selection_remove(i)
        
clients_and_rec_but.bind('<Button-1>',lolo)
clients_record_but.bind('<Button-1>',lolo)

proname_lab = tk.Label(anp_frame, text=':المنتج', font=16, justify='right')
proname_lab.grid(row=1,column=2,pady=5)
proname_ent = tk.Entry(anp_frame,font=15,width=25,justify='right')
proname_ent.grid(row=1,column=1,pady=5)

quantity_lab = tk.Label(anp_frame, text=':الكمية', font=16)
quantity_lab.grid(row=2,column=2,pady=5)
quantity_ent = tk.Entry(anp_frame,font=15,justify='right',width=5)
quantity_ent.grid(row=2,column=1,pady=5)

sum_lab = tk.Label(anp_frame, text=':الاجمالى', font=16)
sum_lab.grid(row=3,column=2,pady=5)
sum_ent = tk.Entry(anp_frame,font=15,justify='right',width=5)
sum_ent.grid(row=3,column=1,pady=5)

reg_record_but = tk.Button(anp_frame, text='تسجيل', command=add_prorecord,width=5,font=('Bold',16),height=2)
reg_record_but.grid(row=5,column=2,pady=5,padx=12)

# add_bidi_support(proname_ent)
proname_ent.focus_set()
"""except AttributeError:
    myt_message(0)
except IndexError:
    myt_message(0)"""
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


pay_dely_frame = tk.Frame(main_notebook,height=300,width=380)
pay_dely_frame.pack(fill='both',expand=True)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def pay_function():
    selected_row_from_tree = myt.item(myt.focus(), 'values')
    change_client_credit(1,selected_row_from_tree[1],pay_entry.get())
    conn.commit()
    inserting_clients_data()

pay_label = tk.Label(pay_dely_frame, text=':المبلغ', font=('bold',16))
pay_label.grid(row=0,column=2,padx=5,pady=5)

pay_entry = tk.Entry(pay_dely_frame,font=('bold',16),width=10)
pay_entry.grid(row=0,column=1,padx=5,pady=5)

pay_button= tk.Button(pay_dely_frame, text='تخصيم', command=pay_function,font=('bold',16))
pay_button.grid(row=1,column=1,padx=5,pady=5)

clear_pay_button= tk.Button(pay_dely_frame, text='مسح', command=lambda: pay_entry.delete(0,'end'),font=('bold',16))
clear_pay_button.grid(row=0,column=0,padx=5,pady=5)
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

add_new_client_frame = tk.Frame(main_notebook,height=100,width=100)
add_new_client_frame.pack(fill='both',expand=True)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def add_record():
    add_record_values = (name_ent.get(), money_ent.get(),)
    c.execute('INSERT INTO clients VALUES (?,?)', add_record_values)
    conn.commit()
    name_ent.delete(0, 'end')
    money_ent.delete(0, 'end')
    # success_msg()
    clients_list()
    name_ent.focus_set()

name_lab = tk.Label(add_new_client_frame, text=':الاسم', font=('Bold',16))
name_lab.grid(column=2, row=1, padx=5, pady=5)
name_ent = tk.Entry(add_new_client_frame,justify='right',font=('Bold',16))
name_ent.grid(column=1, row=1, padx=5, pady=5)

money_lab = tk.Label(add_new_client_frame, text=':الآجل', font=('Bold',16))
money_lab.grid(column=2, row=2, padx=5, pady=5)
money_ent = tk.Entry(add_new_client_frame,justify='right',font=('Bold',16))
money_ent.grid(column=1, row=2, padx=5, pady=5)

reg_record_but = tk.Button(add_new_client_frame, text='تسجيل', command=add_record, font=('Bold',16))
reg_record_but.grid(column=0, row=1, padx=5, pady=5)

name_ent.focus_set()
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

main_notebook.add(anp_frame, text='تسجيل بيع بند')
main_notebook.add(pay_dely_frame, text='تخصيم')
main_notebook.add(add_new_client_frame, text='إضافة عميل جديد')

#=======================================================================


clients_list()

root.mainloop()
