import subprocess
from typing import List, Optional
import os

import logging
import colorlog

import time

logprint = logging.getLogger("wifi_framework")
logprint.setLevel(logging.DEBUG)

# handler = colorlog.StreamHandler()
# handler.setFormatter(
#     colorlog.ColoredFormatter(
#         "%(log_color)s%(asctime)s\t[%(levelname)s]\t%(message)s",
#         log_colors={
#             "DEBUG": "cyan",
#             "INFO": "green",
#             "WARNING": "yellow",
#             "ERROR": "red",
#             "CRITICAL": "bold_red",
#         }
#     )
# )

# logprint.addHandler(handler)
# logprint.propagate = False



if not logprint.handlers:
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s\t[%(levelname)s]\t%(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            }
        )
    )
    logprint.addHandler(handler)

logprint.propagate = False



class CommandExecutor:

    def __init__(self,
                 default_timeout: int = 30,
                 logger=None):
        self.default_timeout = default_timeout
        self.logger = logger

    def execute(
            self,
            cmd: List[str],
            timeout: Optional[int] = None,
            check: bool = False):

        timeout = timeout or self.default_timeout

        if self.logger:
            self.logger.debug(f"Executing: {' '.join(cmd)}")

        try:

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=check
            )

            if self.logger:

                self.logger.debug(
                    f"Return Code : {result.returncode}"
                )

                if result.stdout:
                    self.logger.debug(result.stdout.strip())

                if result.stderr:
                    self.logger.debug(result.stderr.strip())

            return result

        except subprocess.TimeoutExpired:

            if self.logger:
                self.logger.error(
                    f"Command timed out after {timeout}s"
                )

            return None

        except subprocess.CalledProcessError as e:

            if self.logger:
                self.logger.error(str(e))

            return e

        except Exception as e:

            if self.logger:
                self.logger.exception(e)

            return None

    def execute_in_namespace(
            self,
            namespace: str,
            cmd: List[str],
            timeout: Optional[int] = None,
            check: bool = False):

        return self.execute(
            ["ip", "netns", "exec", namespace] + cmd,
            timeout,
            check
        )

class WPASupplicant:
    def __init__(self, client: Client, executer):
        self.interface = client.interface
        self.namespace = client.namespace
        self.executer = executer
        self.config_path = f"/tmp/squadron/{self.interface}"
        self.saved_network = []

    def generate_config(self):
        config = f"""ctrl_interface=/run/wpa_supplicant
        update_config=1
        """
        os.makedirs("/tmp/squadron", exist_ok=True)
        with open(self.config_path, "w") as f:
            f.write(config)
        wpa_supplicant_cmd = ["wpa_supplicant", "-B", "-i", self.interface, "-c", self.config_path]
        self.executer.execute_in_namespace(self.namespace, wpa_supplicant_cmd)


    def connect_SSID(self, network_id = 0):
        logprint.info(f"Connecting with network id: {network_id}, SSID: {self.get_ssid_from_network_id(network_id)}")
        wpa_cli_cmd = ["wpa_cli", "-i", self.interface, "select_network", str(network_id)]
        self.executer.execute_in_namespace(self.namespace, wpa_cli_cmd)

    def disconnect_SSID(self):
        logprint.info(f"Disconnecting SSID")
        wpa_cli_cmd = ["wpa_cli", "-i", self.interface, "disconnect"]
        self.executer.execute_in_namespace(self.namespace, wpa_cli_cmd)

    def stop_wpa_supplicant(self):
        logprint.info(f"Stopping wpa supplicant")
        wpa_cli_cmd = ["wpa_cli", "-i", self.interface, "terminate"]
        self.executer.execute_in_namespace(self.namespace, wpa_cli_cmd)

    def remove_network(self, network_id):
        network_id = str(network_id)
        logprint.info(f"Removing network with network id: {network_id}")
        wpa_cli_cmd = ["wpa_cli", "-i", self.interface, "remove_network", network_id]
        self.executer.execute_in_namespace(self.namespace, wpa_cli_cmd)  
        for index, item in enumerate(self.saved_network):
            if item.network_id == network_id:
                popped_item = self.saved_network.pop(index)
                logprint.info(f"Popped ID: {popped_item.network_id}")
                break

    def remove_all_network(self):
        logprint.info(f"Removing all networks")
        wpa_cli_cmd = ["wpa_cli", "-i", self.interface, "remove_network", "all"]
        self.executer.execute_in_namespace(self.namespace, wpa_cli_cmd)     

    def add_SSID(self, ssid, password):
        result = self.executer.execute_in_namespace(
            self.namespace,
            ["wpa_cli", "-i", self.interface, "add_network"]
        )
        network_id = str(result.stdout.strip())

        wpa_cli_cmd = ["wpa_cli", "-i", self.interface, "set_network", network_id, "ssid", f'"{ssid}"']
        self.executer.execute_in_namespace(self.namespace, wpa_cli_cmd)
        wpa_cli_cmd = ["wpa_cli", "-i", self.interface, "set_network", network_id, "psk", f'"{password}"']
        self.executer.execute_in_namespace(self.namespace, wpa_cli_cmd)
        self.saved_network.append(WPASavedSSID(network_id, ssid, password))

    def display_all_saved_networks(self):
        logprint.debug(f"Saved Network List")
        for index, network in enumerate(self.saved_network):
            logprint.debug(f"Saved Network {index}")
            logprint.debug(f"Network ID\t{network.network_id}")
            logprint.debug(f"SSID\t{network.ssid}")
            logprint.debug(f"Password\t{network.password}")
        
        
        wpa_cli_cmd = ["wpa_cli", "-i", self.interface, "list_network"]
        self.executer.execute_in_namespace(self.namespace, wpa_cli_cmd)

    def get_ssid_from_network_id(self, network_id):
        ssid = None
        for network in self.saved_network:
            if network.network_id == str(network_id):
                ssid = network.ssid
        return ssid

class WPASavedSSID:
    def __init__(self, network_id, ssid, password):
        self.network_id = network_id
        self.ssid = ssid
        self.password = password


class Client:
    def __init__(self, interface, namespace):
        self.interface = interface
        self.namespace = namespace

def main():
    executer = CommandExecutor(logger = logprint)
    client = Client("wlx00c0caba4553", "ns2")
    x = WPASupplicant(client, executer)
    x.stop_wpa_supplicant()
    time.sleep(2)
    x.generate_config()
    x.add_SSID("Hydra0", "K5x48Vz3")
    x.add_SSID("Hydra", "K5x48Vz3")
    x.add_SSID("Hydra2", "K5x48Vz3")
    x.add_SSID("Hydra3", "K5x48Vz3")
    x.add_SSID("Hydra4", "K5x48Vz3")
    x.add_SSID("Hydra5", "K5x48Vz3")
    x.display_all_saved_networks()
    x.remove_network(6)
    x.display_all_saved_networks()
    x.connect_SSID(1)
    x.display_all_saved_networks()
    x.disconnect_SSID()
    x.display_all_saved_networks()
    x.connect_SSID(1)
    x.display_all_saved_networks()

if __name__ == "__main__":
    main()