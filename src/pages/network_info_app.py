import streamlit as st
import ipaddress
import time
from typing import Union

# Define a type alias for network objects
Network = Union[ipaddress.IPv4Network, ipaddress.IPv6Network]

def get_valid_input(prompt: str) -> Network:
    # while True:
    try:
        network = st.text_input(prompt)
        if not network:
            st.warning("Please enter a network address.")
        # continue
        netobj = ipaddress.ip_network(network, strict=False)
        return netobj
    except ValueError as e:
        st.error(f"Invalid input: {e}. Please enter a valid network address.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


def is_private(address):
    for block in [ipaddress.IPv4Network('10.0.0.0/8'),
                  ipaddress.IPv4Network('172.16.0.0/12'),
                  ipaddress.IPv4Network('192.168.0.0/16')]:
        if address in block:
            return True
    return False

def is_global(network: Network) -> bool:
    """Determine whether the network is global (not private)"""
    for ip in network:
        if is_private(ip):
            return False
    return True

def print_hosts(network):
    host_list = list(network.hosts())
    for host_index, ip in enumerate(host_list, start=1):
        st.write(f"{ip} ({host_index})")

def print_network_details(network):
    """Print network details and hosts."""
    st.write(f"\nNetwork Address: {network.network_address}")
    st.write(f"Number of valid hosts: {network.num_addresses - 2}")
    st.write(f"Network Size: {network.num_addresses}")
    st.write(f"Netmask: {network.netmask}")
    st.write(f"Network Slash Notation: {network.exploded}")
    st.write(f"Is global: {is_global(network)}")
    st.write(f"Is private: {is_private(network.network_address)}")
    st.write(f"Is link local: {network.is_link_local}")
    st.write(f"Broadcast Address: {network.broadcast_address}")
    st.write(f"Network Version: {'IPv6' if network.version == 6 else 'IPv4'}")
    
    for ip in network.hosts():
        st.write(ip)

def main():
    st.title("Network Information Tool")
    st.write("Enter a network address in CIDR notation, e.g., 192.168.1.0/24")
    st.write("The app will display network address details and valid host addresses.")
    
    network = get_valid_input("Enter a network address in the following format xxx.xxx.xxx.0/xx: ")

    if network:
        print_network_details(network)
        print_hosts(network)
        st.success("Network information successfully processed!")
    else:
        st.info("No network address entered. Please try again.")

if __name__ == "__main__":
    main()