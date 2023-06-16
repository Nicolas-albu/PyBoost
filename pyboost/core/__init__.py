from pathlib import Path

from .beautify import BeautifyConsole
from .pyboost import PyBoost

__NAME_CONFIG_FILE__ = "pyboost.json"

# Gets the name of the folder where PyBoost is running.
__PATH_NAME__: str = Path().cwd().name

# Gets the current path directory.
__CURRENT_PATH__: Path = Path().cwd()

# Gets the path for debug the PyBoostCLI.
__DEBUG_PATH__: Path = __CURRENT_PATH__ / "scripts" / "debug"

__all__ = [
    "PyBoost",
    "__PATH_NAME__",
    "__DEBUG_PATH__",
    "BeautifyConsole",
    "__CURRENT_PATH__",
    "__NAME_CONFIG_FILE__",
]
