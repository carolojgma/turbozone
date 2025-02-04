import os
import subprocess
import socket

def get_local_ip():
    """Retrieve the local IP address of the current machine."""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def ping_test(host='google.com'):
    """Perform a simple ping test to a given host."""
    response = subprocess.run(['ping', '-n', '4', host], capture_output=True, text=True)
    if response.returncode == 0:
        print(f"Ping to {host} successful:\n{response.stdout}")
    else:
        print(f"Ping to {host} failed:\n{response.stderr}")

def flush_dns():
    """Flush the DNS cache to improve connectivity."""
    response = subprocess.run(['ipconfig', '/flushdns'], capture_output=True, text=True)
    if response.returncode == 0:
        print("DNS cache successfully flushed.")
    else:
        print(f"Failed to flush DNS cache:\n{response.stderr}")

def display_network_status():
    """Display the current network status and configuration."""
    response = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
    if response.returncode == 0:
        print(f"Network Configuration:\n{response.stdout}")
    else:
        print(f"Failed to retrieve network configuration:\n{response.stderr}")

def change_dns_server(dns_server):
    """Change the DNS server to the specified address."""
    interface = get_active_interface()
    if interface:
        response = subprocess.run(['netsh', 'interface', 'ip', 'set', 'dns', interface, 'static', dns_server], 
                                  capture_output=True, text=True)
        if response.returncode == 0:
            print(f"DNS server changed to {dns_server}.")
        else:
            print(f"Failed to change DNS server:\n{response.stderr}")
    else:
        print("No active network interface found.")

def get_active_interface():
    """Get the name of the active network interface."""
    response = subprocess.run(['netsh', 'interface', 'show', 'interface'], capture_output=True, text=True)
    if response.returncode == 0:
        interfaces = response.stdout.splitlines()
        for line in interfaces:
            if "Connected" in line:
                return line.split()[3]  # Assumes interface name is the fourth column
    return None

def main():
    print("Welcome to TurboZone - Network Enhancement Tool for Windows")
    print(f"Your local IP address is: {get_local_ip()}")

    while True:
        print("\nChoose an option:")
        print("1. Perform a ping test")
        print("2. Flush DNS cache")
        print("3. Display network status")
        print("4. Change DNS server")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            host = input("Enter host to ping (default: google.com): ") or 'google.com'
            ping_test(host)
        elif choice == '2':
            flush_dns()
        elif choice == '3':
            display_network_status()
        elif choice == '4':
            dns = input("Enter new DNS server address: ")
            change_dns_server(dns)
        elif choice == '5':
            print("Exiting TurboZone. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()