from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='sqlint',
        use_stdin=True,
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+):'
                     r'(?P<severity>ERROR|WARNING) (?P<message>(?:\s*.+)*)')
class SQLintBear:
    """
    Checks the given file using ``sqlint``.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return tuple()
