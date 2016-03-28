from coalib.bearlib.abstractions.Linter import Linter


@Linter(executable='luacheck',
        output_format='regex',
        output_regex=r'\s*.+:(?P<line>\d+):(?P<column>\d+): (?P<message>.+)')
class LuaLintBear:
    """
    Checks the code with ``luacheck``.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
