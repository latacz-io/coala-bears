from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='shellcheck',
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+): '
                     r'(?P<severity>error|warning|info): (?P<message>.+)')
class ShellCheckBear:
    """
    Checks the given code with ``shellcheck``.
    """

    @staticmethod
    def create_arguments(filename, file, config_file, shell: str='sh'):
        """
        :param shell: Target shell being used.
        """
        return '--f', 'gcc', '-s', shell, filename
