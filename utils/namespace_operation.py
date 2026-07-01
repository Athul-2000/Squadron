from utils import logprint
from utils import run_cmd
from utils import KillProcessByPID

def LinkNamespaceWithPhy(phy, namespace_name):
    command = ["iw", "phy", phy, "set", "netns", "name", namespace_name]
    logprint.info(f"Linking namespace {namespace_name} with phy {phy}")
    result = run_cmd(["iw", "phy", phy, "set", "netns", "name", namespace_name])
    if result and result.returncode == 0:
        logprint.info(f"Linked namespace {namespace_name} with phy {phy}")
    else:
        logprint.error(f"Failed to link namespace {namespace_name} with phy {phy}")
        if result:
            logprint.error(result.stderr.strip())
    return result



def DeleteNamespaceByName(namespace_name):
    result = run_cmd(["ip", "netns", "delete", namespace_name])

    if result and result.returncode == 0:
        logprint.info(f"Deleted namespace {namespace_name}")
    else:
        logprint.error(f"Failed to delete namespace {namespace_name}")
        if result:
            logprint.error(result.stderr.strip())


def CreateNamespaceByName(namespace_name):
    logprint.info(f"Creating namespace: {namespace_name}")
    result = run_cmd(["ip", "netns", "add", namespace_name])
    if result and result.returncode == 0:
        logprint.info(f"Created namespace {namespace_name}")
    else:
        logprint.error(f"Failed to create namespace {namespace_name}")
        if result:
            logprint.error(result.stderr.strip())
    return result


def ExecuteCommandInNamespace(namespace_name, command):
    result = run_cmd(["ip", "netns", "exec", namespace_name] + command)


def DeleteAllNamespaces():
    logprint.info("STARTING EXISTING NAMESPACE CLEANUP")

    # 1. Identify all namespaces on the device
    result = run_cmd(["ip", "netns", "list"])

    if result is None:
        logprint.error("Failed to retrieve namespace list.")
        return

    namespaces = [
        line.split()[0]
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    if not namespaces:
        logprint.warning("No network namespaces found on device.")
        return

    logprint.info(f"Found {len(namespaces)} namespaces: {', '.join(namespaces)}")

    for ns in namespaces:
        logprint.info(f"Cleaning namespace: {ns}")

        # Kill dhclient running inside the namespace
        result = run_cmd(["ip", "netns", "exec", ns, "pgrep", "dhclient"])

        if result and result.returncode == 0:
            for pid in result.stdout.split():
                logprint.info(f"Killing dhclient PID {pid} in {ns}")
                KillProcessByPID(pid)
        else:
            logprint.debug(f"No dhclient running in {ns}")

        DeleteNamespaceByName(ns)

