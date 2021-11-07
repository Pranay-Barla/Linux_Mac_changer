

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()  # its a class and 'parser' is its object
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC")
    parser.add_option("-m", "--mac", dest="new_mac", help="new MAC")
    (options, arguments) = parser.parse_args()  # ooptions wil contain eth0 arguments will contain --i etc
    if not options.interface:
        parser.error("[-] Please Specify interface, use --help")
    elif not options.new_mac:
        parser.error("[-] Please Specify new mac, use --help")
    return options

def change_mac(interface, new_mac):
    print("[+] Changing MAC Address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-]Could not read Mac Address")

options = get_arguments()
current_mac = get_current_mac(options.interface)
print("[+]Current MAC = " + str(current_mac))

change_mac(options.interface, options.new_mac) #calling the function

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC Address was Successfully changed to " + options.new_mac)
else:
    print("[-] MAC Adress did not change.")
