from utils import DeleteAllNamespaces
from utils import DisplayRFKillList,UnblockAllRFPhy
from utils import logprint
from utils import KillProcessByName
from utils import GetProcessesToBeKilled
from utils import ReloadWifiDriver
from client_manager import CreateClient
from namespace_manager import CreateWifiNamespaces
from interface_manager import GetWifiInterfacePhy
from utils import WifiInterfaceView,ClientView
from client_manager import MakeLoopbackAndWifiInterfacesUp
from client_manager import ConnectClientsToWifiAP
from client_manager import EnableDhcp

import time

CONFIG_FILE_PATH = "config_files/config.yaml"
WIFI_AP_PATH = "config_files/wpa.conf"

def KillDependentProcess():
    for process in GetProcessesToBeKilled(CONFIG_FILE_PATH):
        KillProcessByName(process)



def Prerequesites():
    KillDependentProcess()
    DeleteAllNamespaces()
    ReloadWifiDriver()
    DisplayRFKillList()
    UnblockAllRFPhy()
    DisplayRFKillList()


def CreateAndConfigureClients():
    wifi_interfaces_list = GetWifiInterfacePhy(CONFIG_FILE_PATH)
    namespace_list = CreateWifiNamespaces(CONFIG_FILE_PATH)
    clients_list = CreateClient(wifi_interfaces_list, namespace_list)
    MakeLoopbackAndWifiInterfacesUp(clients_list)

    ConnectClientsToWifiAP(clients_list, WIFI_AP_PATH)
    time.sleep(5)
    EnableDhcp(clients_list)
    time.sleep(5)

    WifiInterfaceView(wifi_interfaces_list)
    ClientView(clients_list)


def WifiConfigure():
    Prerequesites()
    CreateAndConfigureClients()



def main():
    WifiConfigure()
    EthernetConfigure()


if __name__ == "__main__":
    main()
