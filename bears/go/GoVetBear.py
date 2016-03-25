from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='go',
        use_stderr=True,
        output_regex=r'.+:(?P<line>\d+): (?P<message>.*)\n')
class GoVetBear:
    """
    Checks the code using `go vet`.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return 'vet', filename
