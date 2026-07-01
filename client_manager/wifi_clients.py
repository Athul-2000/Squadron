from interface_manager import WiFiInterface
from namespace_manager import Namespace
from utils import LinkNamespaceWithPhy


def CreateClient(wifi_interface_obj_list, namespace_obj_list):
    wifi_clients_list = []
    client_count = 0
    for wifi_interface,namespace in zip(wifi_interface_obj_list,namespace_obj_list):
        link_ns_with_phy = LinkNamespaceWithPhy(wifi_interface.GetWlanPhy(), namespace.GetNamespaceName())
        if link_ns_with_phy.returncode == 0:
            wifi_interface.SetIsNamespaceBinded(True)
        wifi_interface.BindNamespace(namespace)
        client_count = client_count + 1
        client_name = f"Client{client_count}"
        wifi_clients_list.append(WifiClient(client_name, namespace, wifi_interface))
    return wifi_clients_list


def MakeLoopbackAndWifiInterfacesUp(clients_list):
    for client in clients_list:
        client.MakeLoopbackInterfaceUp()
        client.MakeWifiInterfaceUp()



def ConnectClientsToWifiAP(clients_list, filepath):
    for client in clients_list:
        wifi_interface = client.GetWifiInterfaceName()
        wpa_supplicant_cmd = ["wpa_supplicant", "-B", "-i", wifi_interface, "-c", filepath]
        client.ExecuteCommandInNamespace(wpa_supplicant_cmd)

def DisableDhcp(clients_list) -> None:
    for client in clients_list:
        wifi_interface = client.GetWifiInterfaceName()
        dhclient_disable_command = ["dhclient", wifi_interface]
        client.ExecuteCommandInNamespace(dhclient_disable_command)


def EnableDhcp(clients_list) -> None:
    for client in clients_list:
        wifi_interface = client.GetWifiInterfaceName()
        dhclient_enable_command = ["dhclient", wifi_interface]
        client.ExecuteCommandInNamespace(dhclient_enable_command)

class WifiClient():
    def __init__(self, name, namespace, wifi_interface):
        self.name: str = name
        self.namespace: Namespace = namespace
        self.wifi_interface: WiFiInterface = wifi_interface

    def GetName(self):
        return self.name

    def SetNamespace(self, namespace: Namesapce):
        self.namespace = namespace

    def SetWifiInterface(self, wifi_interface: WiFiInterface):
        self.wifi_interface = wifi_interface

    def GetNamespace(self) -> Namesapce:
        return self.namespace

    def GetNamespaceName(self) -> str:
        return self.namespace.GetNamespaceName()

    def GetWifiInterface(self) -> WiFiInterface:
        return self.wifi_interface

    def GetWifiInterfaceName(self) -> str:
        return self.GetWifiInterface().GetWifiInterfaceName()

    def GetWifiInterfacePhy(self) -> str:
        return self.GetWifiInterface().GetWlanPhy()

    def MakeLoopbackInterfaceUp(self) -> None:
        command = ["ip", "link", "set", "lo", "up"]
        self.GetNamespace().ExecuteInNamespace(command)

    def MakeWifiInterfaceUp(self) -> None:
        command = ["ip", "link", "set", self.GetWifiInterfaceName(), "up"]
        self.GetNamespace().ExecuteInNamespace(command)

    def ExecuteCommandInNamespace(self, command: list) -> None:
        self.GetNamespace().ExecuteInNamespace(command)