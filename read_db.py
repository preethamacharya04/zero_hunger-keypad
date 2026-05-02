import sqlite3
import json

db_path = "storage/god_mode.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def get_data():
    tables = ["users", "reports", "market_prices"]
    data = {}
    for table in tables:
        try:
            cursor.execute(f"SELECT * FROM {table}")
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            data[table] = [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            data[table] = str(e)
    return data

if __name__ == "__main__":
    print(json.dumps(get_data(), indent=2))
conn.close()
