from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='proselint',
        output_regex=r'.+?:(?P<line>\d+):(?P<column>\d+): \S* (?P<message>.+)')
class ProseLintBear:
    # TODO -> Docs
    """

    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
