"""
contra-env-setup - command

the library used to verify if commands exist
in the environment of tests
"""
from avocado.utils import path as utils_path
from avocado.utils.software_manager import SoftwareManager


def get_command(command, package=None):
    """
    check if the command is present in the environment
    of tests, if not can offer an installation on package argument
    """
    try:
        return utils_path.find_command(command)

    except utils_path.CmdNotFoundError:

        if package is None:
            raise utils_path.CmdNotFoundError

        sm_p = SoftwareManager()
        sm_p.install(package)
        return utils_path.find_command(command)
