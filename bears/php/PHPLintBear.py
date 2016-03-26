from coalib.bearlib.abstractions.Linter import Linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@Linter(executable='php',
        output_regex=r'(?P<severity>\S+) error: (?P<message>.*) in '
                     r'.* on line (?P<line>\d+)',
        severity_map={'Parse': RESULT_SEVERITY.MAJOR,
                      'Fatal': RESULT_SEVERITY.MAJOR})
class PHPLintBear:
    """
    Checks the code with ``php -l``. This runs it on each file separately.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return ('-l', '-n', '-d', 'display_errors=On', '-d', 'log_errors=Off',
                filename)
