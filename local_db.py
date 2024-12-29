import sqlite3

class Database:
    """Class to handle database operations related to request limits."""

    def __init__(self, db_name='request_limit.db'):
        self.db_name = db_name

    def _connect(self):
        """Establish and return a connection to the SQLite database."""
        return sqlite3.connect(self.db_name)

    def create_db(self):
        """Create the request_limits table if it doesn't already exist."""
        conn = None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS request_limits (
                    ip_address TEXT PRIMARY KEY,
                    request_count INTEGER,
                    last_request_time INTEGER
                )
            ''')
            conn.commit()
            print("Database and table created successfully.")
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
            if conn:
                conn.close()

# Example usage
if __name__ == "__main__":
    db = Database()  # Create an instance of the Database class
    db.create_db()    # Create the database and table
