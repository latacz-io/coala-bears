from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='ruby',
        output_stream='stderr',
        output_format='regex',
        output_regex=r'.+?:(?P<line>\d+): (?P<message>.*?'
                     r'(?P<severity>error|warning)[,:] \S+)\s?'
                     r'(?:\S+\s(?P<column>.*?)\^)?')
class RubySyntaxBear:
    """
    Checks the code with ``ruby -wc`` on each file separately.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '-wc', filename
