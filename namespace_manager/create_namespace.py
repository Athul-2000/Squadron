from utils import CreateNamespaceByName
from utils import GetWifiInterfaces
from utils import ExecuteCommandInNamespace

def CreateWifiNamespaces(filename) -> list[Namespace]:
    interfaces_count = 0
    namespace_obj_list = []
    interfaces_count = len(GetWifiInterfaces(filename))
    for count in range(1, interfaces_count + 1):
        namespace_name = f"ns{count}"
        namespace = Namespace(namespace_name)
        create_ns_result = CreateNamespaceByName(namespace.GetNamespaceName())
        if create_ns_result.returncode == 0:
            namespace.SetIsCreated(True)
        namespace_obj_list.append(namespace)
    return namespace_obj_list

def CreateEthernetNamespaces(filename):
    print("Sample")



class Namespace:
    def __init__(self, namespace_name):
        self.namespace_name: str = namespace_name
        self.is_created_flag: bool = False

    def SetNamespaceName(self, namespace_name: str) -> None:
        self.namespace_name = namespace_name
    
    def GetNamespaceName(self) -> str:
        return self.namespace_name

    def ExecuteInNamespace(self, command) -> None:
        ExecuteCommandInNamespace(self.GetNamespaceName(), command)

    def SetIsCreated(self, flag: bool) -> None:
        self.is_created_flag = flag

    def GetIsCreated(self) -> bool:
        return self.is_created_flag