from .logger import logprint
from .execute_command import run_cmd
import time

REMOVE_WIFI_DRIVER_CMD = ["modprobe", "-r", "rtw88_8812au"]
LOAD_WIFI_DRIVER_CMD = ["modprobe", "rtw88_8812au"]
SLEEP_TIME_BETWEEN_REMOVE_AND_LOAD = 4

def RemoveWifiDriver():
    logprint.info("Removing WiFi driver - rtw88_8812au")
    run_cmd(REMOVE_WIFI_DRIVER_CMD)

def LoadWifiDriver():
    logprint.info("Loading WiFi driver - rtw88_8812au")
    run_cmd(LOAD_WIFI_DRIVER_CMD)

def ReloadWifiDriver():
    RemoveWifiDriver()
    time.sleep(SLEEP_TIME_BETWEEN_REMOVE_AND_LOAD)
    LoadWifiDriver()