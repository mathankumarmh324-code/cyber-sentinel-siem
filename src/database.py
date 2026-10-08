import sqlite3

def init_db(db_path="alerts.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            source_ip TEXT,
            classification TEXT,
            risk_score INTEGER,
            evidence TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_alert(source_ip, classification, risk_score, evidence, db_path="alerts.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO alerts (source_ip, classification, risk_score, evidence)
        VALUES (?, ?, ?, ?)
    ''', (source_ip, classification, risk_score, evidence))
    conn.commit()
    conn.close()