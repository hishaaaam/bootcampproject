import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime

# Global variable to track current user ID
current_user_id = None

# Function to establish a database connection
def connect_to_database():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="aadhil1234",
            database="ola"
        )
        mycursor = mydb.cursor()
        return mydb, mycursor

    except Error as e:
        messagebox.showerror("Database Connection Error", f"Error connecting to database: {e}")
        return None, None

# Function to load pickup locations
def load_pickup_locations():
    try:
        mydb, mycursor = connect_to_database()
        if mydb and mycursor:
            mycursor.execute("SELECT DISTINCT Address FROM Drivers WHERE IsActive = 1")
            locations = [row[0] for row in mycursor.fetchall()]
            return locations

    except Error as e:
        messagebox.showerror("Error", f"Error fetching pickup locations: {e}")

    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()

# Function to load vehicle types available at a pickup location
def load_vehicle_types(pickup_location):
    try:
        mydb, mycursor = connect_to_database()
        if mydb and mycursor:
            mycursor.execute("""
                SELECT DISTINCT VehicleType
                FROM Vehicles
                WHERE VehicleID IN (
                    SELECT VehicleID FROM Drivers WHERE Address = %s AND IsActive = 1
                )
            """, (pickup_location,))
            vehicle_types = [row[0] for row in mycursor.fetchall()]
            return vehicle_types

    except Error as e:
        messagebox.showerror("Error", f"Error fetching vehicle types: {e}")

    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()

# Function to load distinct modes of payment available
def load_payment_modes():
    try:
        mydb, mycursor = connect_to_database()
        if mydb and mycursor:
            mycursor.execute("SELECT DISTINCT PaymentMethod FROM Payments")
            payment_modes = [row[0] for row in mycursor.fetchall()]
            return payment_modes

    except Error as e:
        messagebox.showerror("Error", f"Error fetching payment modes: {e}")

    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()

# Function to register a new user
def sign_up():
    def register_user():
        uname = entry_uname.get()
        address = entry_address.get()
        email = entry_email.get()
        phone = entry_phone.get()
        password = entry_password.get()

        try:
            mydb, mycursor = connect_to_database()
            if mydb and mycursor:
                mycursor.execute("INSERT INTO Users (UName, Address, Email, PhoneNumber, PasswordHash) VALUES (%s, %s, %s, %s, %s)",
                                 (uname, address, email, phone, password))
                mydb.commit()
                messagebox.showinfo("Success", "User registered successfully")
                sign_up_window.destroy()
                add_logout_button(root)  # Add logout button after successful sign-up

        except Error as e:
            messagebox.showerror("Error", f"Error registering user: {e}")

        finally:
            if mycursor:
                mycursor.close()
            if mydb:
                mydb.close()

    sign_up_window = tk.Toplevel(root)
    sign_up_window.title("Sign up")
    sign_up_window.attributes('-fullscreen', True)  # Full-screen mode

    tk.Label(sign_up_window, text="OLA CABS", fg="blue", font=('Helvetica', 30, 'bold')).pack(pady=20)

    tk.Label(sign_up_window, text="Username", font=('Helvetica', 18)).pack(pady=10)
    entry_uname = tk.Entry(sign_up_window, font=('Helvetica', 18))
    entry_uname.pack(pady=5)

    tk.Label(sign_up_window, text="Address", font=('Helvetica', 18)).pack(pady=10)
    entry_address = tk.Entry(sign_up_window, font=('Helvetica', 18))
    entry_address.pack(pady=5)

    tk.Label(sign_up_window, text="Email", font=('Helvetica', 18)).pack(pady=10)
    entry_email = tk.Entry(sign_up_window, font=('Helvetica', 18))
    entry_email.pack(pady=5)

    tk.Label(sign_up_window, text="Phone Number", font=('Helvetica', 18)).pack(pady=10)
    entry_phone = tk.Entry(sign_up_window, font=('Helvetica', 18))
    entry_phone.pack(pady=5)

    tk.Label(sign_up_window, text="Password", font=('Helvetica', 18)).pack(pady=10)
    entry_password = tk.Entry(sign_up_window, show="*", font=('Helvetica', 18))
    entry_password.pack(pady=5)

    tk.Button(sign_up_window, text="Register", command=register_user, fg="white", bg="blue", font=('Helvetica', 18)).pack(pady=20)

# Function to authenticate and sign in a user
def sign_in():
    def authenticate_user():
        email = entry_email.get()
        password = entry_password.get()

        try:
            mydb, mycursor = connect_to_database()
            if mydb and mycursor:
                mycursor.execute("SELECT * FROM Users WHERE Email = %s AND PasswordHash = %s", (email, password))
                user = mycursor.fetchone()
                if user:
                    messagebox.showinfo("Success", f"Welcome {user[1]}!")  # user[1] is the username (UName)
                    sign_in_window.destroy()
                    open_booking_page(user[0])  # user[0] is the UserID
                    add_logout_button(root)  # Add logout button after successful sign-in
                else:
                    messagebox.showerror("Error", "Invalid Email or Password")

        except Error as e:
            messagebox.showerror("Error", f"Error signing in: {e}")

        finally:
            if mycursor:
                mycursor.close()
            if mydb:
                mydb.close()

    sign_in_window = tk.Toplevel(root)
    sign_in_window.title("Sign In")
    sign_in_window.attributes('-fullscreen', True)  # Full-screen mode

    tk.Label(sign_in_window, text="OLA CABS", fg="blue", font=('Helvetica', 30, 'bold')).pack(pady=20)

    tk.Label(sign_in_window, text="Email", font=('Helvetica', 18)).pack(pady=10)
    entry_email = tk.Entry(sign_in_window, font=('Helvetica', 18))
    entry_email.pack(pady=5)

    tk.Label(sign_in_window, text="Password", font=('Helvetica', 18)).pack(pady=10)
    entry_password = tk.Entry(sign_in_window, show="*", font=('Helvetica', 18))
    entry_password.pack(pady=5)

    tk.Button(sign_in_window, text="Sign In", command=authenticate_user, fg="white", bg="blue", font=('Helvetica', 18)).pack(pady=20)

# Function to add logout and exit buttons at the top of a window
def add_logout_button(window):
    def logout():
        global current_user_id
        current_user_id = None
        window.destroy()
        add_login_buttons(root)  # Add login buttons after logout

    logout_button = tk.Button(window, text="Logout", command=logout, fg="white", bg="blue", font=('Helvetica', 14))
    logout_button.pack(side=tk.RIGHT, padx=20)

    exit_button = tk.Button(window, text="Exit", command=root.destroy, fg="white", bg="red", font=('Helvetica', 14))
    exit_button.pack(side=tk.RIGHT, padx=20)

# Function to handle continuing to vehicle selection after entering pickup and drop-off locations
def continue_to_vehicle_selection(pickup_location, dropoff_location):
    vehicle_types = load_vehicle_types(pickup_location)
    if not vehicle_types:
        messagebox.showerror("Error", "No vehicles available at selected pickup location.")
        return

    vehicle_selection_window = tk.Toplevel(root)
    vehicle_selection_window.title("Select Vehicle and Payment")
    vehicle_selection_window.attributes('-fullscreen', True)  # Full-screen mode

    tk.Label(vehicle_selection_window, text="Select Vehicle Type", font=('Helvetica', 18)).pack(pady=20)
    combo_vehicle_type = ttk.Combobox(vehicle_selection_window, font=('Helvetica', 18))
    combo_vehicle_type['values'] = vehicle_types
    combo_vehicle_type.pack(pady=10)

    tk.Label(vehicle_selection_window, text="Select Mode of Payment", font=('Helvetica', 18)).pack(pady=20)
    combo_payment_mode = ttk.Combobox(vehicle_selection_window, font=('Helvetica', 18))
    combo_payment_mode['values'] = load_payment_modes()
    combo_payment_mode.pack(pady=10)

    def confirm_booking():
        vehicle_type = combo_vehicle_type.get()
        payment_mode = combo_payment_mode.get()

        if not vehicle_type or not payment_mode:
            messagebox.showerror("Error", "Please select both vehicle type and payment mode.")
            return

        mydb, mycursor = connect_to_database()
        if mydb and mycursor:
            try:
                # Insert new ride record
                ride_status = "Booked"
                fare_estimate = 100  # Placeholder for fare estimation
                pickup_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                mycursor.execute("""
                    INSERT INTO Rides (UserID, DriverID, VehicleID, PickupLocation, DropoffLocation, PickupTime, Fare, Status)
                    VALUES (%s, NULL, (SELECT VehicleID FROM Vehicles WHERE VehicleType = %s LIMIT 1), %s, %s, %s, %s, %s)
                """, (current_user_id, vehicle_type, pickup_location, dropoff_location, pickup_time, fare_estimate, ride_status))
                mydb.commit()

                # Retrieve the ride ID
                mycursor.execute("SELECT LAST_INSERT_ID()")
                ride_id = mycursor.fetchone()[0]

                # Record payment information
                mycursor.execute("""
                    INSERT INTO Payments (UserID, RideID, Amount, PaymentMethod, TransactionID)
                    VALUES (%s, %s, %s, %s, %s)
                """, (current_user_id, ride_id, fare_estimate, payment_mode, f"TXN{random.randint(100000000, 999999999)}"))
                mydb.commit()

                # Display booking summary and feedback form
                summary_window = tk.Toplevel(root)
                summary_window.title("Booking Summary and Feedback")
                summary_window.attributes('-fullscreen', True)  # Full-screen mode

                tk.Label(summary_window, text="Booking Summary", fg="blue", font=('Helvetica', 24, 'bold')).pack(pady=20)

                tk.Label(summary_window, text=f"Ride ID: {ride_id}", font=('Helvetica', 18)).pack()
                tk.Label(summary_window, text=f"Pickup Location: {pickup_location}", font=('Helvetica', 18)).pack()
                tk.Label(summary_window, text=f"Drop-off Location: {dropoff_location}", font=('Helvetica', 18)).pack()
                tk.Label(summary_window, text=f"Vehicle Type: {vehicle_type}", font=('Helvetica', 18)).pack()

                # Fetch driver and vehicle details for display
                mycursor.execute("""
                    SELECT Drivers.DName, Vehicles.RegistrationNumber
                    FROM Drivers JOIN Vehicles ON Drivers.VehicleID = Vehicles.VehicleID
                    WHERE Vehicles.VehicleType = %s AND Drivers.IsActive = 1
                    LIMIT 1
                """, (vehicle_type,))
                driver_details = mycursor.fetchone()
                if driver_details:
                    driver_name, vehicle_registration = driver_details
                    tk.Label(summary_window, text=f"Driver Name: {driver_name}", font=('Helvetica', 18)).pack()
                    tk.Label(summary_window, text=f"Vehicle Registration No: {vehicle_registration}", font=('Helvetica', 18)).pack()

                # Fetch amount paid for the ride
                mycursor.execute("SELECT Amount FROM Payments WHERE RideID = %s", (ride_id,))
                amount_paid = mycursor.fetchone()
                if amount_paid:
                    tk.Label(summary_window, text=f"Amount Paid: {amount_paid[0]}", font=('Helvetica', 18)).pack()

                tk.Label(summary_window, text="Feedback", font=('Helvetica', 24, 'bold')).pack(pady=20)
                tk.Label(summary_window, text="Rate your ride (1-5):", font=('Helvetica', 18)).pack()
                rating_var = tk.IntVar()
                rating_scale = tk.Scale(summary_window, from_=1, to=5, orient=tk.HORIZONTAL, variable=rating_var, font=('Helvetica', 18))
                rating_scale.pack()
                tk.Label(summary_window, text="Comments:", font=('Helvetica', 18)).pack()
                comments_entry = tk.Text(summary_window, height=3, font=('Helvetica', 18))
                comments_entry.pack()

                def submit_feedback():
                    rating = rating_var.get()
                    comments = comments_entry.get("1.0", tk.END).strip()

                    if not rating or rating < 1 or rating > 5:
                        messagebox.showerror("Error", "Please rate your ride between 1 to 5.")
                        return

                    try:
                        mydb, mycursor = connect_to_database()
                        if mydb and mycursor:
                            mycursor.execute("""
                                INSERT INTO Feedback (RideID, UserID, DriverID, Rating, Comments)
                                VALUES (%s, %s, NULL, %s, %s)
                            """, (ride_id, current_user_id, rating, comments))
                            mydb.commit()
                            messagebox.showinfo("Success", "Feedback submitted successfully")
                            summary_window.destroy()

                    except Error as e:
                        messagebox.showerror("Error", f"Error submitting feedback: {e}")

                    finally:
                        if mycursor:
                            mycursor.close()
                        if mydb:
                            mydb.close()

                tk.Button(summary_window, text="Submit Feedback", command=submit_feedback, fg="white", bg="blue", font=('Helvetica', 18)).pack(pady=20)

            except Error as e:
                messagebox.showerror("Error", f"Error booking ride: {e}")

            finally:
                if mycursor:
                    mycursor.close()
                if mydb:
                    mydb.close()

    tk.Button(vehicle_selection_window, text="Confirm Booking", command=confirm_booking, fg="white", bg="blue", font=('Helvetica', 18)).pack(pady=20)

    add_logout_button(vehicle_selection_window)

# Function to open booking page after successful login
def open_booking_page(user_id):
    global current_user_id
    current_user_id = user_id

    booking_window = tk.Toplevel(root)
    booking_window.title("Book a Ride")
    booking_window.attributes('-fullscreen', True)  # Full-screen mode

    tk.Label(booking_window, text="OLA CABS", fg="blue", font=('Helvetica', 30, 'bold')).pack(pady=20)

    tk.Label(booking_window, text="Pickup Location", font=('Helvetica', 18)).pack(pady=10)
    combo_pickup_location = ttk.Combobox(booking_window, font=('Helvetica', 18))
    combo_pickup_location['values'] = load_pickup_locations()
    combo_pickup_location.pack(pady=5)

    tk.Label(booking_window, text="Drop-off Location", font=('Helvetica', 18)).pack(pady=10)
    entry_dropoff_location = tk.Entry(booking_window, font=('Helvetica', 18))
    entry_dropoff_location.pack(pady=5)

    def validate_and_continue():
        pickup_location = combo_pickup_location.get()
        dropoff_location = entry_dropoff_location.get()

        if not pickup_location or not dropoff_location:
            messagebox.showerror("Error", "Please enter both pickup and drop-off locations.")
            return

        continue_to_vehicle_selection(pickup_location, dropoff_location)

    tk.Button(booking_window, text="Continue", command=validate_and_continue, fg="white", bg="blue", font=('Helvetica', 18)).pack(pady=20)

    add_logout_button(booking_window)

# Function to sign out
def sign_out():
    global current_user_id
    current_user_id = None
    messagebox.showinfo("Logged Out", "You have been logged out successfully.")

# Function to add logout and exit buttons after successful login
def add_login_buttons(window):
    exit_button = tk.Button(window, text="Exit", command=root.destroy, fg="white", bg="red", font=('Helvetica', 14))
    exit_button.pack(side=tk.RIGHT, padx=20)

    logout_button = tk.Button(window, text="Logout", command=sign_out, fg="white", bg="blue", font=('Helvetica', 14))
    logout_button.pack(side=tk.RIGHT, padx=20)

# Main window initialization
root = tk.Tk()
root.title("OLA Booking App")
root.attributes('-fullscreen', True)  # Full-screen mode

tk.Label(root, text="Welcome to OLA Cabs", fg="blue", font=('Helvetica', 30, 'bold')).pack(pady=20)

# Sign Up button
tk.Button(root, text="Sign Up", command=sign_up, fg="white", bg="blue", font=('Helvetica', 18)).pack(pady=20)

# Sign In button (example user_id = 1)
tk.Button(root, text="Sign In", command=lambda: sign_in(), fg="white", bg="blue", font=('Helvetica', 18)).pack(pady=20)

# Exit button
tk.Button(root, text="Exit", command=root.destroy, fg="white", bg="red", font=('Helvetica', 18)).pack(pady=20)

# Start the Tkinter main loop
root.mainloop()