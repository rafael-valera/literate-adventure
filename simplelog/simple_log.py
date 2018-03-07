#!/usr/bin/python2
# Description: Command line tool to scan a file entries matching them
# against a given regex and store them in a new file or print them
# to the standard output

import argparse
import re
import sys


def append_to_file(output_file, line):
    """ Appends log entries to output file. If file does not exists
        a new one is made """
    try:
        with open(output_file, mode="a+") as output:
            output.write(line + "\n")
    except IOError as io_error:
        print io_error
        sys.exit(1)


def get_file_entries(filename, pattern):
    """ yield all log entries that match the pattern """
    try:
        with open(filename, 'r') as file_object:
            for log_entry in file_object.readlines():
                matches_pattern = re.search(pattern, log_entry)
                if matches_pattern:
                    yield str.strip(log_entry)
    except IOError as io_error:
        print io_error
        sys.exit(1)


def main():
    options = argparse.ArgumentParser()
    options.add_argument("filename", help="target file", type=str)
    options.add_argument("regex", help="regex pattern matches log entries with regular expressions", type=str)
    options.add_argument("-v", "--verbose", help="outputs matches to the standard output ", action="store_true")
    options.add_argument("-o", "--output", help="destination output file", type=str)
    arguments = options.parse_args()

    try:
        compiled_pattern = re.compile(pattern=arguments.regex, flags=re.IGNORECASE)
    except re.error as re_error:
        print "Regex error: " + re_error.args[0] + ". Used regex: '%s'" % arguments.regex
        sys.exit(1)

    if arguments.verbose and arguments.regex:
        print "Used regex: <%s>" % arguments.regex

    for file_entry in get_file_entries(arguments.filename, compiled_pattern):
        if arguments.output:
            append_to_file(arguments.output, file_entry)
        else:
            print file_entry

        if arguments.verbose:
            print file_entry

    if arguments.output:
        print arguments.output + " has been created."


if __name__ == '__main__':
    main()
