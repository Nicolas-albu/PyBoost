from os.path import abspath, dirname
from pathlib import Path

__NAME_CONFIG_FILE__ = 'pyboot.toml'

# Gets the current path directory.
__CURRENT_PATH__: Path = Path().cwd()

# Gets the name of the folder where PyBoot is running.
__PATH_NAME__: str = Path().cwd().name

__BASE_DIR__ = Path(dirname(abspath(__file__))).parent.parent

__SCRIPTS_PATH__: Path = __BASE_DIR__ / 'scripts' / 'django_blank'

__SECRETS_CONF_DJANGO__: Path = __SCRIPTS_PATH__ / 'secrets_conf_django.yaml'

__SETTINGS_CONF_DJANGO__: Path = __SCRIPTS_PATH__ / 'settings_conf_django.yaml'

__SETTINGS_DJANGO__: Path = __SCRIPTS_PATH__ / 'settings_django.py'

__GITIGNORE_DJANGO__: Path = __SCRIPTS_PATH__ / 'conf_django.gitignore'
