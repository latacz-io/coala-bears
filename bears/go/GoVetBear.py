from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='go',
        output_stream='stderr',
        output_format='corrected',
        output_regex=r'.+:(?P<line>\d+): (?P<message>.*)')
class GoVetBear:
    """
    Checks the code using ``go vet``.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return 'vet', filename
