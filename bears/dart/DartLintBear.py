from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='dartanalyzer',
        output_regex=r'\[(?P<severity>error|warning)\] (?P<message>.+)\('
                     r'(?P<file_name>.+), line (?P<line>\d+),'
                     r' col (?P<column>\d+)\)')
class DartLintBear:
    """
    Checks the code with ``dart-linter``.

    This bear expects dart commands to be on your ``PATH``. Please ensure
    /path/to/dart-sdk/bin is in your ``PATH``.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
