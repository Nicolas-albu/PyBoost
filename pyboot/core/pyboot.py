"""
This module provides the PyBoot class for building projects with PyBoot
configuration.
"""

from typing import Generator

from .builder import AbstractBuilder, factory_builder
from .environment import Environment


class PyBootDirector:
    """
    The PyBoot class for building projects with PyBoot configuration.

    This class represents a project builder with PyBoot configuration. It
    provides functionality for creating and configuring projects based on
    specified options.
    """

    __slots__ = ['__venv', '__builder']

    def __init__(self, **options):
        """
        Initialize the PyBoot instance.

        Attributes:
            __builder (Builder): The Builder instance for project building
                operations.
            __venv (Environment): The Environment instance for managing the
                project's virtual environment.

        Example:
            >>> from pyboot.core import PyBootDirector
            >>>
            >>> project_name = input('What is the name of the project? ')
            >>> pyboot = PyBootDirector(project_name=project_name, ...)
            >>>
            >>> for task in pyboot.run():
            ...     print(task)
        """
        __class_builder = factory_builder(template_name=options['template'])
        self.__venv = Environment(project_path=options['project_path'])
        self.__builder: AbstractBuilder = __class_builder(self.__venv, options)

    def run(self) -> Generator:
        """
        Run the project building process.

        This method performs the necessary steps for project configuration and
        file generation.
        """
        yield from self.__builder.run()
