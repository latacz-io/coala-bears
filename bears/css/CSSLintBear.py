from coalib.bearlib.abstractions.Linter import Linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@Linter(executable='csslint',
        output_regex=r'(?P<file_name>.+):\s* (?:line (?P<line>\d+), '
                     r'col (?P<col>\d+), )?(?P<severity>Error|Warning) - '
                     r'(?P<message>.*)',
        severity_map={"Error": RESULT_SEVERITY.MAJOR,
                      "Warning": RESULT_SEVERITY.NORMAL})
class CSSLintBear:
    """
    Checks the code with ``csslint``.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--format=compact', filename
