from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='alex',
        output_regex=r'\s*(?P<line>\d+):(?P<column>\d+)-(?P<end_line>\d+):'
                     r'(?P<end_column>\d+) +(?P<severity>warning)'
                     r' +(?P<message>.+)')
class AlexBear:
    """
    Checks the markdown file with Alex - Catch insensitive, inconsiderate
    writing.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
