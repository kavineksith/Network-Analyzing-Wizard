#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import time
import sqlite3
from network_info_wizard import NetworkInformation
from network_connection_analyzer import NetworkManager
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')

class Database:
    """Class responsible for interacting with the SQLite database for request limits."""

    def __init__(self, db_name='request_limit.db'):
        self.db_name = db_name

    def get_connection(self):
        """Establish and return a connection to the SQLite database."""
        try:
            return sqlite3.connect(self.db_name)
        except sqlite3.DatabaseError as e:
            raise Exception(f"Database connection error: {e}")

    def check_request_limit(self, ip, limit=5, window=60):
        """Check if the IP has exceeded the request limit within the given window."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            current_time = int(time.time())
            cursor.execute('SELECT request_count, last_request_time FROM request_limits WHERE ip_address = ?', (ip,))
            row = cursor.fetchone()

            if row:
                request_count, last_request_time = row
                # Reset counter if the time window has passed
                if current_time - last_request_time > window:
                    request_count = 0
                    last_request_time = current_time

                if request_count >= limit:
                    conn.close()
                    return False
                else:
                    # Increment the request count and update the timestamp
                    cursor.execute('UPDATE request_limits SET request_count = ?, last_request_time = ? WHERE ip_address = ?',
                                   (request_count + 1, current_time, ip))
            else:
                # Create a new entry for this IP if it does not exist
                cursor.execute('INSERT INTO request_limits (ip_address, request_count, last_request_time) VALUES (?, ?, ?)',
                               (ip, 1, current_time))

            conn.commit()
            conn.close()
            return True

        except sqlite3.DatabaseError as e:
            raise Exception(f"Database error during request limit check: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")


class RateLimiter:
    """Class responsible for handling rate-limiting logic using the Database class."""

    def __init__(self, database, limit=5, window=60):
        self.database = database
        self.limit = limit
        self.window = window

    def check_and_update(self, ip):
        """Check if the IP has exceeded the request limit and update the database."""
        try:
            return self.database.check_request_limit(ip, self.limit, self.window)
        except Exception as e:
            raise Exception(f"Error checking or updating rate limit: {e}")


class ReportGenerator:
    """Class responsible for generating reports."""

    @staticmethod
    def get_report(report_type):
        """Generate a report based on the report type."""
        try:
            if report_type == 'basic_report':
                statistics = NetworkInformation().network_report()
                if statistics is None:
                    return None, 'Failed to generate network report.'
                return statistics, None

            elif report_type == 'advanced_report':
                statistics = NetworkManager().network_report()
                if statistics is None:
                    return None, 'Failed to generate network report.'
                return statistics, None

            else:
                return None, 'Invalid report type. Please choose "basic_report" or "advanced_report".'

        except Exception as e:
            raise Exception(f"Error generating report: {e}")


class App:
    """Class responsible for setting up the Flask app and routes."""

    def __init__(self):
        self.app = Flask(__name__)
        self.database = Database()
        self.rate_limiter = RateLimiter(self.database)
        self.report_generator = ReportGenerator()
        self.configure_app()

    def configure_app(self):
        """Configure the Flask app, set up CORS and routes."""
        CORS(self.app, resources={r"/api/*": {"origins": ["http://127.0.0.1"]}}) # Please add the appropriate origin
        self.app.add_url_rule('/report', view_func=self.get_report, methods=['GET'])
        limiter = Limiter(get_remote_address, app=self.app)
        limiter.init_app(self.app)

    def get_report(self):
        """Endpoint to handle the report generation."""
        ip = request.remote_addr  # Get the client's IP address
        
        # Check if the IP has exceeded the rate limit
        try:
            if not self.rate_limiter.check_and_update(ip):
                return jsonify({'error': 'Request limit exceeded. Please try again later.'}), 429

            report_type = request.args.get('type', default='single_report', type=str)

            statistics, error = self.report_generator.get_report(report_type)
            if error:
                return jsonify({'error': error}), 400

            return jsonify(statistics), 200

        except Exception as e:
            # Log the error
            logging.error(f"Error in get_report: {e}")
            return jsonify({'error': 'Internal server error. Please try again later.'}), 500

    def run(self):
        """Run the Flask app."""
        try:
            self.app.run(host='0.0.0.0', port=5000, debug=True)
        except Exception as e:
            # Log the error (not shown here, but would be logged in a real application)
            print(f"Error running the app: {e}")


if __name__ == "__main__":
    app = App()
    app.run()
