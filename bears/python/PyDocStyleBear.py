from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='pydocstyle',
        use_stderr=True,
        output_format='regex',
        output_regex=r'.*\.py:(?P<line>\d+) .+:\n\s+(?P<message>.*)')
class PyDocStyleBear:
    """
    Checks python docstrings.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
