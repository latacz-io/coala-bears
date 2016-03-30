from os.path import abspath, dirname, join

from coalib.bearlib.abstractions.Linter import Linter


jar = join(dirname(abspath(__file__)), 'scalastyle.jar')
scalastyle_config_file = join(dirname(abspath(__file__)),
                              'scalastyle_config.xml')


@Linter(executable='java',
        output_format='regex',
        output_regex=r'(?P<severity>warning) file=.+ message=(?P<message>.+) '
                     r'line=(?P<line>\d+)(?: column=(?P<column>\d+))?',
        prerequisite_check_command=('java', '-jar', jar, '-c',
                                    scalastyle_config_file, '.', '-q', 'true'),
        prerequisite_check_fail_message='Required jar file ' + jar +
                                        ' not found.')
class ScalaLintBear:
    """
    Checks the code with ``scalastyle`` on each file separately.
    """

    @staticmethod
    def create_arguments(filename, file, config_file,
                         scalalint_config: str=""):
        """
        :param scalalint_config: Path to a custom configuration file.
        """
        style_config = scalalint_config or scalastyle_config_file
        return '-jar', jar, filename, '--config', style_config
