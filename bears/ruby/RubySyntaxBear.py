from coalib.bearlib.abstractions.Linter import Linter


# TODO Linter: enable multiline mode? or provide an extra field for match flags
@Linter(executable='ruby',
        use_stderr=True,
        output_format='regex',
        output_regex=r'.+?:(?P<line>\d+): (?P<message>.*?'
                     r'(?P<severity>error|warning)[,:] \S+)\s?'
                     r'(?:\S+\s(?P<column>.*?)\^)?')
# TODO See old regex because of the start-anchors, presumably multiline spec
# TODO was assumed
class RubySyntaxBear:
    """
    Checks the code with ``ruby -wc`` on each file separately.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '-wc', filename
