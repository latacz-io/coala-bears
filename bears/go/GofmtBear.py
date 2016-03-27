from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='gofmt',
        use_stdin=True,
        output_format='corrected',
        diff_message='Formatting can be improved.')
class GofmtBear:
    """
    Proposes corrections of Go code using gofmt.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return tuple()
