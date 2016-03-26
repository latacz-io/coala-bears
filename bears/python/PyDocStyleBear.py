from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='pydocstyle',
        output_regex=r'.*\.py:(?P<line>\d+) .+:\n\s+(?P<message>.*)',
        use_stderr=True)
class PyDocStyleBear:
    """
    Checks python docstrings.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
