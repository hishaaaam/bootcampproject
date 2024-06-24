import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import random

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
                password="hisham@45",
                database="ola"
            )
            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO Users (UName, Address, Email, PhoneNumber, PasswordHash) VALUES (%s, %s, %s, %s, %s)",
                             (uname, address, email, phone, password))
            mydb.commit()
            messagebox.showinfo("Success", "User registered successfully")
            sign_up_window.destroy()
        except Error as e:
            messagebox.showerror("Error", f"Error registering user: {e}")
        finally:
            if mycursor:
                mycursor.close()
            if 'mydb' in locals():
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
        mycursor = None

        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="hisham@45",
                database="ola"
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM Users WHERE Email = %s AND PasswordHash = %s", (email, password))
            user = mycursor.fetchone()
            if user:
                messagebox.showinfo("Success", f"Welcome {user[1]}!")  # user[1] is the username (UName)
                sign_in_window.destroy()
                open_booking_page(user[0])  # user[0] is the UserID
            else:
                messagebox.showerror("Error", "Invalid Email or Password")
        except Error as e:
            messagebox.showerror("Error", f"Error signing in: {e}")
        finally:
            if mycursor:
                mycursor.close()
            if 'mydb' in locals():
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

# Booking page function
def open_booking_page(user_id):
    def load_vehicle_types():
        mycursor = None
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="hisham@45",
                database="ola"
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT DISTINCT VehicleType FROM Vehicles")
            vehicle_types = [row[0] for row in mycursor.fetchall()]
            return vehicle_types
        except Error as e:
            messagebox.showerror("Error", f"Error fetching vehicle types: {e}")
        finally:
            if mycursor:
                mycursor.close()
            if 'mydb' in locals():
                mydb.close()

    def load_pickup_locations():
        mycursor = None
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="hisham@45",
                database="ola"
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT DISTINCT Address FROM Drivers WHERE IsActive = 1")
            locations = [row[0] for row in mycursor.fetchall()]
            return locations
        except Error as e:
            messagebox.showerror("Error", f"Error fetching pickup locations: {e}")
        finally:
            if mycursor:
                mycursor.close()
            if 'mydb' in locals():
                mydb.close()

    def load_random_vehicle(vehicle_type, pickup_location):
        mycursor = None
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="hisham@45",
                database="ola"
            )
            mycursor = mydb.cursor()
            mycursor.execute("""
                SELECT VehicleID, Model, RegistrationNumber
                FROM Vehicles
                WHERE VehicleType = %s AND VehicleID IN (
                    SELECT VehicleID FROM Drivers WHERE Address = %s AND IsActive = 1
                )
            """, (vehicle_type, pickup_location))
            vehicles = mycursor.fetchall()
            if vehicles:
                return random.choice(vehicles)
            else:
                return None
        except Error as e:
            messagebox.showerror("Error", f"Error fetching vehicles: {e}")
        finally:
            if mycursor:
                mycursor.close()
            if 'mydb' in locals():
                mydb.close()

    def confirm_booking():
        mycursor = None
        try:
            vehicle_type = combo_vehicle_type.get()
            pickup_location = combo_pickup.get()
            dropoff_location = entry_dropoff.get()

            selected_vehicle = load_random_vehicle(vehicle_type, pickup_location)
            if not selected_vehicle:
                messagebox.showerror("Error", "No available vehicles found for the selected type and location.")
                return

            vehicle_id, vehicle_model, vehicle_registration = selected_vehicle

            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="hisham@45",
                database="ola"
            )
            mycursor = mydb.cursor()
            mycursor.execute("""
                SELECT DriverID FROM Drivers WHERE VehicleID = %s
            """, (vehicle_id,))
            driver_id = mycursor.fetchone()[0]

            mycursor.execute("""
                INSERT INTO Rides (UserID, DriverID, VehicleID, PickupLocation, DropoffLocation, Status)
                VALUES (%s, %s, %s, %s, %s, 'Confirmed')
            """, (user_id, driver_id, vehicle_id, pickup_location, dropoff_location))
            mydb.commit()

            ride_id = mycursor.lastrowid

            # Fetch booking summary details
            mycursor.execute("""
                SELECT UName, DName, VehicleType, Model, RegistrationNumber
                FROM Rides
                JOIN Users ON Rides.UserID = Users.UserID
                JOIN Drivers ON Rides.DriverID = Drivers.DriverID
                JOIN Vehicles ON Rides.VehicleID = Vehicles.VehicleID
                WHERE Rides.RideID = %s
            """, (ride_id,))
            summary = mycursor.fetchone()

            messagebox.showinfo("Booking Confirmed", f"Your booking has been confirmed!\n\nUser: {summary[0]}\nDriver: {summary[1]}\nVehicle: {summary[2]} {summary[3]} ({summary[4]})")

            booking_window.destroy()
        except Error as e:
            messagebox.showerror("Error", f"Error confirming booking: {e}")
        finally:
            if mycursor:
                mycursor.close()
            if 'mydb' in locals():
                mydb.close()

    booking_window = tk.Toplevel(root)
    booking_window.title("Book a Ride")
    booking_window.geometry("400x400")

    tk.Label(booking_window, text="OLA CABS", fg="blue", font=('Helvetica', 15, 'bold')).pack(pady=10)

    tk.Label(booking_window, text="Pickup Location", font=('Helvetica', 12)).pack(pady=5)
    combo_pickup = ttk.Combobox(booking_window)
    combo_pickup['values'] = load_pickup_locations()
    combo_pickup.pack(pady=5)

    tk.Label(booking_window, text="Dropoff Location", font=('Helvetica', 12)).pack(pady=5)
    entry_dropoff = tk.Entry(booking_window)
    entry_dropoff.pack(pady=5)

    tk.Label(booking_window, text="Vehicle Type", font=('Helvetica', 12)).pack(pady=5)
    combo_vehicle_type = ttk.Combobox(booking_window)
    combo_vehicle_type['values'] = load_vehicle_types()
    combo_vehicle_type.pack(pady=5)

    tk.Button(booking_window, text="Confirm Booking", command=confirm_booking, fg="white", bg="blue").pack(pady=20)


# Main Window
root = tk.Tk()
root.title("OLA Booking App")
root.geometry("200x150")

tk.Button(root, text="Sign Up", command=sign_up, fg="white", bg="blue").pack(pady=10)
tk.Button(root, text="Sign In", command=sign_in, fg="white", bg="blue").pack(pady=10)

root.mainloop()
