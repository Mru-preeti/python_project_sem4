import sqlite3

with sqlite3.connect('Login_data.db') as conn:
    cursor = conn.cursor()

    # Create USERS table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS USERS (
            username TEXT NOT NULL,
            email_id TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)

    # Insert a user (ignore if exists)
    cursor.execute("""
        INSERT OR IGNORE INTO USERS (username, email_id, password)
        VALUES ('tester', 'tester@gmail.com', 'test')
    """)

    # Create results table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            quiz_type TEXT,
            questions TEXT,
            user_answers TEXT,
            score INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            Correctanswer TEXT
        )
    """)

  
