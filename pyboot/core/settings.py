from os.path import abspath, dirname
from pathlib import Path

__NAME_CONFIG_FILE__ = 'pyboot.toml'

__DEFAULT_VENV_NAME__ = '.venv'

__VENV_NAMES__ = __DEFAULT_VENV_NAME__, 'venv', 'env'

# Gets the current project path.
__CURRENT_PATH__: Path = Path().cwd()

# Gets the name of the folder where PyBoot is running.
__PATH_NAME__: str = Path().cwd().name

__BASE_DIR__ = Path(dirname(abspath(__file__))).parent.parent

__TEMPLATES_PATH__: Path = __BASE_DIR__ / 'templates'

__ENVIRONMENT_STAGES__: tuple = 'development', 'testing', 'production'

__TEMPLATES_NAME__ = [
    'django4.2-blank',
]
