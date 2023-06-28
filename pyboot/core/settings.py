from os.path import abspath, dirname
from pathlib import Path

__NAME_CONFIG_FILE__ = 'pyboot.toml'

# Gets the current path directory.
__CURRENT_PATH__: Path = Path().cwd()

# Gets the name of the folder where PyBoot is running.
__PATH_NAME__: str = Path().cwd().name

__BASE_DIR__ = Path(dirname(abspath(__file__))).parent.parent

__SCRIPTS_PATH__: Path = __BASE_DIR__ / 'scripts'

__TEMPLATE_DJANGO_BLANK__: Path = __SCRIPTS_PATH__ / 'django_blank'

__SETTINGS_DJANGO__: Path = __TEMPLATE_DJANGO_BLANK__ / 'settings_django.py'

__REQUIREMENTS__: Path = __TEMPLATE_DJANGO_BLANK__ / 'requirements.txt'

__SECRETS_CONF_DJANGO__: Path = (
    __TEMPLATE_DJANGO_BLANK__ / 'secrets_conf_django.yaml'
)

__SETTINGS_CONF_DJANGO__: Path = (
    __TEMPLATE_DJANGO_BLANK__ / 'settings_conf_django.yaml'
)

__GITIGNORE_DJANGO__: Path = (
    __TEMPLATE_DJANGO_BLANK__ / 'conf_django.gitignore'
)
