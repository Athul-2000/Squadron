from utils import GetPhy,SetInterfaceUp,SetInterfaceDown,GetInterfaceState,GetWifiInterfaces
from utils import CreateNamespaceByName,LinkNamespaceWithPhy
from namespace_manager import Namespace

def GetWifiInterfacePhy(filename) -> list[WiFiInterface]:
    wifi_interface_obj_list = []
    for wifi_interface in GetWifiInterfaces(filename):
        obj = WiFiInterface(wifi_interface)
        phy = GetPhy(wifi_interface)
        phy_name = None
        if phy != None:
            obj.SetWlanPhyStatus(True)
            phy_name = "phy"+str(phy)

        obj.SetWlanPhy(phy_name)
        wifi_interface_obj_list.append(obj)
    return wifi_interface_obj_list


def BindWifiInterfaceWithNamespace(wifi_interface_obj_list, namespace_obj_list):
    for wifi_interface,namespace in zip(wifi_interface_obj_list,namespace_obj_list):
        link_ns_with_phy = LinkNamespaceWithPhy(wifi_interface.GetWlanPhy(), namespace.GetNamespaceName())
        if link_ns_with_phy.returncode == 0:
            wifi_interface.SetIsNamespaceBinded(True)
        wifi_interface.BindNamespace(namespace)



class WiFiInterface:
    def __init__(self, wifi_interface_name: str):
        self.wifi_interface_name: str = wifi_interface_name
        self.phy: str = None
        self.namespace: Namespace = None
        self.wlan_phy_status: bool = False
        self.is_namespace_binded: bool = False

    def SetWifiInterfaceName(self, wifi_interface_name: str):
        self.wifi_interface_name = wifi_interface_name
    
    def GetWifiInterfaceName(self) -> str:
        return self.wifi_interface_name

    def SetWlanPhy(self, phy: str) -> None:
        self.phy = phy

    def GetWlanPhy(self) -> str:
        return self.phy

    def GetWlanPhyStatus(self) -> bool: 
        return self.wlan_phy_status

    def SetWlanPhyStatus(self, status: bool):
        self.wlan_phy_status = status

    def GetIsNamespaceBinded(self) -> bool:
        return self.is_namespace_binded

    def SetIsNamespaceBinded(self, status: bool):
        self.is_namespace_binded = status

    def BindNamespace(self, namespace: Namespace):
        self.namespace = namespace

    def GetBindedNamespace(self) -> Namespace:
        return self.namespace