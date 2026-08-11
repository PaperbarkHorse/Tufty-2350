from menu.base import Menu, MenuItem
from menu.items.header import Header
from menu.items.button import Button
from menu.items.spacer import Spacer
from menu.items.dropdown import Dropdown
from menu.items.property import Property
import system
import secrets
import wifi

class NetworkMenu(Menu):
    
    def __init__(self):
        super().__init__()

        network_dropdown = Dropdown("Network", system.get_selected_network, system.set_selected_network)
        network_dropdown.add_option(None, "[None]")
        for network in secrets.WIFI_NETWORKS:
            network_dropdown.add_option(network, network["name"])

        self.add_item(Header("Network"))
        self.add_item(Button("Back", self.close))
        self.add_item(network_dropdown)
        self.add_item(Property("SSID", lambda: (system.get_selected_network() or {}).get("ssid")))
        self.add_item(Spacer(5))
        self.add_item(Header("Actions"))
        self.add_item(Button("Connect", self.connect))
        self.add_item(Button("Disconnect", wifi.disconnect))
        self.add_item(Spacer(5))
        self.add_item(Header("Status"))
        self.add_item(Property("Connected", wifi.is_connected))
        self.add_item(Property("Status", lambda: wifi.status()[0]))
        self.add_item(Property("", lambda: wifi.status()[1]))
        self.add_item(Property("Address", wifi.ip))
        self.add_item(Property("Gateway", wifi.gateway))
        self.add_item(Property("Subnet", wifi.subnet))
        self.add_item(Property("DNS", wifi.nameserver))

    def connect(self):
        network = system.get_selected_network()

        if network == None:
            return

        wifi.disconnect()
        wifi.connect(network["ssid"], network["password"])
