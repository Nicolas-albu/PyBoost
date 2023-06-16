from pathlib import Path

from .beautify import BeautifyConsole
from .pyboot import PyBoot

__NAME_CONFIG_FILE__ = "pyboot.json"

# Gets the name of the folder where PyBoot is running.
__PATH_NAME__: str = Path().cwd().name

# Gets the current path directory.
__CURRENT_PATH__: Path = Path().cwd()

# Gets the path for debug the PyBootCLI.
__DEBUG_PATH__: Path = __CURRENT_PATH__ / "scripts" / "debug"

__all__ = [
    "PyBoot",
    "__PATH_NAME__",
    "__DEBUG_PATH__",
    "BeautifyConsole",
    "__CURRENT_PATH__",
    "__NAME_CONFIG_FILE__",
]
