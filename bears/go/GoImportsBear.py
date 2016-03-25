from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='goimports',
        provides_correction=True,
        use_stdin=True,
        diff_message='Imports need to be added/removed.')
class GoImportsBear:
    """
    Adds/Removes imports to Go code for missing imports.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return tuple()
