import sqlite3
from datetime import datetime

class VoiceLedger:
    def __init__(self, db_path="storage/god_mode.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Creates the necessary tables for Garuda Sanket."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User Table: Stores info about the farmer
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            phone_number TEXT PRIMARY KEY,
                            name TEXT,
                            village TEXT,
                            crops TEXT,
                            trust_score INTEGER DEFAULT 100
                          )''')

        # Reports Table: For the 'Collective Intelligence' (Pests/Diseases)
        cursor.execute('''CREATE TABLE IF NOT EXISTS reports (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            phone_number TEXT,
                            village TEXT,
                            issue_type TEXT,
                            timestamp DATETIME
                          )''')

        # Market Table: For the 'Market King' Negotiator logic
        cursor.execute('''CREATE TABLE IF NOT EXISTS market_prices (
                            crop_name TEXT PRIMARY KEY,
                            best_price REAL,
                            location TEXT,
                            last_updated DATETIME
                          )''')

        conn.commit()
        conn.close()

    def add_user(self, phone, name, village, crops):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, 100)", 
                       (phone, name, village, crops))
        conn.commit()
        conn.close()

    def report_issue(self, phone, village, issue):
        """Logs a problem for outbreak detection."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reports (phone_number, village, issue_type, timestamp) VALUES (?, ?, ?, ?)",
                       (phone, village, issue, datetime.now()))
        conn.commit()
        conn.close()

    def check_outbreak(self, village, issue, limit=5):
        """Checks if multiple farmers in the same village reported the same issue."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Look for reports of the same issue in the same village in the last 48 hours
        cursor.execute('''SELECT COUNT(*) FROM reports 
                          WHERE village = ? AND issue_type = ? 
                          AND timestamp > datetime('now', '-2 days')''', (village, issue))
        count = cursor.fetchone()[0]
        conn.close()
        return count >= limit