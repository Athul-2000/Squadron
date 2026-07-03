from utils import logprint
from utils import run_cmd

def DeleteStrayMacvlanInterfaces():
    logprint.info("Deleting stray Macvlans for all interfaces")
    links_raw = run_cmd(["ip", "-o", "link", "show"])
    
    for line in links_raw.splitlines():
        # Look for the '@' symbol indicating a virtual link (e.g., mv1@enp1s0)
        if "@" in line:
            iface_match = re.search(r':\s+([^@\s]+)@', line)
            if iface_match:
                iface = iface_match.group(1)
                # Double check if it is a macvlan type
                details = run_cmd(["ip", "-d", "link", "show", iface])
                if "macvlan" in details:
                    logprint.info(f"Deleting stray macvlan from host: {iface}")
                    run_cmd(["ip", "link", "delete", iface])