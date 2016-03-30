import autoflake

from coalib.bears.LocalBear import LocalBear


class PyUnusedCodeBear(LocalBear):

    def run(self, filename, file):
        """
        Detects unused code. This functionality is limited to:

        - Unneeded pass statements.
        - Unneeded builtin imports. (Others might have side effects.)
        """
        corrected = autoflake.fix_code(''.join(file)).splitlines(True)

        for diff in Diff.from_string_arrays(file, corrected).split_diff():
            yield Result(self,
                         "This file contains unused source code.",
                         affected_code=(diff.range(filename),),
                         diffs={filename: diff})
