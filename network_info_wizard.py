#!/usr/bin/env python3

import json
import psutil
import socket
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

class NetworkInformation:
    @staticmethod
    # Function to check localhost connectivity
    def check_localhost_connectivity():
        try:
            logger.info("Checking localhost connectivity...")
            socket.gethostbyname('127.0.0.1')
            status = "PC is connected to localhost."
            logger.info("PC is connected to localhost.")
        except socket.gaierror:
            status = "PC isn't connected to localhost."
            logger.error("PC isn't connected to localhost.")
        finally:
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).close()

        return status

    @staticmethod
    # Function to check network connectivity
    def check_network_connectivity():
        try:
            logger.info("Checking network connectivity...")
            socket.gethostbyname('www.google.com')
            status = "PC is connected to the internet."
            logger.info("PC is connected to the internet.")
        except socket.gaierror:
            status = "PC isn't connected to the internet."
            logger.error("PC isn't connected to the internet.")
        finally:
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).close()

        return status

    @staticmethod
    # Function to monitor network traffic
    def monitor_network_traffic():
        try:
            logger.info("Monitoring network traffic...")
            network = psutil.net_io_counters()
            traffic_info = {
                'Network Traffic Information': {
                    'Send': f'{network.bytes_sent / (1024 ** 2):.2f} Mbps',
                    'Received': f'{network.bytes_recv / (1024 ** 2):.2f} Mbps',
                },
                'Extra Information': {
                    'Packets Sent': f'{network.packets_sent}',
                    'Packet Received': f'{network.packets_recv}',
                    'ErrorIn': f'{network.errin}',
                    'ErrorOut': f'{network.errout}',
                    'DropIn': f'{network.dropin}',
                    'DropOut': f'{network.dropout}'
                }
            }
            logger.info("Network traffic monitored successfully.")
            return traffic_info
        except Exception as e:
            logger.error(f"Network Traffic Monitoring Error: {e}")
            return {"error": f"Network Traffic Monitoring Error: {e}"}

    @staticmethod
    # Function to manage network statistics
    def network_report():
        try:
            logger.info("Generating network report...")
            localhost_connectivity = NetworkInformation().check_localhost_connectivity()
            network_connectivity = NetworkInformation().check_network_connectivity()
            network_traffic = NetworkInformation().monitor_network_traffic()

            statistics = {
                'Network Usage Statistics': {
                    'Localhost Connectivity': localhost_connectivity,
                    'Network Connectivity': network_connectivity,
                    'Network Traffic': network_traffic,
                }
            }

            result = json.dumps(statistics, indent=4)
            logger.info("Network report generated successfully.")
            return result
        except Exception as e:
            logger.error(f"Network Traffic Monitoring Report Generating Error: {e}")
            return {"error": f"Network Traffic Monitoring Report Generating Error: {e}"}
