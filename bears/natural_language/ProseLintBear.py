from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='proselint',
        output_format='regex',
        output_regex=r'.+?:(?P<line>\d+):(?P<column>\d+): \S* (?P<message>.+)')
class ProseLintBear:
    """
    Lints the file using ``proselint``.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
