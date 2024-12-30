import sqlite3
import logging

# Configure the logger
logging.basicConfig(level=logging.DEBUG,  # Log all levels (DEBUG and above)
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

# Create a logger
logger = logging.getLogger(__name__)

class Database:
    """Class to handle database operations related to request limits."""

    def __init__(self, db_name='request_limit.db'):
        self.db_name = db_name
        logger.debug(f"Initialized Database with name: {self.db_name}")

    def _connect(self):
        """Establish and return a connection to the SQLite database."""
        try:
            conn = sqlite3.connect(self.db_name)
            logger.info(f"Successfully connected to database: {self.db_name}")
            return conn
        except sqlite3.DatabaseError as e:
            logger.error(f"Database connection failed: {e}")
            raise

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
            logger.info("Database and table created successfully.")
        except sqlite3.DatabaseError as e:
            logger.error(f"Database error: {e}")
        finally:
            if conn:
                conn.close()
                logger.debug("Database connection closed.")

# Example usage
if __name__ == "__main__":
    db = Database()  # Create an instance of the Database class
    db.create_db()    # Create the database and table
