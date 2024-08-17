import sqlite3
import subprocess
from tkinter import *
from tkinter import messagebox

# Connect to SQLite database
conn = sqlite3.connect('ims.db')
cursor = conn.cursor()

# Function to check login credentials
def login():
    eid = entry_eid.get()
    password = entry_password.get()
    
    print(f"Attempting login with EID: {eid} and Password: {password}")

    # Fetch user details from the employee table
    cursor.execute("SELECT LOWER(utype) FROM employee WHERE eid=? AND pass=?", (eid, password))
    user = cursor.fetchone()
    
    print(f"Query result: {user}")

    if user:
        utype = user[0]
        if utype == "admin":
            root.destroy()  # Close the login window
            subprocess.run(["python", "dashbord.py"])  # Launch dashboard
        elif utype == "employee":
            root.destroy()  # Close the login window
            subprocess.run(["python", "billing.py"])  # Launch billing system
    else:
        messagebox.showerror("Error", "Invalid Employee ID or Password")
        

# Tkinter window setup
root = Tk()
root.title("Login")
root.geometry("600x500")  # Increased window size
root.configure(bg="#f0f0f0")  # Light background color

# Centering the window
root.eval('tk::PlaceWindow . center')

# Font settings
header_font = ("Arial", 24, "bold")
label_font = ("Arial", 14)
entry_font = ("Arial", 14)
button_font = ("Arial", 16, "bold")

# Header or Logo (Optional)
header_label = Label(root, text="Welcome to IMS Login", font=header_font, bg="#f0f0f0", fg="#333")
header_label.pack(pady=40)

# Frame for organizing input fields
input_frame = Frame(root, bg="#f0f0f0")
input_frame.pack(pady=20)

# Employee ID Label and Entry
label_eid = Label(input_frame, text="Employee ID", font=label_font, bg="#f0f0f0")
label_eid.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_eid = Entry(input_frame, font=entry_font, bd=2, relief="groove")
entry_eid.grid(row=0, column=1, padx=10, pady=10)

# Password Label and Entry
label_password = Label(input_frame, text="Password", font=label_font, bg="#f0f0f0")
label_password.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_password = Entry(input_frame, show="*", font=entry_font, bd=2, relief="groove")
entry_password.grid(row=1, column=1, padx=10, pady=10)

# Login Button
login_button = Button(root, text="Login", font=button_font, bg="#007acc", fg="white", bd=0, relief="ridge", command=login)
login_button.pack(pady=40, ipadx=20, ipady=10)

# Start the Tkinter loop
root.mainloop()

# Close the database connection when done
conn.close()

root.mainloop() 
