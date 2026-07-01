from .logger import logprint
from .execute_command import run_cmd


def KillProcessByName(process_name):
    logprint.info(f"Killing process {process_name}")
    run_cmd(["pkill", process_name])

def KillProcessByPID(pid):
    logprint.info(f"Killing {pid}")
    run_cmd(["kill", pid])