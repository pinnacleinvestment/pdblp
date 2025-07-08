import sqlite3

def main():
    # Path to your SQLite database file
    db_path = 'sample.db'  # Change this to your actual database path

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create requestlog table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requestlog (
            id INTEGER PRIMARY KEY,
            timestamp TIMESTAMP,
            request_type TEXT
        )
    ''')

    # Print all table names
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    print('Tables:', tables)

    # If blpapilog exists, rename it to blpapilog_old
    if ('blpapilog',) in tables:
        cursor.execute('ALTER TABLE blpapilog RENAME TO blpapilog_old')
        conn.commit()
        print('Renamed blpapilog to blpapilog_old')

    # Create new normalized blpapilog table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blpapilog (
            id INTEGER PRIMARY KEY,
            request_id INTEGER,
            ticker TEXT,
            field TEXT,
            FOREIGN KEY(request_id) REFERENCES requestlog(id)
        )
    ''')
    conn.commit()

    # Migrate data from blpapilog_old if it exists
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    if ('blpapilog_old',) in tables:
        rows = cursor.execute('SELECT id, timestamp, request_type, tickers, fields FROM blpapilog_old').fetchall()
        for row in rows:
            request_id = row[0]
            timestamp = row[1]
            request_type = row[2]
            tickers = [t.strip() for t in row[3].split(',') if t.strip()]
            fields = [f.strip() for f in row[4].split(',') if f.strip()]
            # Insert into requestlog (ignore if already present)
            cursor.execute('''
                INSERT OR IGNORE INTO requestlog (id, timestamp, request_type) VALUES (?, ?, ?)
            ''', (request_id, timestamp, request_type))
            for ticker in tickers:
                for field in fields:
                    cursor.execute('''
                        INSERT INTO blpapilog (request_id, ticker, field) VALUES (?, ?, ?)
                    ''', (request_id, ticker, field))
        conn.commit()
        print('Migrated data to new blpapilog table.')
    else:
        print('No blpapilog_old table to migrate.')

    # Close connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
