from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='infer',
        output_regex=r'.+:(?P<line>\d+): (?P<severity>error|warning): '
                     r'(?P<message>.*)')
class InferBear:
    """
    Checks the code with ``infer``.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '-nbp', '--', 'javac', filename
