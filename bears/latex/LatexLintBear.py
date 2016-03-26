from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='chktex',
        output_regex=r'(?P<severity>Error|Warning) \d+ in .+ line '
                     r'(?P<line>\d+): (?P<message>.*)')
class LatexLintBear:
    """
    Checks the code with ``chktex``.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
