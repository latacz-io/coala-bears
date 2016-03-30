from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='mcs',
        output_stream='stderr',
        output_format='regex',
        output_regex=r'.+\((?P<line>\d+),(?P<column>\d+)\): '
                     r'(?P<severity>error|warning) \w+: (?P<message>.+)')
class CSharpLintBear:
    """
    Checks the code with ``mcs`` on each file separately.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
