from coalib.bearlib.abstractions.Linter import Linter
from coalib.settings.Setting import path


@Linter(executable='cmakelint',
        output_regex=r'(?P<file_name>\S+):(?P<line>[0-9]+): (?P<message>.*)')
class CMakeLintBear:
    """
    Checks the code with ``cmakelint``.
    """

    @staticmethod
    def create_arguments(filename,
                         file,
                         config_file,
                         cmakelint_config: path=""):
        """
        :param cmakelint_config: The location of the cmakelintrc config file.
        """
        return (('--config=' + cmakelint_config)
                if cmakelint_config else tuple() + (filename,))
