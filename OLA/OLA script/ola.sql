CREATE TABLE Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    UName TEXT NOT NULL,
    Address TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    PhoneNumber TEXT UNIQUE NOT NULL,
    PasswordHash TEXT NOT NULL
);

CREATE TABLE Vehicles (
    VehicleID INTEGER PRIMARY KEY AUTOINCREMENT,
    VehicleType TEXT NOT NULL,
    RegistrationNumber TEXT UNIQUE NOT NULL,
    Model TEXT NOT NULL,
    Manufacturer TEXT NOT NULL,
    YearOfManufacture INTEGER,
    Capacity INTEGER
);

CREATE TABLE Drivers (
    DriverID INTEGER PRIMARY KEY AUTOINCREMENT,
    DName TEXT NOT NULL,
    Email TEXT UNIQUE,
    Address TEXT NOT NULL,
    PhoneNumber TEXT UNIQUE NOT NULL,
    LicenseNumber TEXT UNIQUE NOT NULL,
    VehicleID INTEGER,
    IsActive INTEGER DEFAULT 1,
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(VehicleID)
);

CREATE TABLE Rides (
    RideID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER,
    DriverID INTEGER,
    VehicleID INTEGER,
    PickupLocation TEXT NOT NULL,
    DropoffLocation TEXT NOT NULL,
    PickupTime TIMESTAMP,
    DropoffTime TIMESTAMP,
    Fare NUMERIC(10, 2),
    Status TEXT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (DriverID) REFERENCES Drivers(DriverID),
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(VehicleID)
);

CREATE TABLE Payments (
    PaymentID INTEGER PRIMARY KEY AUTOINCREMENT,
    RideID INTEGER,
    UserID INTEGER,
    Amount NUMERIC(10, 2) NOT NULL,
    PaymentMethod TEXT NOT NULL,
    TransactionID TEXT UNIQUE,
    FOREIGN KEY (RideID) REFERENCES Rides(RideID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE Feedback (
    FeedbackID INTEGER PRIMARY KEY AUTOINCREMENT,
    RideID INTEGER,
    UserID INTEGER,
    DriverID INTEGER,
    Rating INTEGER CHECK (Rating >= 1 AND Rating <= 5),
    Comments TEXT,
    FOREIGN KEY (RideID) REFERENCES Rides(RideID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (DriverID) REFERENCES Drivers(DriverID)
);
INSERT INTO Users (UName, Address, Email, PhoneNumber, PasswordHash) VALUES
('John Doe', 'Kochi, Kerala', 'john.doe@example.com', '+91 9876543210', 'hashed_password'),
('Jane Smith', 'Trivandrum, Kerala', 'jane.smith@example.com', '+91 8765432109', 'hashed_password'),
('David Thomas', 'Kozhikode, Kerala', 'david.thomas@example.com', '+91 7654321098', 'hashed_password'),
('Anna Jacob', 'Alappuzha, Kerala', 'anna.jacob@example.com', '+91 6543210987', 'hashed_password'),
('Michael George', 'Thrissur, Kerala', 'michael.george@example.com', '+91 5432109876', 'hashed_password');

INSERT INTO Vehicles (VehicleType, RegistrationNumber, Model, Manufacturer, YearOfManufacture, Capacity) VALUES
('Sedan', 'KL-01 AB 1234', 'Honda City', 'Honda', 2020, 5),
('SUV', 'KL-02 CD 5678', 'Toyota Fortuner', 'Toyota', 2019, 7),
('Hatchback', 'KL-03 EF 9012', 'Hyundai i20', 'Hyundai', 2021, 5),
('Scooter', 'KL-04 GH 3456', 'Honda Activa', 'Honda', 2020, 2),
('Luxury Sedan', 'KL-05 IJ 7890', 'Mercedes-Benz E-Class', 'Mercedes-Benz', 2022, 5);

INSERT INTO Drivers (DName, Email, Address, PhoneNumber, LicenseNumber, VehicleID) VALUES
('Thomas Mathew', 'thomas.mathew@example.com', 'Kochi, Kerala', '+91 9876543211', 'DL-202345', 1),
('Sara Joseph', 'sara.joseph@example.com', 'Trivandrum, Kerala', '+91 8765432108', 'DL-202346', 2),
('Rajesh Kumar', 'rajesh.kumar@example.com', 'Kozhikode, Kerala', '+91 7654321097', 'DL-202347', 3),
('Priya Nair', 'priya.nair@example.com', 'Alappuzha, Kerala', '+91 6543210986', 'DL-202348', 4),
('Arun Singh', 'arun.singh@example.com', 'Thrissur, Kerala', '+91 5432109875', 'DL-202349', 5);

INSERT INTO Rides (UserID, DriverID, VehicleID, PickupLocation, DropoffLocation, PickupTime, DropoffTime, Fare, Status) VALUES
(1, 1, 1, 'Ernakulam Junction', 'Fort Kochi', '2024-06-15 10:00:00', '2024-06-15 10:30:00', 250.00, 'Completed'),
(2, 2, 2, 'Trivandrum Central', 'Kovalam Beach', '2024-06-15 11:00:00', '2024-06-15 11:30:00', 500.00, 'Completed'),
(3, 3, 3, 'Kozhikode Railway Station', 'Beypore Beach', '2024-06-15 12:00:00', '2024-06-15 12:45:00', 300.00, 'Completed'),
(4, 4, 4, 'Alappuzha Boat Jetty', 'Marari Beach', '2024-06-15 13:00:00', '2024-06-15 13:30:00', 150.00, 'Completed'),
(5, 5, 5, 'Thrissur Railway Station', 'Guruvayoor Temple', '2024-06-15 14:00:00', '2024-06-15 14:45:00', 200.00, 'Completed');

INSERT INTO Payments (RideID, UserID, Amount, PaymentMethod, TransactionID) VALUES
(1, 1, 250.00, 'Credit Card', 'TXN123456789'),
(2, 2, 500.00, 'PayPal', 'TXN987654321'),
(3, 3, 300.00, 'Cash',  'TXN567890123'),
(4, 4, 150.00, 'Debit Card', 'TXN345678901'),
(5, 5, 200.00, 'UPI', 'TXN789012345');

INSERT INTO Feedback (RideID, UserID, DriverID, Rating, Comments) VALUES
(1, 1, 1, 4, 'Smooth ride, polite driver.'),
(2, 2, 2, 5, 'Excellent service, comfortable vehicle.'),
(3, 3, 3, 3, 'Driver arrived late, but ride was fine.'),
(4, 4, 4, 4, 'Good experience overall.'),
(5, 5, 5, 5, 'Highly recommended! Great service.');
