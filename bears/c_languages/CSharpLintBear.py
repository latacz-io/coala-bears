from coalib.bearlib.abstractions.Linter import Linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@Linter(executable='mcs',
        output_regex=r'(?P<filename>.+\.cs)\((?P<line>\d+),(?P<col>\d+)\): '
                     r'(?P<severity>error|warning) (?P<severity_code>\w+): '
                     r'(?P<message>.+)',
        use_stderr=True,
        severity_map={"warning": RESULT_SEVERITY.NORMAL,
                      "error": RESULT_SEVERITY.MAJOR})
class CSharpLintBear:
    """
    Checks the code with `mcs` on each file separately.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
