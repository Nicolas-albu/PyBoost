"""
This module provides the PyBoot class for building projects with PyBoot
configuration.
"""

from .builder import Builder
from .environment import Environment


class PyBoot:
    """
    The PyBoot class for building projects with PyBoot configuration.

    This class represents a project builder with PyBoot configuration. It
    provides functionality for creating and configuring projects based on
    specified options.
    """

    __slots__ = [
        '__options',
        '__name_project',
        '__builder',
        '__venv',
    ]

    def __init__(self, **options):
        """
        Initialize the PyBoot instance.

        Args:
            **options: Keyword arguments for configuring the PyBoot instance.
                - name_project: The name of the project.
                - directory: The directory of the project.
                - add_python_version: Add the .python-version file to the
                    project with the specified Python version.
                - add_poetry: Use Poetry to manage the project dependencies
                    instead of pip and virtualenv.
                - add_dotenv: Configure and add dotenv file to project.
                - add_format: Add the black formatter and isort to the project.
                - add_makefile: Add a makefile to the project.
                - with_drf: Add the Django Rest Framework to the project.

        Attributes:
            __options (dict): The options for configuring the PyBoot instance.
            __name_project (str): The name of the project.
            __builder (Builder): The Builder instance for project building
                operations.
            __venv (Environment): The Environment instance for managing the
                project's virtual environment.
        """
        self.__options = options
        __directory = options['directory']
        self.__name_project = self.__options['name_project']
        self.__builder = Builder(directory=__directory)
        self.__venv = Environment(project_path=__directory)

    def run(self) -> None:
        """
        Run the project building process.

        This method performs the necessary steps for project configuration and
        file generation.
        """
        # general settings
        self.__create_pyboot_config_file(self.__options)
        self.__create_folders('docs', 'static', 'media', 'templates', 'apps')

        if self.__options['add_python_version']:
            python_version = self.__options['add_python_version']
            self.__builder.add_python_version_file(python_version)

        if self.__options['add_makefile']:
            self.__builder.add_makefile()

        # environment settings
        self.__venv.add_dependency('django', version="4.2.2")
        self.__venv.add_dependency('dynaconf')
        self.__venv.export_django_settings(self.__name_project)

        # django settings
        self.__builder.add_main_folder(self.__venv, self.__name_project)
        self.__builder.add_settings_files(self.__name_project)
        self.__builder.configure_static_folder(self.__venv)

    def __create_pyboot_config_file(self, data: dict, /) -> None:
        """
        Create the PyBoot configuration file.

        Args:
            data: The data used for generating the configuration file.
        """
        # remove PosixPath of directory
        data['directory'] = str(data['directory'])

        # remove False values
        pyboot_config = dict(filter(lambda item: item[1], data.items()))

        self.__builder.create_config_file(pyboot_config)

    def __create_folders(self, *folders) -> None:
        """
        Create folders for the project.

        Args:
            *folders: Variable number of strings representing the names of the
                folders to be created.
        """
        for folder in folders:
            self.__builder.add_folder(folder)
