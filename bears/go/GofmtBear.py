from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='gofmt',
        provides_correction=True,
        use_stdin=True,
        diff_message='Formatting can be improved.')
class GofmtBear:
    """
    Proposes corrections of Go code using gofmt.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return tuple()
