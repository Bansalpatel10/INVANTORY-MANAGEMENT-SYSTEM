from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
class supllier:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Bright Bazaar")
        self.root.config(bg="White")
        self.root.focus_force()

        # variables
       

        self.var_sup_invoice=StringVar()
        self.var_name=StringVar()
        self.var_contact=StringVar()
        self.var_searchtxt = StringVar()

  
        # search
        lbl_search = Label(self.root, text="Invoice No.", font=("goudy old style", 15), bg="white")
        lbl_search.place(x=700, y=80)
        txt_search = Entry(self.root, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow")
        txt_search.place(x=800, y=80, width=180)
        btn_search = Button(self.root, text="Search", command=self.search, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2")
        btn_search.place(x=990, y=80, width=100, height=28)
       
        # title
        title=Label(self.root,text="Supplier Details",font=("goudy old style",20,"bold"),bg="#0f4d7d",fg="white").place(x=50,y=10,width=1000,height=40)

        # contant

        # row 1
        lbl_suppiler_invoice=Label(self.root,text="Invoice No.",font=("goudy old style",15),bg="white").place(x=50,y=80)
        txt_suppiler_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=("goudy old style",15),bg="lightyellow").place(x=180,y=80,width=180)

        # row 2
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15),bg="white").place(x=50,y=120)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=180,y=120,width=180)
        # row 3
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=50,y=160)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow").place(x=180,y=160,width=180)
      
        # row 4
        lbl_desc=Label(self.root,text="Description",font=("goudy old style",15),bg="white").place(x=50,y=200) 
        self.txt_desc=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_desc.place(x=180,y=200,width=470,height=90)
       

        # buttons
        btn_add=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=180,y=320,width=110,height=35)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=300,y=320,width=110,height=35)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=420,y=320,width=110,height=35)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=540,y=320,width=110,height=35)


        # supplier details

        sup_frame=Frame(self.root,bd=3,relief=RIDGE)
        sup_frame.place(x=700,y=120,width=380,height=350)
        
        scrolly=Scrollbar(sup_frame,orient=VERTICAL)
        scrollx=Scrollbar(sup_frame,orient=HORIZONTAL)

        self.supplierTable = ttk.Treeview(sup_frame, columns=("invoice", "name", "contact","desc"),yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)      

        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.pack(side=BOTTOM,fill=X)

        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)
        
        self.supplierTable.heading("invoice",text="EMP ID")
        self.supplierTable.heading("name",text="NAME")
        self.supplierTable.heading("contact",text="CONTACT")
        self.supplierTable.heading("desc",text="DESCRIPTON")
        self.supplierTable["show"]="headings"

        self.supplierTable.column("invoice",width=90)
        self.supplierTable.column("name",width=100)
        self.supplierTable.column("contact",width=100)
        self.supplierTable.column("desc",width=100)
        self.supplierTable.pack(fill=BOTH,expand=1)
        self.supplierTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()


# function for database
    def add(self):
        if self.var_sup_invoice.get() == "":
            messagebox.showerror("Error", "Invoice is required", parent=self.root)
        else:
            try:
                con = sqlite3.connect('ims.db')
                cur = con.cursor()

                # Check if the invoice already exists
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Invoice number already exists. Please try a different one.", parent=self.root)
                else:
                    cur.execute("INSERT INTO supplier (invoice, name, contact, desc) VALUES (?, ?, ?, ?)",
                                (
                                    self.var_sup_invoice.get(),
                                    self.var_name.get(),
                                    self.var_contact.get(),
                                    self.txt_desc.get('1.0', END),
                                ))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier added successfully", parent=self.root)
                    self.show()
                    self.clear()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
            finally:
                con.close()

    def update(self):
        if self.var_sup_invoice.get() == "":
            messagebox.showerror("Error", "Invoice is required", parent=self.root)
        else:
            try:
                con = sqlite3.connect('ims.db')
                cur = con.cursor()

                # Check if the invoice exists before updating
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Invoice number. Please select the supplier from the list.", parent=self.root)
                else:
                    cur.execute("""
                        UPDATE supplier SET
                            name=?,
                            contact=?,
                            desc=?
                        WHERE invoice=?
                    """, (
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0', END),
                        self.var_sup_invoice.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier updated successfully", parent=self.root)
                    self.show()
                    self.clear()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
            finally:
                con.close()

    def delete(self):
        if self.var_sup_invoice.get() == "":
            messagebox.showerror("Error", "Invoice No. is required", parent=self.root)
        else:
            try:
                con = sqlite3.connect('ims.db')
                cur = con.cursor()

                # Check if the invoice exists before deleting
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Invoice number. Please select the supplier from the list.", parent=self.root)
                else:
                    cur.execute("DELETE FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier deleted successfully", parent=self.root)
                    self.show()
                    self.clear()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
            finally:
                con.close()

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0', END)
        self.var_searchtxt.set("")
        self.supplierTable.selection_remove(self.supplierTable.selection())

    def search(self):
        if self.var_searchtxt.get() == "":
            messagebox.showerror("Error", "Invoice No. is required", parent=self.root)
        else:
            try:
                con = sqlite3.connect('ims.db')
                cur = con.cursor()
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_searchtxt.get(),))
                row = cur.fetchone()
                if row is not None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
            finally:
                con.close()

    def show(self):
        try:
            con = sqlite3.connect('ims.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM supplier")
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.supplierTable.focus()
        content = self.supplierTable.item(f)
        row = content['values']
        
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0', END)
        self.txt_desc.insert(END, row[3])

if __name__=="__main__":
    root=Tk()
    obj=supllier(root)
    root.mainloop() 