import json

from coalib.bearlib.abstractions.Linter import Linter
from coalib.results.Result import Result


@Linter(executable='dockerfile_lint')
class DockerfileLintBear:
    """
    Checks the given file with ``dockerfile_lint``.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--json', '-f', filename

    def process_output(self, output, filename, file):
        output = json.loads("".join(output))

        for severity in output:
            if severity == "summary":
                continue
            for issue in output[severity]["data"]:
                yield Result.from_values(
                    origin=self,
                    message=issue["message"],
                    file=filename,
                    severity=self.severity_map[issue["level"]],
                    line=issue["line"])
