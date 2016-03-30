from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='goimports',
        use_stdin=True,
        output_format='corrected',
        diff_message='Imports need to be added/removed.')
class GoImportsBear:
    """
    Adds/Removes imports to Go code for missing imports.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return ()
