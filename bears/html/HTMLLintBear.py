from coalib.bearlib.abstractions.Linter import Linter
from coalib.settings.Setting import typed_list


@Linter(executable='html_lint.py',
        output_format='regex',
        output_regex=r'(?P<line>\d+):(?P<column>\d+):\s'
                     r'(?P<severity>Error|Warning|Info):\s(?P<message>.+)')
class HTMLLintBear:
    """
    Checks the code with ``html_lint.py`` on each file separately.
    """

    @staticmethod
    def create_arguments(filename, file, config_file,
                         htmllint_ignore: typed_list(str)=[]):
        """
        :param htmllint_include: List of checkers to ignore.
        """
        ignore = ','.join(part.strip() for part in htmllint_ignore)
        return '--disable=' + ignore, filename
