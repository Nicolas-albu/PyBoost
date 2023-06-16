"""
This module provides the PyBoost class for building projects with PyBoost
configuration.
"""

__all__ = ["PyBoost"]

from .builder import Builder


class PyBoost:
    """
    The PyBoost class for building projects with PyBoost configuration.

    Args:
        **options: Keyword arguments for configuring the PyBoost instance.
            - directory: The directory of the project.
            - Other options specific to the project configuration.

    Attributes:
        __options (dict): The options for configuring the PyBoost instance.
        __builder (Builder): The Builder instance for project building
            operations.
    """

    def __init__(self, **options):
        """
        Initialize the PyBoost instance.

        Args:
            **options: Keyword arguments for configuring the PyBoost instance.
        """
        self.__options = options
        directory = options["directory"]
        self.__builder = Builder(directory=directory)

    def run(self) -> None:
        """
        Run the project building process.

        This method performs the necessary steps for project configuration and
        file generation.
        """
        self.__create_config_file(self.__options)

        if not self.__options["with_drf"]:
            name_project = self.__options["name_project"]
            self.__builder.add_main_folder(name_project)

        if self.__options["add_dotenv"]:
            with_drf: bool = self.__options["with_drf"]
            self.__builder.add_dotenv_file(with_drf)

        if self.__options["add_python_version"]:
            python_version = self.__options["add_python_version"]
            self.__builder.add_python_version_file(python_version)

        if self.__options["add_makefile"]:
            self.__builder.add_makefile()

    def __create_config_file(self, data: dict) -> None:
        """
        Create the PyBoost configuration file.

        Args:
            data: The data used for generating the configuration file.
        """
        pyboost_config = dict(filter(lambda item: item[1], data.items()))
        self.__builder.generate_pyboost_json(pyboost_config)
