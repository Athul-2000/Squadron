import yaml
from .logger import logprint

def GetYamlFileObject(filename):
    logprint.info(f"Reading {filename}")
    with open(filename) as f:
        config = yaml.safe_load(f)
    return config


def GetProcessesToBeKilled(filename):
    return GetYamlFileObject(filename)["processes_to_be_killed"]

def GetWifiInterfaces(filename):
    return GetYamlFileObject(filename)["wifi_interfaces"]  
