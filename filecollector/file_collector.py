# /usr/bin/python3

"""
    File collector walks through a given directory tree finding given file
    formats and stores it in a zip file.

    Copyright (C) 2017 rafael valera

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import os
import sys
import warnings
import zipfile

docs = (".txt", ".doc", ".xls", ".xlsx", ".docx", ".pdf", ".odt")
videos = ('.m1v', '.mpeg', '.mov', '.qt', '.mpa', '.mpg', '.mpe', '.avi', '.movie', '.mp4')
audios = ('.ra', '.aif', '.aiff', '.aifc', '.wav', '.au', '.snd', '.mp3', '.mp2')
images = ('.ras', '.xwd', '.bmp', '.jpe', '.jpg', '.jpeg', '.xpm', '.ief', '.pbm',
          '.tif', '.gif', '.ppm', '.xbm', '.tiff', '.rgb', '.pgm', '.png', '.pnm')


class CollectedFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.filename = os.path.basename(file_path)
        self.extension = os.path.splitext(file_path)

    def get_absolute_file_path(self):
        return self.file_path

    def get_file_extension(self):
        return self.extension

    def get_filename(self):
        return self.filename

    def __str__(self):
        return "<MediaFile: {}>".format(self.filename)


def append_to_zipfile(container, file, verbose=False):
    """
        Appends file to zipfile. If verbose, prints the filename
        lto the standard output stream

        :param container: zip file full path
        :param file: file to be added
        :param verbose: if true, prints '.../{filename}' to stdout

    """
    append = "a"
    with warnings.catch_warnings():
        try:
            warnings.simplefilter("ignore")
            with zipfile.ZipFile(container, append) as temp_zipfile:
                temp_zipfile.write(file.get_absolute_file_path(), file.get_filename())
        except FileNotFoundError as not_found_exception:
            print(not_found_exception, file=sys.stderr)
            sys.exit(1)
        else:
            if verbose:
                print("..." + file, file=sys.stdout)


def collect_files(src, file_extensions):
    """
        Walks through source file tree and yields a CollectedFile object
        that meets the file extensions criteria. If source directory does
        not exists, a FileNotFoundError exception is raised and if the
        argument file_extensions is not a tuple a TypeError exception will
        be raised

        Params:
        :param src: a source directory to collect files from
        :param file_extensions: a tuple of file extensions (.txt, .xls, .jpeg)

        yields: CollectedFile object
    """
    if not os.path.exists(src):
        raise FileNotFoundError()

    if not isinstance(file_extensions, tuple):
        raise TypeError()
    else:
        for path, dirs, files in os.walk(src):
            for file in files:
                if file.lower().endswith(file_extensions):
                    yield CollectedFile(os.path.join(path, file))


def main():
    flags_parser = argparse.ArgumentParser(description="Collects files by extension and stores it in a zip file")

    flags_parser.add_argument("source", help="source directory to collect files from", type=str)
    flags_parser.add_argument("--verbose", "-v", help="prints to stdout the files being appended to the zipfile",
                              action="store_true", default=False)
    flags_parser.add_argument("--media", "-m", help="includes most commom media file extensions to the search criteria",
                              action="store_true", default=False)
    flags_parser.add_argument("zipfile", help="/path/to/my_file.zip ", type=str)
    flags_parser.add_argument("extensions", help="file extensions to be added to the search criteria ex: txt pdf jpeg"
                                                 "png wav", type=tuple, nargs="*")

    # Arguments
    arguments = flags_parser.parse_args()
    source = arguments.source
    is_verbose = arguments.verbose
    zip_file_path_container = arguments.zipfile
    media = arguments.media
    program_extensions = tuple(audios + images + docs + videos)
    user_extensions = tuple(["".join(ext) for ext in arguments.extensions])

    if media:
        all_extensions = program_extensions + user_extensions
    else:
        all_extensions = tuple(["".join(ext) for ext in arguments.extensions])

    for collected_file in collect_files(source, all_extensions):
        append_to_zipfile(zip_file_path_container, collected_file.get_absolute_file_path(), is_verbose)


if __name__ == "__main__":
    main()
