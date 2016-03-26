import shlex

from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='golint',
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+): (?P<message>.*)')
class GoLintBear:
    """
    Checks the code using ``golint``. This will run golint over each file
    separately.
    """

    @staticmethod
    def create_arguments(filename,
                         file,
                         config_file,
                         golint_cli_options: str=''):
        """
        :param golint_cli_options: Any other flags you wish to pass to golint
                                   can be passed.
        """
        return (tuple(shlex.split(golint_cli_options))
                if golint_cli_options else tuple() + (filename,))
