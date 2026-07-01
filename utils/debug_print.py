from .execute_command import run_cmd
from .logger import logprint

def Seperator() -> None:
    logprint.debug("#"*30)

def WifiInterfaceView(wifi_interfaces_list: WiFiInterface) -> None:
    Seperator()
    logprint.debug("DEBUG LOGS FOR WIFI INTERFACE")
    for wifi_interface in wifi_interfaces_list:
        logprint.debug(f"Interface: {wifi_interface.GetWifiInterfaceName()}")
        logprint.debug(f"Phy: {wifi_interface.GetWlanPhy()}")
        logprint.debug(f"Namespace: {wifi_interface.GetBindedNamespace().GetNamespaceName()}")
    Seperator()

def ClientView(clients_list: WifiClient) -> None:
    Seperator()
    logprint.debug("DEBUG LOGS FOR WIFI CLIENTS")
    for client in clients_list:
        logprint.debug(f"Client Name: {client.GetName()}")
        logprint.debug(f"Interface: {client.GetWifiInterfaceName()}")
        logprint.debug(f"Phy: {client.GetWifiInterfacePhy()}")
        logprint.debug(f"Namespace: {client.GetNamespaceName()}")
        logprint.debug(f"ifconfig:")
        client.ExecuteCommandInNamespace(["ifconfig"])
        logprint.debug(f"iw <interface> link:")
        client.ExecuteCommandInNamespace(["iw", client.GetWifiInterfaceName(), "link"])
    Seperator()