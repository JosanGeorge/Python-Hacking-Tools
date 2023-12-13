#!/usr/bin/env python3
import subprocess
import optparse
import re

def arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help = "Specify The Interface")
    parser.add_option("-m", "--mac", dest = "new_mac", help="Specify The New MAC")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Specify The Interface, --help for more info")
    elif not options.new_mac:
        parser.error("[-] Specify The New MAC, --help for more info")
    else:
        return options

def mac_changer(interface,new_mac):
    print("[+] Changing MAC Address of " + interface + " To " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def current_mac(interface):
    ifconfig = subprocess.check_output(["ifconfig", interface])
    search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))
    if search_result:
        return search_result.group(0)
    else:
        return None

options = arguments()
present_mac = current_mac(options.interface)
print("Current MAC: " + str(present_mac))
mac_changer(options.interface, options.new_mac)
present_mac = current_mac(options.interface)
if present_mac == options.new_mac:
    print("[+] MAC Address Was Successfully Changed To " + str(present_mac))
else:
    print("[-] MAC Address Has Not Been Changed")
