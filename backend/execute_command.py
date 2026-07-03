
class ExecuteCommand:

    def ExecuteGlobalCommand(self, cmd, check=False):
        logprint.debug(f"Executing: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=check
            )

            logprint.debug(f"Return code: {result.returncode}")

            if result.stdout:
                logprint.debug(f"stdout: {result.stdout.strip()}")

            if result.stderr:
                logprint.debug(f"stderr: {result.stderr.strip()}")

            return result

        except FileNotFoundError:
            logprint.error(f"Command not found: {cmd[0]}")
            return None

        except Exception as e:
            logprint.exception(e)
            return None

    def ExecuteCommandInNamespace(self, namespace_name, cmd):
        result = self.ExecuteGlobalCommand(["ip", "netns", "exec", namespace_name] + cmd)