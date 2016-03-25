from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='goreturns',
        provides_correction=True,
        use_stdin=True,
        diff_message='Imports or returns need to be added/removed.')
class GoReturnsBear:
    """
    Proposes corrections of Go code using ``goreturns``.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return tuple()
