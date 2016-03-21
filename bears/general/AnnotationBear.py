from coalib.parsing.StringProcessing.Core import (search_for,
                                                  search_in_between,
                                                  unescaped_search_in_between)


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
