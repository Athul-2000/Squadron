import subprocess
from typing import List, Optional


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
