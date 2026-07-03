from .execute_command import CommandExecutor

class WPASupplicant:
    def __init__(self, client: Client, executer):
        self.interface = client.interface
        self.namespace = client.namespace
        self.executer = executer
        self.config_path = f"/tmp/squadron/{self.interface}"
        self.saved_ssid = list[WPASavedSSID]

    def generate_config(self, ssid, password):
        config = f"""ctrl_interface=/run/wpa_supplicant
        update_config=1

        network=={{
            ssid="{ssid}"
            psk="{password}"
        }}
        """
        os.makedirs("/tmp/squadron", exist_ok=True)
        with open(self.config_path, "w") as f:
            f.write(config)
        wpa_supplicant_cmd = ["wpa_supplicant", "-B", "-i", self.interface, "-c", self.wpa_config]
        self.executer.execute_in_namespace(self.namespace, wpa_supplicant_cmd)


    def connect_SSID(self, id = 0):
        wpa_cli_cmd = ["wpa_cli", "-i", self.interface, "select_network", str(id)]
        self.executer.execute_in_namespace(wpa_cli_cmd)

    def disconnect_SSID(self):
        wpa_cli_cmd = ["wpa_cli", "-i", self.interface, "disconnect"]
        self.executer.execute_in_namespace(self.namespace, wpa_cli_cmd)

    def reconnect_SSID(self):
        wpa_cli_cmd = ["wpa_cli", "-i", self.interface, "reconnect"]
        self.executer.execute_in_namespace(self.namespace, wpa_cli_cmd)

    def stop_wpa_supplicant(self):
        wpa_cli_cmd = ["wpa_cli", "-i", self.interface, "terminate"]
        self.executer.execute_in_namespace(self.namespace, wpa_cli_cmd)

    def remove_network(self, id):
        wpa_cli_cmd = ["wpa_cli", "-i", self.interface, "remove_network", str(id)]
        self.executer.execute_in_namespace(wpa_cli_cmd)  

    def remove_all_network(self):
        wpa_cli_cmd = ["wpa_cli", "-i", self.interface, "remove_network", "all"]
        self.executer.execute_in_namespace(wpa_cli_cmd)     

    def add_SSID(self, id):
        saved_ssid_count = str(len(self.saved_ssid))
        wpa_cli_cmd = ["wpa_cli", "-i", self.interface, "add_network", saved_ssid_count, "ssid", 'self.ssid']
        self.executer.execute_in_namespace(wpa_cli_cmd)
        wpa_cli_cmd = ["wpa_cli", "-i", self.interface, "add_network", saved_ssid_count, "psk", 'K5x48Vz3']
        self.executer.execute_in_namespace(wpa_cli_cmd)
        wpa_cli_cmd = ["wpa_cli", "-i", self.interface, "enable_network"]
        self.executer.execute_in_namespace(wpa_cli_cmd)



class WPASavedSSID:
    def __init__(self, id, ssid, password):
        self.id = id
        self.ssid = ssid
        self.password = password

