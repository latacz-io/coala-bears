from csv import DictReader
from io import StringIO

from coalib.bearlib.abstractions.Linter import Linter
from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


def convert_if_not_empty(value: str, conversion):
    """
    Returns the value converted if it is not None or empty.

    :param value:      The value to convert.
    :param conversion: The conversion callable.
    :return:           None or the converted value.
    """
    if value is not None and value != '':
        return conversion(value)

    return None


@Linter(executable='coffeelint',
        severity_map={'warn': RESULT_SEVERITY.NORMAL,
                      'error': RESULT_SEVERITY.MAJOR})
class CoffeeLintBear(LocalBear, Lint):
    """
    Coffeelint's your files!
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--reporter=csv', filename

    def _process_output(self, output, filename, file):
        reader = DictReader(StringIO("".join(output)))

        for row in reader:
            try:
                yield Result.from_values(
                    origin=self,
                    message=row['message'],
                    file=filename,
                    line=convert_if_not_empty(row['lineNumber'], int),
                    end_line=convert_if_not_empty(row['lineNumberEnd'], int),
                    severity=self.severity_map[row['level']])
            except KeyError:  # Invalid CSV line, ignore
                pass
