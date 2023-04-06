import subprocess
from subprocess import CompletedProcess
from typing import List


def execute_cli_command(command: List[str]) -> CompletedProcess:
    """
    Args:
        command (List[str]): _description_ - ["ls", "-l", "-h"]

    Returns:
        CompletedProcess:
            has `stderr`, `stdout`, `returncode` attributes
    """
    process_result = subprocess.run(command, check=True, capture_output=True)
    print('stdout: ', process_result.stdout)
    print('stderr: ', process_result.stderr)
    if process_result.returncode != 0:
        raise Exception(process_result.stderr)
