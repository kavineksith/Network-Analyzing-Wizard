import sqlite3
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create file handler for logging to a file
file_handler = logging.FileHandler('network_analysis.log')
file_handler.setLevel(logging.DEBUG)  # Write all logs (DEBUG and higher) to the file

# Create a stream handler for the terminal (set to WARNING or higher to suppress DEBUG and INFO)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.WARNING)  # Only show WARNING, ERROR, and CRITICAL messages on terminal

# Create a formatter and attach it to both handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Set the logger's level to DEBUG to capture all log levels
logger.setLevel(logging.DEBUG)

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
