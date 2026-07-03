from utils import logprint
from utils import run_cmd


def DeleteDhcplease():
    logging.info("Cleaning up leftover DHCP lease/PID files...")
    run_cmd(["rm", "-f", "/var/run/dhclient.ns*.pid"])
    run_cmd(["rm", "-f", "/var/lib/dhcp/dhclient.ns*.leases"])