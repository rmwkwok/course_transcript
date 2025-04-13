import os
import sys
import json
import time
import shutil
import logging
import requests
import functools
import contextlib
from enum import IntEnum, auto

from coursera import coursera_dl, commandline


# For escaping listed markdown special characters in transcript
ESCAPE = str.maketrans({c: f'\\{c}' for c in '''\\`*_{}[]<>()#+-.!|$'''})


class Lv(IntEnum):
    SPECIALIZATION = auto()
    COURSE = auto()
    MODULE = auto()
    LESSON = auto()
    MATERIAL = auto()


class Markdown:
    toc: str = '# Table of content\n'
    transcript: str = '# Transcripts\n'

    def add_level(self, lv: Lv, text: str) -> None:
        '''Add indented bullet point for TOC and header for transcript.

        Args:
            lv: Lv
                A level object on which the indentation and heading
                levels are based
            text: str
                The text for content and header
        '''
        if lv < Lv.LESSON:
            fmt_toc = '#' * (lv + 1) + ' '
        else:
            fmt_toc = ' ' * (lv - Lv.LESSON) * 2 + '- '

        fmt_transcript = ' ' * (lv - 1) * 2 + '- '

        self.toc += f'{fmt_toc}{text}\n'
        self.transcript += f'{fmt_transcript}{text}\n'

    def add_transcript(self, text: str)-> None:
        '''Add transcript.

        Args:
            text: str
                Transcript text
        '''
        text = text.translate(ESCAPE).replace('\n', ' ')
        indent = ' ' * (Lv.MATERIAL - 1) * 2 + '  '
        self.transcript += f'\n{indent}{text}\n'

    @property
    def output(self) -> str:
        return self.toc + self.transcript


_enumerate = functools.partial(enumerate, start=1)


@contextlib.contextmanager
def tempdir() -> contextlib.AbstractContextManager[str]:
    '''A context manager that creates a temporary folder and change the
    current working directory to it.'''

    # Remember the current working directory and under which create a
    # temporary directory that will be switched into
    curr_wd = os.getcwd()
    temp_wd = os.path.join(curr_wd, 'course_transcript_temp_folder')

    if not os.path.exists(temp_wd):
        os.mkdir(temp_wd)

    # Copy conf file to the temporary directory for use by coursera-dl
    curr_conf = commandline.LOCAL_CONF_FILE_NAME
    temp_conf = os.path.join(temp_wd, commandline.LOCAL_CONF_FILE_NAME)

    if os.path.isfile(curr_conf):
        shutil.copyfile(curr_conf, temp_conf)

    try:
        # Change to the temporary directory
        os.chdir(temp_wd)
        yield curr_wd

    finally:
        # Revert back to the original working directory
        os.chdir(curr_wd)


def parse_syllabus(
        md: Markdown,
        course_num: int | None,
        course_slug: str,
    ) -> None:
    '''Parse the `course_slug`'s syllabus JSON file into markdown text.

    Args:
        md: Markdown
            `Markdown` object to add parsed syllabus text into
        course_num: int | None
            Course number. Expect `None` if the course does not belong
            to a specialization
        course_slug: str
            Course slug
    '''

    # Load syllabus json downloaded by coursera-dl
    with open(f'{course_slug}-syllabus-parsed.json', 'r') as f:
        syllabus = json.loads(f.read())
        # disregard the Resources section, or it causes error when unpacking
        # in the first loop below because it has only 2 elements to unpack
        syllabus = filter(lambda m: m[0] != 'Resources', syllabus)

    # Add course level
    c_alias = f'C{course_num}' if course_num else ''
    title = (f'{c_alias}: ' if course_num else '') + course_slug
    md.add_level(Lv.COURSE, title)

    for m_num, (m_slug, modules, m_data) in _enumerate(syllabus):
        # Add module level
        alias = f'{c_alias}M{m_num}'
        md.add_level(Lv.MODULE, f'{alias}: {m_data["name"]}')

        for l_num, (l_slug, lessons, l_data) in _enumerate(modules):
            # Add lesson level
            alias = f'{c_alias}M{m_num}L{l_num}'
            md.add_level(Lv.LESSON, f'{alias}: {l_data["name"]}')

            for ma_num, (ma_slug, materials, ma_data) in _enumerate(lessons):
                # Add material level
                url = '/'.join((
                    'https://www.coursera.org/learn',
                    course_slug,
                    ma_data['type_name'],
                    ma_data['id'],
                    ma_data['slug'],
                ))
                title = f'{alias}: {ma_data["name"]}'
                md.add_level(Lv.MATERIAL, f'[{title}]({url})')

                # Add transcript
                for key, val in materials.items():
                    if key[-4:] != '.txt': # identifier for transcript
                        continue

                    logging.info(f'Getting transcript for {title}')

                    transcript_url = val[0][0]
                    if (r := requests.get(transcript_url)).status_code == 200:
                        md.add_transcript(r.text)
                        continue

                    logging.warning(f'[X] Failed. URL = {transcript_url}')


def main():

    with tempdir() as curr_wd:

        # limits coursera-dl to only download syllabus
        sys.argv.append('--only-syllabus')

        # get arguments
        args = commandline.parse_args()

        # Get syllabus
        # if --specialization is specified in arguments and any of the class
        #     names is a specialization, 'specialization.coursera-dl.jsonl'
        #     will be created to store the specialization's course names sorted
        #     by their course numbers.
        # Each course's syllabus will be stored as
        #     f'{course_name}-syllabus-parsed.json'
        coursera_dl.main()
        logging.info('Syllabuses downloaded. Starting to get transcripts...')

        # Load specializations' ordered course slugs for identifying
        # which class_name is specialization, what courses are included, and
        # the ordering of the courses in specialization
        course_slugs = {}
        if os.path.isfile(path := 'specialization.coursera-dl.jsonl'):
            with open(path, 'r') as f:
                for _json in map(json.loads, f.read().splitlines()):
                    course_slugs.update(_json)

        for name in args.class_names:
            # Create a markdown per class_name
            md = Markdown()

            # Prepare courses to be parsed. Specialization and course are
            # treated differently
            if args.specialization and (c_slugs := course_slugs.get(name)):
                md.add_level(Lv.SPECIALIZATION, name)
                c_slugs = _enumerate(c_slugs)

            else:
                c_slugs = [(None, name)]

            # Parse syllabuses course by course
            for course_num, course_slug in c_slugs:
                # Sleep
                logging.info(
                    'Sleeping for %d seconds before downloading next course. '
                    'You can change this with --download-delay option.',
                    args.download_delay
                )
                time.sleep(args.download_delay)

                parse_syllabus(md, course_num, course_slug)

            # Save markdown
            with open(f'{os.path.join(curr_wd, name)}.md', 'w') as f:
                f.write(md.output)


if __name__ == '__main__':
    main()

