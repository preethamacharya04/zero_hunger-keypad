import sqlite3
import random
import time
import os

DB_PATH = 'database.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Phone_Number TEXT,
            Location_Zone TEXT,
            Request_Status TEXT,
            Trust_Score INTEGER
        )
    ''')
    
    # Create Donors Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Donors (
            Donor_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Business_Name TEXT,
            Donor_Type TEXT,
            Base_Location TEXT,
            Hunger_Credits_Balance INTEGER,
            Reliability_Rating REAL
        )
    ''')
    
    # Create Donations Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Donations (
            Donation_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Donor_ID INTEGER,
            Food_Type TEXT,
            Quantity INTEGER,
            Timestamp_Created REAL,
            Expiry_Window_Hours REAL,
            Current_Status TEXT,
            FOREIGN KEY (Donor_ID) REFERENCES Donors (Donor_ID)
        )
    ''')
    
    # Create Transactions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transactions (
            Transaction_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            User_ID INTEGER,
            Donor_ID INTEGER,
            Freshness_Code INTEGER,
            Verification_Status TEXT,
            Sector_Point_ID TEXT,
            FOREIGN KEY (User_ID) REFERENCES Users (User_ID),
            FOREIGN KEY (Donor_ID) REFERENCES Donors (Donor_ID)
        )
    ''')
    
    conn.commit()
    conn.close()

def generate_random_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Insert Random User
    zones = ['North', 'South', 'East', 'West', 'Central']
    statuses = ['Pending', 'Matched', 'Fulfilled', 'Flagged']
    
    phone = f"9876{random.randint(100000, 999999)}"
    zone = random.choice(zones)
    req_status = random.choice(statuses)
    trust_score = random.randint(50, 100)
    
    cursor.execute(
        "INSERT INTO Users (Phone_Number, Location_Zone, Request_Status, Trust_Score) VALUES (?, ?, ?, ?)",
        (phone, zone, req_status, trust_score)
    )
    user_id = cursor.lastrowid
    
    # 2. Insert Random Donor
    business_names = ['Grand Hotel', 'City Cafe', 'Vrrudhashrama', 'Fresh Bakes', 'Community Hub']
    donor_types = ['Restaurant', 'Hotel', 'Individual', 'Hub']
    
    biz_name = random.choice(business_names) + f" {random.randint(1, 99)}"
    d_type = random.choice(donor_types)
    loc = random.choice(zones)
    credits = random.randint(100, 5000)
    rating = round(random.uniform(3.5, 5.0), 1)
    
    cursor.execute(
        "INSERT INTO Donors (Business_Name, Donor_Type, Base_Location, Hunger_Credits_Balance, Reliability_Rating) VALUES (?, ?, ?, ?, ?)",
        (biz_name, d_type, loc, credits, rating)
    )
    donor_id = cursor.lastrowid
    
    # 3. Insert Random Donation
    food_types = ['Grains', 'Cooked Meal', 'Baby Food', 'Vegetables']
    status_don = ['Available', 'Claimed', 'Expired']
    
    food = random.choice(food_types)
    qty = random.randint(10, 100)
    current_time = time.time()
    # Let some donations be older to show expiration logic
    time_created = current_time - random.randint(0, 14400) # up to 4 hours ago
    expiry_hours = random.uniform(2.0, 6.0)
    curr_status = random.choice(status_don)
    
    cursor.execute(
        "INSERT INTO Donations (Donor_ID, Food_Type, Quantity, Timestamp_Created, Expiry_Window_Hours, Current_Status) VALUES (?, ?, ?, ?, ?, ?)",
        (donor_id, food, qty, time_created, expiry_hours, curr_status)
    )
    
    # 4. Insert Random Transaction
    v_status = 'Pending'
    
    fresh_code = random.randint(1000, 9999)
    sector_id = f"SEC-{random.randint(1, 10)}"
    
    cursor.execute(
        "INSERT INTO Transactions (User_ID, Donor_ID, Freshness_Code, Verification_Status, Sector_Point_ID) VALUES (?, ?, ?, ?, ?)",
        (user_id, donor_id, fresh_code, v_status, sector_id)
    )
    
    conn.commit()
    conn.close()

def get_dashboard_data():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    current_time = time.time()
    
    # Update expired donations before fetching
    cursor.execute(f'''
        UPDATE Donations 
        SET Current_Status = 'Expired' 
        WHERE (Expiry_Window_Hours - (({current_time} - Timestamp_Created) / 3600)) < 1 
        AND Current_Status != 'Expired'
    ''')
    conn.commit()
    
    # Fetch Users
    cursor.execute("SELECT * FROM Users ORDER BY User_ID DESC LIMIT 20")
    users = [dict(row) for row in cursor.fetchall()]
    
    # Fetch Donors
    cursor.execute("SELECT * FROM Donors ORDER BY Donor_ID DESC LIMIT 20")
    donors = [dict(row) for row in cursor.fetchall()]
    
    # Fetch Donations with calculated Time Remaining
    cursor.execute(f'''
        SELECT d.*, dn.Business_Name,
        ROUND(d.Expiry_Window_Hours - (({current_time} - d.Timestamp_Created) / 3600), 2) as Time_Remaining
        FROM Donations d
        JOIN Donors dn ON d.Donor_ID = dn.Donor_ID
        ORDER BY d.Donation_ID DESC LIMIT 20
    ''')
    donations = [dict(row) for row in cursor.fetchall()]
    
    # Fetch Transactions
    cursor.execute('''
        SELECT t.*, u.Phone_Number, d.Business_Name 
        FROM Transactions t
        JOIN Users u ON t.User_ID = u.User_ID
        JOIN Donors d ON t.Donor_ID = d.Donor_ID
        ORDER BY t.Transaction_ID DESC LIMIT 20
    ''')
    transactions = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return {
        'users': users,
        'donors': donors,
        'donations': donations,
        'transactions': transactions
    }

def verify_vrrudhashrama_transactions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # First, let's artificially set one random transaction to "Rejected - Spoiled" 
    # to maintain the visual showcase requirement of the UI, but ONLY if none exist.
    cursor.execute("SELECT COUNT(*) FROM Transactions WHERE Verification_Status = 'Rejected - Spoiled'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            UPDATE Transactions 
            SET Verification_Status = 'Rejected - Spoiled' 
            WHERE Transaction_ID = (SELECT Transaction_ID FROM Transactions ORDER BY RANDOM() LIMIT 1)
        ''')
    
    # Mark all Pending Vrrudhashrama transactions as Verified!
    cursor.execute('''
        UPDATE Transactions
        SET Verification_Status = 'Verified'
        WHERE Donor_ID IN (
            SELECT Donor_ID FROM Donors WHERE Business_Name LIKE '%Vrrudhashrama%'
        ) AND Verification_Status = 'Pending'
    ''')
    
    conn.commit()
    conn.close()
