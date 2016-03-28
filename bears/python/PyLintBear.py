import os
import shlex

from coalib.bearlib.abstractions.Linter import Linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Setting import typed_list


@Linter(executable='pylint',
        output_format='regex',
        output_regex=r'(?P<line>\d+)\.(?P<column>\d+)\|'
                     r'(?P<severity>[WFECRI]): (?P<message>.*)',
        severity_map={'F': RESULT_SEVERITY.MAJOR,
                      'E': RESULT_SEVERITY.MAJOR,
                      'W': RESULT_SEVERITY.NORMAL,
                      'C': RESULT_SEVERITY.INFO,
                      'R': RESULT_SEVERITY.INFO,
                      'I': RESULT_SEVERITY.INFO})
class PyLintBear:
    """
    Checks the code with pylint. This will run pylint over each file
    separately.
    """

    @staticmethod
    def create_arguments(filename, file, config_file,
                         pylint_disable: typed_list(str)=None,
                         pylint_enable: typed_list(str)=None,
                         pylint_cli_options: str="",
                         pylint_rcfile: str=""):
        """
        :param pylint_disable:     Disable the message, report, category or
                                   checker with the given id(s).
        :param pylint_enable:      Enable the message, report, category or
                                   checker with the given id(s).
        :param pylint_cli_options: Any command line options you wish to be
                                   passed to pylint.
        :param pylint_rcfile:      The rcfile for PyLint.
        """
        args = ('--report=n', '--persistent=n',
                '--msg-template="{line}.{column}|{C}:{msg_id} - {msg}"')
        if pylint_disable:
            args += ('--disable=' + ','.join(pylint_disable),)
        if pylint_enable:
            args += ('--enable=' + ','.join(pylint_enable),)
        if pylint_cli_options:
            args += tuple(shlex.split(pylint_cli_options))
        if pylint_rcfile:
            args += '--rcfile=' + pylint_rcfile
        else:
            args += '--rcfile=' + os.devnull

        return args + (filename,)
