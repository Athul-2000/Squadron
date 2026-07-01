import subprocess
import time
from .logger import logprint

def GetPhy(iface):
    return_value = None
    out = subprocess.check_output(
        ["iw", "dev", iface, "info"],
        text=True
    )

    for line in out.splitlines():
        line = line.strip()
        if line.startswith("wiphy"):
            return_value = int(line.split()[1])

    if return_value == None:
        logprint.info(f"{iface} corresponds to Nil")
    else:
        logprint.info(f"{iface} corresponds to phy{return_value}")
    return return_value


def SetInterfaceUp(iface):
    subprocess.run(
        ["ip", "link", "set", iface, "up"],
        check=True
    )


def SetInterfaceDown(iface):
    subprocess.run(
        ["ip", "link", "set", iface, "down"],
        check=True
    )


def GetInterfaceState(iface):
    out = subprocess.check_output(
        ["ip", "link", "show", iface],
        text=True
    )

    # look for "state UP/DOWN"
    for line in out.splitlines():
        if "state" in line:
            return line.split()[8]  # crude but works

    return None

# iface = "wlx00c0caba4552"

# print("PHY:", GetPhy(iface))

# SetInterfaceDown(iface)
# time.sleep(4)
# print("State:", get_state(iface))


# SetInterfaceUp(iface)
# time.sleep(4)
# print("State:", GetInterfaceState(iface))
