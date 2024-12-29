# Network Analyzing Wizard Documentation

## Overview

This Python script provided offer a comprehensive framework for monitoring and managing network-related information on a system. They utilize the powerful `psutil` and `netifaces` libraries to gather detailed statistics about network interfaces, active connections, and real-time network traffic. The `NetworkManager` class focuses on collecting and structuring data about interface statistics (such as speed, status, and MTU), IP addresses, and connection types (TCP, UDP), while the `NetworkInformation` class checks system connectivity (to localhost and external services like Google) and monitors network traffic (bytes sent/received, packet stats). The scripts generate structured JSON reports, making it easy to integrate this network data into applications or use it for diagnostics. Designed with error handling for robustness, these scripts provide a reliable toolset for network administrators and IT professionals to monitor, troubleshoot, and analyze network performance and health in real-time.


## Features

- **Localhost Connectivity Check**: Determines if the host machine is connected to localhost.
- **Internet Connectivity Check**: Assesses whether the machine has internet access by trying to resolve a well-known domain.
- **Network Traffic Monitoring**: Monitors and reports network traffic metrics such as data sent and received, as well as packet statistics.
- **Interface Statistics Collection**: Retrieves and reports statistics for each network interface, including status, duplex mode, speed, MTU (Maximum Transmission Unit), and flags.
- **Interface Addresses Collection**: Gathers and reports IP addresses and related information (such as netmask, broadcast address) for each network interface.
- **Network Connections Analysis**: Collects and reports details of active network connections categorized by connection type, such as TCP and UDP. Supports multiple address families and socket types.
- **Comprehensive Data Gathering**: Aggregates all network-related information into a single structured dataset.
- **Network Report Generation**: Compiles all collected network data into a structured JSON report. Converts the gathered data into a well-formatted JSON string for easy readability and usage.

## Dependencies

- **Python 3.x**: The script requires Python 3.x for execution.
- **psutil**: A cross-platform library used to retrieve network traffic statistics.
- **json**: A built-in Python library for handling JSON data.
- **socket**: A built-in Python library used for network connectivity checks.
- **netifaces**: library for network interface information and IP address retrieval

## Conclusion
This Python script offer a robust solution for comprehensive network monitoring and management, utilizing `psutil` and `netifaces` to gather detailed information about network interfaces, connections, and real-time traffic. The `NetworkManager` class collects data on interface statistics, IP addresses, MAC addresses, and network connections, while the `NetworkInformation` class checks system connectivity (both localhost and internet) and tracks network traffic. Both scripts return structured JSON reports, making it easy to integrate and analyze the data. With built-in error handling, the scripts ensure reliability even when network components are unavailable. These functionalities are valuable for network administrators and system diagnostics, providing crucial insights into network health and performance.

*Tailor every script to meet specific user requirements, allowing for easy upgrades and customization to suit individual needs.*

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### **Disclaimer:**
Kindly note that this project is developed solely for educational purposes, not intended for industrial use, as its sole intention lies within the realm of education. We emphatically underscore that this endeavor is not sanctioned for industrial application. It is imperative to bear in mind that any utilization of this project for commercial endeavors falls outside the intended scope and responsibility of its creators. Thus, we explicitly disclaim any liability or accountability for such usage.