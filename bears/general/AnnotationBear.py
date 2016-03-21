from coalib.parsing.StringProcessing.Core import (search_for,
                                                  search_in_between,
                                                  unescaped_search_in_between)
from coalib.bearlib.languages.LanguageDefinition import LanguageDefinition
from coalib.bears.LocalBear import LocalBear
from coalib.results.HiddenResult import HiddenResult
from coalib.results.SourceRange import SourceRange


class AnnotationBear(LocalBear):

    def run(self, filename, file, language: str, language_family: str):
        """
        Finds out all the positions of strings and comments in a file.
        The Bear searches for valid comments and strings and yields their
        ranges as SourceRange objects in HiddenResults.

        :param language:        Language to be whose annotations are to be
                                searched.
        :param language_family: Language family whose annotations are to be
                                searche.
        :return:                HiddenResult with content conatining
                                a tuple of tuples of the form
                                (annotation_start, annotation_end).
        """
        text = ''.join(file)
        lang_dict = LanguageDefinition(language, language_family)

        # Strings
        strings = dict(lang_dict["string_delimiters"])
        strings.update(lang_dict["multiline_string_delimiters"])
        strings_found = find_start_end(text, strings, escape=True)
        # multiline Comments
        comments_found = find_start_end(
                                text,
                                dict(lang_dict["multiline_comment_delimiters"]))
        # single-line Comments
        comments_found += find_singleline_comments(
                                          text,
                                          list(lang_dict["comment_delimiter"]))

        matches_found = strings_found + comments_found
        # Remove Nested
        matches_found = tuple(filter(
                              lambda arg: not in_ranges(matches_found, arg),
                              matches_found))
        # Yield results
        for annotation_found in [strings_found, comments_found]:
            position_range = tuple(AnnotationBear.get_range(text,
                                                            filename,
                                                            matches_found,
                                                            annotation_found))
            yield HiddenResult(self, position_range)

    @classmethod
    def get_range(cls, text, filename, matches_found, annotation_found):
        """
        yields position of valid annotations as SourceRange objects.

        :param text:             A string with all the contents of file.
        :param filename:         Name of file.
        :param matches_found:    All the valid strings and comments found.
        :param annotation_found: All the positions of the given annotation.

        :return:                 SourceRange Objects of all the valid positions
                                 of the annotation.
            """
        for position in set(matches_found) & set(annotation_found):
            yield SourceRange.from_values(
                    filename,
                    start_line=calc_line_col(text,
                                             position[0])[0],
                    start_column=calc_line_col(text,
                                               position[0])[1],
                    end_line=calc_line_col(text,
                                           position[1])[0],
                    end_column=calc_line_col(text,
                                             position[1])[1])


def find_start_end(text, annot, escape=False):
    """
    Gives all positions of annotations which have a start and end.

    :param text:   A string with all the contents of file.
    :param annot:  A dict containing start and end of annotation to be searched.
    :param escape: variable to check wether to ignore escaped annotations

    :return:       A tuple of the form: (annotation_start_position,
                                         annotation_end_position)
    """
    if escape:
        search_func = unescaped_search_in_between
    else:
        search_func = search_in_between
    found_pos = ()
    for annot_type in annot:
        found_pos += tuple(search_func(annot_type, annot[annot_type], text))
    if found_pos:
        found_pos = tuple((i.begin.range[0], i.end.range[1])
                          for i in found_pos)
    return found_pos


def find_singleline_comments(text, comments):
    """
    Finds all single-line comments.

    :param text:      A string with all the contents of file.
    :param comments:  A list contatining different types of
                      single-line comments.

    :return:          A tuple of the form:
                      (single_line_comment_start_position, end_of_line).
    """
    single_comments = []
    for comment_type in comments:
        for found in search_for(comment_type, text):
            start = found.start()
            end = text.find('\n', start)
            end = len(text) + 1 if end == -1 else end
            single_comments.append((start, end))
    return tuple(single_comments)


def in_ranges(outside_ranges, inside_range):
    """
    Finds if a particular range (given by a tuple) is inside a
    collection of given ranges.

    :param outside_ranges: A tuple of tuples of the form (start, end).
    :param inside_range:   A tuple of the form (start, end).

    :return:               True if inside_range is found inside any of the
                           ranges of outside_ranges, else False is returned.
    """
    for outside_range in outside_ranges:
        if inside_range == outside_range:
            continue

        # Special case of python language.
        # Where doc strings (""") and strings (") have a similar start.
        elif inside_range[0] == outside_range[0]:
            if inside_range[1] < outside_range[1]:
                return True

        elif inside_range[0] in range(outside_range[0], outside_range[1]):
            return True
    return False


def calc_line_col(text, pos_to_find):
    """
    Calculate line number and column in the file, from position.

    :param text:        A string with all the contents of file.
    :param pos_to_find: position of character to be found in the
                        line,column form.

    :return:            a tuple of the form (line, column).
    """
    line = 1
    pos = -1
    pos_new_line = text.find('\n')
    while True:
        if pos_new_line == -1:
            return (line, pos_to_find - pos)

        if pos_to_find <= pos_new_line:
            return (line, pos_to_find - pos)

        else:
            line += 1
            pos = pos_new_line
            pos_new_line = text.find('\n', pos_new_line + 1)
