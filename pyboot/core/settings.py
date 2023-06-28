from dataclasses import dataclass
from os.path import abspath, dirname
from pathlib import Path

__NAME_CONFIG_FILE__ = 'pyboot.toml'

# Gets the current path directory.
__CURRENT_PATH__: Path = Path().cwd()

# Gets the name of the folder where PyBoot is running.
__PATH_NAME__: str = Path().cwd().name

__BASE_DIR__ = Path(dirname(abspath(__file__))).parent.parent

__SCRIPTS_PATH__: Path = __BASE_DIR__ / 'scripts'

__ENVIRONMENT_STAGES__: tuple = 'development', 'testing', 'production'


@dataclass(slots=True, eq=False, repr=False)
class Template:
    """Class that contains all paths to templates."""

    template_path: Path
    requirements: Path | str
    settings_django: Path | str
    gitignore_django: Path | str
    secrets_dynf_django: Path | str
    settings_dynf_django: Path | str

    def __post_init__(self):
        self.requirements = self.template_path / self.requirements
        self.settings_django = self.template_path / self.settings_django
        self.gitignore_django = self.template_path / self.gitignore_django
        self.secrets_dynf_django = (
            self.template_path / self.secrets_dynf_django
        )
        self.settings_dynf_django = (
            self.template_path / self.settings_dynf_django
        )

    def __iter__(self):
        yield from (
            self.secrets_dynf_django,
            self.settings_django,
            self.gitignore_django,
            self.settings_dynf_django,
            self.requirements,
        )


# Configurations of template django-blank
__DJANGO_BLANK__: Path = __SCRIPTS_PATH__ / 'django_blank'

template_django_blank = Template(
    template_path=__DJANGO_BLANK__,
    requirements='requirements.txt',
    settings_django='settings_django.py',
    gitignore_django='cfg_django.gitignore',
    secrets_dynf_django='secrets_dynf_django.yaml',
    settings_dynf_django='settings_dynf_django.yaml',
)
