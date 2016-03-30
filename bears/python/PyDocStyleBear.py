from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='pydocstyle',
        output_stream='stderr',
        output_format='regex',
        output_regex=r'.*:(?P<line>\d+) .+:\n\s+(?P<message>.*)')
class PyDocStyleBear:
    """
    Checks python docstrings.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
