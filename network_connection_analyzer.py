#!/usr/bin/env python3

import json
import psutil
import netifaces
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,  # Log all levels (DEBUG and above)
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

# Create a logger
logger = logging.getLogger(__name__)

class NetworkManager:
    def __init__(self):
        self.data = {
            "interface_stats": {},
            "interface_addrs": {},
            "connections": {}
        }

    def gather_interface_stats(self):
        """Gathers network interface statistics."""
        try:
            logger.info("Gathering network interface statistics...")
            stats = psutil.net_if_stats()
            for iface, info in stats.items():
                self.data["interface_stats"][iface] = {
                    "isup": info.isup,
                    "duplex": self._get_duplex_name(info.duplex),
                    "speed": info.speed,
                    "mtu": info.mtu,
                    "flags": info.flags
                }
            logger.info("Network interface statistics gathered successfully.")
        except Exception as e:
            logger.error(f"Error gathering interface stats: {e}")
            return {"error": f"Error gathering interface stats: {e}"}

    def gather_interface_addrs(self):
        """Gathers network interface addresses."""
        try:
            logger.info("Gathering network interface addresses...")
            addrs = psutil.net_if_addrs()
            for iface, info_list in addrs.items():
                self.data["interface_addrs"][iface] = []
                for info in info_list:
                    self.data["interface_addrs"][iface].append({
                        "family": self._get_family_name(info.family),
                        "address": info.address,
                        "netmask": info.netmask,
                        "broadcast": info.broadcast,
                        "ptp": info.ptp
                    })
            logger.info("Network interface addresses gathered successfully.")
        except Exception as e:
            logger.error(f"Error gathering interface addresses: {e}")
            return {"error": f"Error gathering interface addresses: {e}"}

    def gather_connections(self, kind: str):
        """Gathers network connections of a specific kind."""
        try:
            logger.info(f"Gathering network connections of type: {kind}...")
            connections = psutil.net_connections(kind=kind)
            self.data["connections"][kind] = []
            for conn in connections:
                self.data["connections"][kind].append({
                    "fd": conn.fd,
                    "family": self._get_family_name(conn.family),
                    "type": self._get_socket_type_name(conn.type),
                    "local_address": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "None",
                    "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "None",
                    "status": conn.status,
                    "pid": conn.pid if conn.pid is not None else 'None'
                })
            logger.info(f"Network connections of type {kind} gathered successfully.")
        except Exception as e:
            logger.error(f"Error gathering connections for kind='{kind}': {e}")
            return {"error": f"Error gathering connections for kind='{kind}': {e}"}

    def gather_all_info(self):
        """Gathers all network-related information."""
        logger.info("Gathering all network-related information...")
        self.gather_interface_stats()
        self.gather_interface_addrs()
        kinds = [
            "inet",  # IPv4 and IPv6
            "inet4", # IPv4
            "inet6", # IPv6
            "tcp",   # TCP
            "tcp4",  # TCP over IPv4
            "tcp6",  # TCP over IPv6
            "udp",   # UDP
            "udp4",  # UDP over IPv4
            "udp6",  # UDP over IPv6
        ]
        for kind in kinds:
            self.gather_connections(kind)
        logger.info("All network-related information gathered successfully.")
        return self.data

    def _get_duplex_name(self, duplex):
        """Safely get the name of the duplex type."""
        try:
            return duplex.name
        except AttributeError:
            return str(duplex)

    def _get_family_name(self, family):
        """Safely get the name of the address family."""
        try:
            return family.name
        except AttributeError:
            return str(family)

    def _get_socket_type_name(self, socket_type):
        """Safely get the name of the socket type."""
        try:
            return socket_type.name
        except AttributeError:
            return str(socket_type)

    @staticmethod
    def get_network_info():
        """Gathers detailed network interface information.

        Returns:
            A dictionary containing network interface information.
        """
        # Mapping of address family integers to human-readable names
        addr_family_map = {
            netifaces.AF_INET: 'IPv4',
            netifaces.AF_INET6: 'IPv6',
            netifaces.AF_LINK: 'MAC'
        }

        network_info = {}

        try:
            logger.info("Gathering detailed network interface information...")
            interfaces = netifaces.interfaces()
            gateways = netifaces.gateways()  # Get the gateways information

            for interface in interfaces:
                addrs = netifaces.ifaddresses(interface)
                interface_info = {
                    'interface_name': interface,  # More meaningful key
                    'mac_address': None,  # Initialize MAC address as None
                    'default_gateway': None,  # Initialize gateway address as None
                    'ip_addresses': []  # Initialize a list to hold address info
                }
                
                # Get the MAC address if available
                if netifaces.AF_LINK in addrs:
                    mac_info = addrs[netifaces.AF_LINK][0]  # Get the first entry for the MAC address
                    interface_info['mac_address'] = mac_info.get('addr')  # Store the MAC address

                # Get the gateway address for the interface if available
                if 'default' in gateways:
                    for key, value in gateways['default'].items(): # type: ignore
                        if value[1] == interface:  # Check if the interface matches
                            interface_info['default_gateway'] = value[0]  # Get the gateway address
                            break  # Exit the loop once the gateway is found

                # Replace None with "None" for gateway
                if interface_info['default_gateway'] is None:
                    interface_info['default_gateway'] = "None"

                for addr_family, addr_info in addrs.items():
                    for addr in addr_info:
                        # Translate addr_family to human-readable version
                        family_name = addr_family_map.get(addr_family, 'Unknown')
                        address_details = {
                            'address_family': family_name,  # More meaningful key
                            'ip_address': addr.get('addr') if addr.get('addr') is not None else "None",  # Replace None with "None"
                            'subnet_mask': addr.get('netmask') if addr.get('netmask') is not None else "None",  # Replace None with "None"
                            'broadcast_address': addr.get('broadcast') if addr.get('broadcast') is not None else "None",  # Replace None with "None"
                            'peer_address': addr.get('peer') if addr.get('peer') is not None else "None"  # Replace None with "None"
                        }
                        interface_info['ip_addresses'].append(address_details)  # Append address details to the list
                
                network_info[interface] = interface_info

            logger.info("Detailed network interface information gathered successfully.")
            return network_info

        except Exception as e:
            logger.error(f"Error getting network information: {str(e)}")
            return {"error": f"Error getting network information: {str(e)}"}

    @staticmethod
    # Function to manage network statistics
    def network_report():
        try:
            logger.info("Generating network report...")
            # Network Usage Statistics
            deep_analyzed_report = json.dumps(NetworkManager().gather_all_info(), indent=4)
            network_interface_report = json.dumps(NetworkManager().get_network_info(), indent=4)

            # Combine the dictionaries instead of using update on JSON string
            combined_report = dict(json.loads(deep_analyzed_report), **json.loads(network_interface_report))

            result = json.dumps(combined_report, indent=4)
            json_output = json.loads(result)
            logger.info("Network report generated successfully.")
            return json_output  # Return the JSON output as a string
        except Exception as e:
            logger.error(f"Error generating network report: {e}")
            return {"error": f"Error: {e}"}
