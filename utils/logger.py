import logging
import colorlog

logprint = logging.getLogger("wifi_framework")
logprint.setLevel(logging.DEBUG)

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

# =========== USAGE ===========
# logprint.info("Normal Info")
# logprint.warning("Warning Message")
# logprint.error("Error Message")
# logprint.critical("Critical Message")
# logprint.debug("Debug Log")