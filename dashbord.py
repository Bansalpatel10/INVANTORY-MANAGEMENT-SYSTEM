import sqlite3
import sys
import time
from tkinter import*
from tkinter import messagebox
from PIL import Image,ImageTk
from employe import emplyee
from supplier import supllier
from category import category
from product import product
from sales import sales
import os
class IMS:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="White")

        # title
        self.icon_title=PhotoImage(file="images/logo1.png")
        self.title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound="left",font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        # button logout
        btn_logout=Button(self.root,command=self.logout,text="Logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1100,y=5,height=50,width=150)

        # clock
        self.lbl_clock=Label(self.root,text="Welcome Inventory Management System\t\t Date:DD-MM-YYYY\t\t Time:HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        # left menu
        self.menulogo=Image.open("images/menu_im.png")
        self.menulogo=self.menulogo.resize((200,200),Image.LANCZOS)
        self.menulogo=ImageTk.PhotoImage(self.menulogo)

        leftmenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        leftmenu.place(x=0,y=102,width=200,height=570)

        lbl_menulogo=Label(leftmenu,image=self.menulogo)
        lbl_menulogo.pack(side=TOP,fill=X)

        self.icon_side=PhotoImage(file="images/side.png")
        lbl_menu=Label(leftmenu,text="Menu",font=("times new roman",20),bg="#009688").pack(side="top",fill=X)

        btn_employe=Button(leftmenu,text="Employee",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2",command=self.employee).pack(side=TOP,fill=X)
        btn_supplier=Button(leftmenu,text="Supplier",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2",command=self.supllier).pack(side=TOP,fill=X)
        btn_category=Button(leftmenu,text="Category",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2",command=self.category).pack(side=TOP,fill=X)
        btn_product=Button(leftmenu,text="Product",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2",command=self.product).pack(side=TOP,fill=X)
        btn_sale=Button(leftmenu,text="Sale",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2",command=self.sales).pack(side=TOP,fill=X)
        btn_exit=Button(leftmenu,text="Exit",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2",command=self.exit_app).pack(side=TOP,fill=X)

        # content
        self.lbl_employee=Label(self.root,text="Total Employee\n[ 0 ]",bg="#33bbf9",fg="white",font=("times new roman",20,"bold"),bd=5,relief=RIDGE)
        self.lbl_employee.place(x=300,y=120,height=150,width=300)

        self.lbl_supplier=Label(self.root,text="Total Suppiler\n[ 0 ]",bg="#ff5722",fg="white",font=("times new roman",20,"bold"),bd=5,relief=RIDGE)
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)

        self.lbl_categorie=Label(self.root,text="Total Categorie\n[ 0 ]",bg="#009688",fg="white",font=("times new roman",20,"bold"),bd=5,relief=RIDGE)
        self.lbl_categorie.place(x=1000,y=120,height=150,width=300)

        self.lbl_Product=Label(self.root,text="Total Product\n[ 0 ]",bg="#607d85",fg="white",font=("times new roman",20,"bold"),bd=5,relief=RIDGE)
        self.lbl_Product.place(x=300,y=300,height=150,width=300)

        self.lbl_sale=Label(self.root,text="Total Sales\n[ 0 ]",bg="#ffc107",fg="white",font=("times new roman",20,"bold"),bd=5,relief=RIDGE)
        self.lbl_sale.place(x=650,y=300,height=150,width=300)

        # footer
        lbl_footer=Label(self.root,text="IMS by Bansal Manavadariya",font=("times new roman",15),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)


        self.update_content()
        
# buttons working

    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=emplyee(self.new_win)

    def supllier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supllier(self.new_win)
    
    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=category(self.new_win)

    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=product(self.new_win)

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=sales(self.new_win)
    
    def update_content(self):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        try:
            # Fetching product data
            cur.execute("select * from product")
            product = cur.fetchall()
            self.lbl_Product.config(text=f"Total Product\n[ {str(len(product))} ]")

            # Fetching supplier data
            cur.execute("select * from supplier")
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f"Total Supplier\n[ {str(len(supplier))} ]")

            # Fetching employee data
            cur.execute("select * from employee")
            employee = cur.fetchall()
            self.lbl_employee.config(text=f"Total Employee\n[ {str(len(employee))} ]")

            # Fetching category data
            cur.execute("select * from category")
            category = cur.fetchall()
            self.lbl_categorie.config(text=f"Total Category\n[ {str(len(category))} ]")

            # Updating total sales by counting files in the 'bill' directory
            self.lbl_sale.config(text=f'Total Sale\n [{str(len(os.listdir("bill")))}]')
            
            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d/%m/%Y")
            self.lbl_clock.config(text=f"Welcome Inventory Management System\t\t Date:{str(date_)}\t\t Time:{str(time_)}",font=("times new roman",15),bg="#4d636d",fg="white")
            self.lbl_clock.after(200,self.update_content)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()  # Close the database connection
    
    def logout(self):
        self.root.destroy()
        os.system('python login.py')  # Reopen the login page
    
    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=self.root):
            self.root.destroy()
            sys.exit()  # Terminate the program


    
if __name__=="__main__":
    root=Tk()
    obj=IMS(root)
    root.mainloop() 