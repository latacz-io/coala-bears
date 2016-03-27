from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='cppclean',
        output_format='regex',
        output_regex=r'(?P<file_name>[^,:]+):(?P<line>\d+):(?P<message>.*)')
class CPPCleanBear:
    """
    Checks code with ``cppclean``.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
