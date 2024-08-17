import sqlite3
import sys
from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk, messagebox
import time
import os
import tempfile

from fpdf import FPDF


class billing:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+250+190")
        self.root.title("Bright Bazaar")
        self.root.config(bg="White")
        self.cart_list=[]
        self.chk_print=0
        # title
        self.icon_title=PhotoImage(file="images/logo1.png")
        self.title=Label(self.root,text="Bright Bazaar",image=self.icon_title,compound="left",font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        # button logout
        btn_logout=Button(self.root,text="Logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1100,y=5,height=50,width=150)

        # clock
        self.lbl_clock=Label(self.root,text="Welcome Bright Bazaar\t\t Date:DD-MM-YYYY\t\t Time:HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

    #product frame
        product_frame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        product_frame1.place(x=6,y=110,width=410,height=550)

        p_title=Label(product_frame1,text="All products",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

        # search frame
        # variable
        self.var_search=StringVar()
        product_frame2=Frame(product_frame1,bd=2,relief=RIDGE,bg="white")
        product_frame2.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(product_frame2,text="Search Product | By Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)
        
        lbl_search=Label(product_frame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=5,y=45)
        txt_search=Entry(product_frame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=130,y=50,width=150,height=22)
        btn_search=Button(product_frame2,command=self.search,text="Search",font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=285,y=47,width=100,height=25)
        btn_show_all=Button(product_frame2,command=self.show,text="Show All",font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=285,y=10,width=100,height=25)

        # Product Details
        product_frame3 = Frame(product_frame1, bd=3, relief=RIDGE)
        product_frame3.place(x=2, y=140, width=398, height=375)

        scrolly = Scrollbar(product_frame3, orient=VERTICAL)
        scrollx = Scrollbar(product_frame3, orient=HORIZONTAL)

        self.productTable = ttk.Treeview(product_frame3, columns=("pid","name", "price", "qty", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)

        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)

        self.productTable.heading("pid", text="PID")
        self.productTable.heading("name", text="Name")
        self.productTable.heading("price", text="Price")
        self.productTable.heading("qty", text="QTY")
        self.productTable.heading("status", text="Status")
        self.productTable["show"] = "headings"

        self.productTable.column("pid", width=30)
        self.productTable.column("name", width=100)
        self.productTable.column("price", width=100)
        self.productTable.column("qty", width=40)
        self.productTable.column("status", width=90)
        self.productTable.bind("<ButtonRelease-1>", self.get_data)

        self.productTable.pack(fill=BOTH, expand=1)
        lbl_note=Label(product_frame1,text="Note: Enter 0 QTY To Remove Product From Cart",font=("goudy old style",12,"bold"),anchor=W,bg="white",fg="red").pack(side=BOTTOM,fill=X)
        
        self.show()

#product frame

        # variable
        self.var_c_name=StringVar()
        self.var_c_contact=StringVar()


        customer_frame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        customer_frame.place(x=420,y=110,width=530,height=70)

        c_title=Label(customer_frame,text="Customer Details",font=("goudy old style",15),bg="lightgrey").pack(side=TOP,fill=X)
        lbl_name=Label(customer_frame,text="Name",font=("times new roman",15),bg="white").place(x=5,y=35)
        txt_name=Entry(customer_frame,textvariable=self.var_c_name,font=("times new roman",15),bg="lightyellow").place(x=80,y=35,width=180)
        
        lbl_contact=Label(customer_frame,text="Contact",font=("times new roman",15),bg="white").place(x=270,y=35)
        txt_contact=Entry(customer_frame,textvariable=self.var_c_contact,font=("times new roman",15),bg="lightyellow").place(x=380,y=35,width=140)
        
        # calculater and cart frame
        cal_cart_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        cal_cart_frame.place(x=420,y=190,width=530,height=360)

        # calculato frame
        # variable
        self.var_cal_input=StringVar()


        cal_frame=Frame(cal_cart_frame,bd=8,relief=RIDGE,bg="white")
        cal_frame.place(x=5,y=10,width=268,height=340)

        txt_cat_input=Entry(cal_frame,textvariable=self.var_cal_input,font=("arial",15,"bold"),width=21,bd=10,relief=GROOVE,state="readonly",justify=RIGHT)
        txt_cat_input.grid(row=0,columnspan=4)

        btn_7=Button(cal_frame,text="7",font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=0)
        btn_8=Button(cal_frame,text="8",font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=1)
        btn_9=Button(cal_frame,text="9",font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=2)
        btn_sum=Button(cal_frame,text="+",font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=3)

        btn_4=Button(cal_frame,text="4",font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=0)
        btn_5=Button(cal_frame,text="5",font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=1)
        btn_6=Button(cal_frame,text="6",font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=2)
        btn_sub=Button(cal_frame,text="-",font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=3)

        btn_3=Button(cal_frame,text="3",font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=0)
        btn_2=Button(cal_frame,text="2",font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=1)
        btn_1=Button(cal_frame,text="1",font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=2)
        btn_mul=Button(cal_frame,text="*",font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=3)

        btn_0=Button(cal_frame,text="0",font=('arial',15,'bold'),command=lambda:self.get_input(0),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=0)
        btn_c=Button(cal_frame,text="C",font=('arial',15,'bold'),command=self.clear_cal,bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=1)
        btn_eq=Button(cal_frame,text="=",font=('arial',15,'bold'),command=self.perform_cal,bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(cal_frame,text="/",font=('arial',15,'bold'),command=lambda:self.get_input('/'),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=3)



        # Cart Details
        cart_frame = Frame(cal_cart_frame, bd=3, relief=RIDGE)
        cart_frame.place(x=280, y=8, width=245, height=342)
        self.cart_title=Label(cart_frame,text="Cart\tTotal Product: [0]",font=("goudy old style",15),bg="lightgrey")
        self.cart_title.pack(side=TOP,fill=X)

        scrolly = Scrollbar(cart_frame, orient=VERTICAL)
        scrollx = Scrollbar(cart_frame, orient=HORIZONTAL)

        self.cartTable = ttk.Treeview(cart_frame, columns=("pid","name", "price", "qty"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)

        scrollx.config(command=self.cartTable.xview)
        scrolly.config(command=self.cartTable.yview)

        self.cartTable.heading("pid", text="PID")
        self.cartTable.heading("name", text="Name")
        self.cartTable.heading("price", text="Price")
        self.cartTable.heading("qty", text="Qty")
        self.cartTable["show"] = "headings"

        self.cartTable.column("pid", width=40)
        self.cartTable.column("name", width=100)
        self.cartTable.column("price", width=90)
        self.cartTable.column("qty", width=30)
        self.cartTable.bind("<ButtonRelease-1>", self.get_data_cart)
        self.cartTable.pack(fill=BOTH, expand=1)

        # Add cart widgeds frame

        # variable
        self.var_pid=StringVar()
        self.var_p_name=StringVar()
        self.var_p_price=StringVar()
        self.var_p_qty=StringVar()
        self.var_p_stock=StringVar()
        
        add_card_widgets_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        add_card_widgets_frame.place(x=420,y=550,width=530,height=110)

        lbl_p_name=Label(add_card_widgets_frame,text="Product Name",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_p_name=Entry(add_card_widgets_frame,textvariable=self.var_p_name,font=("times new roman",15),bg="lightyellow",state="readonly").place(x=5,y=35,width=190,height=22)

        lbl_p_price=Label(add_card_widgets_frame,text="Price Per QTY",font=("times new roman",15),bg="white").place(x=230,y=5)
        txt_p_price=Entry(add_card_widgets_frame,textvariable=self.var_p_price,font=("times new roman",15),bg="lightyellow",state="readonly").place(x=230,y=35,width=150,height=22)

        lbl_p_qty=Label(add_card_widgets_frame,text="Quantity",font=("times new roman",15),bg="white").place(x=390,y=5)
        txt_p_qty=Entry(add_card_widgets_frame,textvariable=self.var_p_qty,font=("times new roman",15),bg="lightyellow").place(x=390,y=35,width=120,height=22)

        self.lbl_instock=Label(add_card_widgets_frame,text="In Stock",font=("times new roman",15),bg="white")
        self.lbl_instock.place(x=5,y=70)

        btn_clear_cart=Button(add_card_widgets_frame,command=self.clear_cart,text="Clear",font=("times new roman",15,"bold"),bg="lightgrey",cursor="hand2").place(x=180,y=70,width=150,height=30)
        btn_add_cart=Button(add_card_widgets_frame,command=self.add_update_cart,text="Add | Update Cart",font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=340,y=70,width=180,height=30)


# billing frame

        # billing area
        bill_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        bill_frame.place(x=953,y=110,width=390,height=410)

        bill_title=Label(bill_frame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(bill_frame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(bill_frame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)


        # billing buttons
        bill_menu_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        bill_menu_frame.place(x=953,y=520,width=390,height=140)

        self.lbl_amount=Label(bill_menu_frame,text="Bill Amount\n 0",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amount.place(x=2,y=5,width=120,height=70)

        self.lbl_discount=Label(bill_menu_frame,text="Discount\n [5%]",font=("goudy old style",15,"bold"),bg="#8bc34a",fg="white")
        self.lbl_discount.place(x=124,y=5,width=120,height=70)

        self.lbl_net_pay=Label(bill_menu_frame,text="Ne Pay\n 0",font=("goudy old style",15,"bold"),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=246,y=5,width=140,height=70)

        btn_print=Button(bill_menu_frame,command=self.print_bill,text="Print",font=("goudy old style",15,"bold"),bg="lightgrey",cursor="hand2")
        btn_print.place(x=2,y=80,width=120,height=50)

        btn_clear_all=Button(bill_menu_frame,command=self.clear_all,text="Clear All",font=("goudy old style",15,"bold"),bg="gray",fg="white",cursor="hand2")
        btn_clear_all.place(x=124,y=80,width=120,height=50)

        btn_generate=Button(bill_menu_frame,command=self.generate_bill,text="Generate Bill",font=("goudy old style",15,"bold"),bg="#009688",fg="white",cursor="hand2")
        btn_generate.place(x=246,y=80,width=140,height=50)


# footer
        footer=Label(self.root,text="IMS by Bansal Manavadariya",font=("times new roman",15),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
        
        self.update_date_time()



# All Function

    # function for calculator
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)    

    def clear_cal(self):
        self.var_cal_input.set("")

    def perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

        
    def show(self):
        try:
            con = sqlite3.connect('ims.db')
            cur = con.cursor()
            cur.execute("SELECT pid,name,price,qty,status FROM product where status='Active'")
            rows = cur.fetchall()
            self.productTable.delete(*self.productTable.get_children())
            for row in rows:
                self.productTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search(self):
            con = sqlite3.connect('ims.db')
            cur = con.cursor()
            try:
                if self.var_search.get() == "":
                    messagebox.showerror("Error", "Search input should be required", parent=self.root) 
                else:
                    cur.execute("SELECT pid,name,price,qty,status FROM product WHERE name LIKE '%"+self.var_search.get()+"%' and status='Active'" )
                    rows = cur.fetchall()
                    if len(rows) != 0:
                        self.productTable.delete(*self.productTable.get_children())
                        for row in rows:
                            self.productTable.insert('', END, values=row)
                    else:
                        messagebox.showerror("Error", "No record found!", parent=self.root)
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
            finally:
                con.close()
    
    def get_data(self, ev):
        f = self.productTable.focus()
        content = self.productTable.item(f)
        row = content['values']
        self.var_pid.set(row[0])
        self.var_p_name.set(row[1]) 
        self.var_p_price.set(row[2])
        self.lbl_instock.config(text=f"In Stock [{str(row[3])}]")
        self.var_p_stock.set(row[3])
        self.var_p_qty.set("1")

    def get_data_cart(self, ev):
        f = self.cartTable.focus()
        content = self.cartTable.item(f)
        row = content['values']
        self.var_pid.set(row[0])
        self.var_p_name.set(row[1]) 
        self.var_p_price.set(row[2])
        self.var_p_qty.set(row[3])
        self.lbl_instock.config(text=f"In Stock [{str(row[4])}]")
        self.var_p_stock.set(row[4])

    def add_update_cart(self):
        if self.var_pid.get() == "":
            messagebox.showerror("Error", "Select product first!", parent=self.root)
        elif self.var_p_qty.get()=='':
            messagebox.showerror("Error", "Quantity should be required", parent=self.root)
        elif int(self.var_p_qty.get()) > int(self.var_p_stock.get()):
            messagebox.showerror("Error", "Invalid Quantity", parent=self.root)
        else:
            # price_cal=int(self.var_p_qty.get())*float(self.var_p_price.get())
            # price_cal=float(price_cal)

            price_cal=self.var_p_price.get()
            cart_data=[self.var_pid.get(),self.var_p_name.get(),price_cal,self.var_p_qty.get(),self.var_p_stock.get()]
            

            # update cart
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            
            if present=='yes':
                op=messagebox.askyesno('Conform',"Prodcut Alredy present\nDo you want to Update| Remove from cart list",parent=self.root)

                if op==True:
                    if self.var_p_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        # self.cart_list[index_][2]=price_cal
                        self.cart_list[index_][3]=self.var_p_qty.get()
            else:
                self.cart_list.append(cart_data)

            self.show_cart()
            self.bill_update()

    def bill_update(self):
        self.bill_amount=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
             self.bill_amount=self.bill_amount+(float(row[2])*int(row[3]))
        
        self.discount=(self.bill_amount*5)/100
        self.net_pay=self.bill_amount-self.discount
        self.lbl_amount.config(text=f"Bill Amount\n{str(self.bill_amount)}")
        self.lbl_net_pay.config(text=f"Net Pay\n{str(self.net_pay)}")
        self.cart_title.config(text=f"Cart\tTotal Products[{str(len(self.cart_list))}]")

    def show_cart(self):
        try:
            self.cartTable.delete(*self.cartTable.get_children())
            for row in self.cart_list:
                self.cartTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        

    def generate_bill(self):
        if self.var_c_name.get()=='' or self.var_c_contact.get()=='':
            messagebox.showerror("Error", f"Customer Detail are required", parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error", f"Please Add Product in Cart", parent=self.root)
        else:
            self.bill_top()
            self.bill_middle()
            self.bill_bottom()

            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('saved','Bill has been Generated/save in Bill Folder.')

            self.chk_print=1

    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%y"))
        bill_top_temp=f'''
\t\tBright Bazaar
\t Phone No.6352541557,Surat 395006
{str("="*45)}
 Customer Name: {self.var_c_name.get()}
 Ph no. : {self.var_c_contact.get()}
 BIll No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*45)}
 Product Name\t\t\tQTY\tPrice
{str("="*45)}
        '''
        
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_bottom(self):
            bill_bottom_temp=f'''
{str("="*45)}
 Bill Amount\t\t\t\tRs.{self.bill_amount}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*45)}\n
        '''
            self.txt_bill_area.insert(END,bill_bottom_temp)

    def bill_middle(self):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        try:
            for row in self.cart_list:
                
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])

                if int(row[3])==int(row[4]):
                    status='Inactive'
                if int(row[3])!=int(row[4]):
                    status='Active'

                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
              # update qty in product table
                cur.execute('Update product set qty=?, status=? WHERE pid=?',(
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        
    def clear_cart(self):
        self.var_pid.set("")
        self.var_p_name.set("") 
        self.var_p_price.set("")
        self.var_p_qty.set("")
        self.lbl_instock.config(text=f"In Stock")
        self.var_p_stock.set("")

    def clear_all(self): 
        del self.cart_list[:]
        self.var_c_name.set("")
        self.var_c_contact.set("")
        self.txt_bill_area.delete('1.0',END)
        self.cart_title.config(text=f"Cart\tTotal Products [0]")
        self.var_search.set("")
        self.chk_print=0
        self.clear_cart()
        self.show()
        self.show_cart()

    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d/%m/%Y")
        self.lbl_clock.config(text=f"Welcome Bright Bazaar\t\t Date:{str(date_)}\t\t Time:{str(time_)}",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()

        if self.chk_print == 1:
            messagebox.showinfo('Print', 'Please wait while printing', parent=self.root)

            # Fetch data
            # bill = self.fetch_bill_data(self.invoice)

            # Create a temporary file with a .pdf extension
            new_file = tempfile.mktemp('.pdf')

            # Initialize FPDF2 and create a PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)

            # Add a title and some styling
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, 'Invoice', ln=True, align='C')
            pdf.ln(10)

            # Add headers from fetched data
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, 'Bill To:', ln=True)
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, f'Customer Name: {self.var_c_name.get()}', ln=True)  # Example placeholder
            pdf.cell(0, 10, f'Contact No.: {self.var_c_contact.get()}', ln=True)  # Example placeholder
            pdf.cell(0, 10, f'Date: {time.strftime("%d/%m/%Y")}', ln=True)  # Example placeholder
            pdf.ln(10)

            # Draw a line
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(80, 10, 'Product Name', border=1)
            pdf.cell(40, 10, 'Price', border=1)
            pdf.cell(40, 10, 'Quantity', border=1)
            pdf.cell(0, 10, 'Total', border=1, ln=True)
            pdf.set_font("Arial", size=12)

            # Add items from fetched data
            total_amount = 0
            for row in self.cart_list:
                product_name = row[1]
                price = float(row[2])  # Convert price to float
                quantity = int(row[3])  # Convert quantity to integer

                pdf.cell(80, 10, product_name, border=1)  # Product Name
                pdf.cell(40, 10, f'${price:.2f}', border=1)  # Price
                pdf.cell(40, 10, str(quantity), border=1)  # Quantity
                item_total = price * quantity  # Calculate total for the item
                pdf.cell(0, 10, f'${item_total:.2f}', border=1, ln=True)  # Total for this item
                total_amount += item_total  # Add to the total amount

            # Calculate discount
            discount = total_amount * 0.05  # 5% discount
            discounted_total = total_amount - discount

            pdf.ln(10)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(120, 10, 'Total Amount:', 0)
            pdf.cell(0, 10, f'${total_amount:.2f}', 0, ln=True)

            # Add discount and final total
            pdf.cell(120, 10, 'Discount (5%):', 0)
            pdf.cell(0, 10, f'-${discount:.2f}', 0, ln=True)
            pdf.cell(120, 10, 'Total After Discount:', 0)
            pdf.cell(0, 10, f'${discounted_total:.2f}', 0, ln=True)

            # Save the PDF to the temporary file
            pdf.output(new_file)

            # Print the temporary PDF file directly without opening save dialog
            os.startfile(new_file, "print")
        else:
            messagebox.showerror('Print', 'Please generate bill', parent=self.root)

if __name__=="__main__":
    root=Tk()
    obj=billing(root)
    root.mainloop() 