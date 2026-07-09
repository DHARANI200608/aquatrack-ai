import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = 'waterborne_ews.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            role TEXT,
            prediction TEXT,
            confidence REAL,
            aluminium REAL, ammonia REAL, arsenic REAL,
            barium REAL, cadmium REAL, chloramine REAL,
            chromium REAL, copper REAL, flouride REAL,
            bacteria REAL, viruses REAL, lead REAL,
            nitrates REAL, nitrites REAL, mercury REAL,
            perchlorate REAL, radium REAL, selenium REAL,
            silver REAL, uranium REAL,
            timestamp TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            role TEXT,
            alert_level TEXT,
            alert_message TEXT,
            bacteria REAL, viruses REAL, lead REAL,
            arsenic REAL, uranium REAL,
            nitrates REAL, cadmium REAL,
            timestamp TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            role TEXT,
            login_time TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print('Database initialized!')

def save_prediction(username, role, prediction, confidence,
                    aluminium, ammonia, arsenic, barium, cadmium,
                    chloramine, chromium, copper, flouride, bacteria,
                    viruses, lead, nitrates, nitrites, mercury,
                    perchlorate, radium, selenium, silver, uranium):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO predictions
        (username, role, prediction, confidence,
         aluminium, ammonia, arsenic, barium, cadmium,
         chloramine, chromium, copper, flouride, bacteria,
         viruses, lead, nitrates, nitrites, mercury,
         perchlorate, radium, selenium, silver, uranium, timestamp)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
        (username, role, prediction, confidence,
         aluminium, ammonia, arsenic, barium, cadmium,
         chloramine, chromium, copper, flouride, bacteria,
         viruses, lead, nitrates, nitrites, mercury,
         perchlorate, radium, selenium, silver, uranium,
         datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def save_alert(username, role, alert_level, alert_message,
               bacteria, viruses, lead, arsenic, uranium, nitrates, cadmium):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO alerts
        (username, role, alert_level, alert_message,
         bacteria, viruses, lead, arsenic, uranium,
         nitrates, cadmium, timestamp)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
        (username, role, alert_level, alert_message,
         bacteria, viruses, lead, arsenic, uranium,
         nitrates, cadmium,
         datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def save_login(username, role):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO logins (username, role, login_time)
                 VALUES (?,?,?)''',
              (username, role,
               datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def get_predictions():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        'SELECT * FROM predictions ORDER BY timestamp DESC LIMIT 50', conn)
    conn.close()
    return df

def get_alerts():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        'SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 50', conn)
    conn.close()
    return df

def get_logins():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        'SELECT * FROM logins ORDER BY login_time DESC LIMIT 20', conn)
    conn.close()
    return df

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM predictions')
    total_predictions = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM predictions WHERE prediction='UNSAFE'")
    unsafe_count = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM alerts')
    total_alerts = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM logins')
    total_logins = c.fetchone()[0]
    conn.close()
    return total_predictions, unsafe_count, total_alerts, total_logins

if __name__ == '__main__':
    init_db()
    print('Tables created successfully!')