from utils import logprint
from utils import run_cmd

def DisplayRFKillList():
    logprint.info(f"RFKill List")
    run_cmd(["rfkill", "list"])

def UnblockAllRFPhy():
    logprint.info(f"Unblocking RF Phy")
    run_cmd(["rfkill", "unblock", "all"])