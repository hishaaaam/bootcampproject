import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error


# sign up function
def sign_up():
    def register_user():
        uname = entry_uname.get()
        address = entry_address.get()
        email = entry_email.get()
        phone = entry_phone.get()
        password = entry_password.get()

        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="aadhil1234",
                database="ola"
            )
            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO Users (Username, Address, Email, Phone, Password) VALUES (%s, %s, %s, %s, %s)",
                             (uname, address, email, phone, password))
            mydb.commit()
            messagebox.showinfo("Success", "User registered successfully")
            sign_up_window.destroy()
        except Error as e:
            messagebox.showerror("Error", f"Error registering user: {e}")
        finally:
            mycursor.close()
            mydb.close()

    sign_up_window = tk.Toplevel(root)
    sign_up_window.title("Sign up")
    sign_up_window.geometry("350x300")

    tk.Label(sign_up_window, text="OLA CABS", fg="blue", font=('Helvetica', 15, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

    
    tk.Label(sign_up_window, text="Username", font=('Helvetica', 12)).grid(row=1, column=0, padx=10, pady=5)
    entry_uname = tk.Entry(sign_up_window)
    entry_uname.grid(row=1, column=1, padx=10, pady=5)

    
    tk.Label(sign_up_window, text="Address", font=('Helvetica', 12)).grid(row=2, column=0, padx=10, pady=5)
    entry_address = tk.Entry(sign_up_window)
    entry_address.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(sign_up_window, text="Email", font=('Helvetica', 12)).grid(row=3, column=0, padx=10, pady=5)
    entry_email = tk.Entry(sign_up_window)
    entry_email.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(sign_up_window, text="Phone Number", font=('Helvetica', 12)).grid(row=4, column=0, padx=10, pady=5)
    entry_phone = tk.Entry(sign_up_window)
    entry_phone.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(sign_up_window, text="Password", font=('Helvetica', 12)).grid(row=5, column=0, padx=10, pady=5)
    entry_password = tk.Entry(sign_up_window, show="*")
    entry_password.grid(row=5, column=1, padx=10, pady=5)

    tk.Button(sign_up_window, text="Register", command=register_user, fg="white", bg="blue").grid(row=6, column=1, pady=10)

# sign in function
def sign_in():
    def authenticate_user():
        email = entry_email.get()
        password = entry_password.get()

        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="aadhil1234",
                database="ola"
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM Users WHERE Email = %s AND Password = %s", (email, password))
            user = mycursor.fetchone()
            if user:
                messagebox.showinfo("Success", f"Welcome {user[0]}!")
                sign_in_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid Email or Password")
        except Error as e:
            messagebox.showerror("Error", f"Error signing in: {e}")
        finally:
            mycursor.close()
            mydb.close()

    sign_in_window = tk.Toplevel(root)
    sign_in_window.title("Sign In")
    sign_in_window.geometry("350x200")

    tk.Label(sign_in_window, text="OLA CABS", fg="blue", font=("Helvetica", 15, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(sign_in_window, text="Email", font=('Helvetica', 12)).grid(row=1, column=0, padx=10, pady=5)
    entry_email = tk.Entry(sign_in_window)
    entry_email.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(sign_in_window, text="Password", font=('Helvetica', 12)).grid(row=2, column=0, padx=10, pady=5)
    entry_password = tk.Entry(sign_in_window, show="*")
    entry_password.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(sign_in_window, text="Sign In", command=authenticate_user, fg="white", bg="blue").grid(row=3, column=1, pady=10)

# Main Window
root = tk.Tk()
root.title("OLA Booking App")
root.geometry("200x150")

tk.Button(root, text="Sign Up", command=sign_up, fg="white", bg="blue").pack(pady=10)
tk.Button(root, text="Sign In", command=sign_in, fg="white", bg="blue").pack(pady=10)

root.mainloop()
