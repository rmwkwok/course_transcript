# Course Transcript Downloader

------

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

------

## About this project
This work uses a modified `coursera-dl` to download courses' syllabuses, in which course structure, course materials' URLs and transcript file URLs are extracted to build markdown files consisting of (1) a Table Of Content and (2) Transcript text.

The [used coursera-dl](https://github.com/rmwkwok/coursera-dl) is a modification to [rawsalt/coursera-dl](https://github.com/rawsalt/coursera-dl) which is a modification to the original [coursera-dl/coursera-dl](https://github.com/coursera-dl/coursera-dl).


## Examples

See created markdown examples [here](https://github.com/rmwkwok/course_transcript/tree/main/examples). Table Of Content may best be used with the "outline feature" of Github: (1) open a markdown, (2) select "Preview" mode which should be the default, (3) at the upper-right corner of the preview box, click the menu button with 3 dots and 3 bars to expand the outline.

## How to use

1. Install. `pipx` is recommended as it creates an isolated environment for this program and its dependencies, avoiding conflicts between programs.

```
pipx install git+https://github.com/rmwkwok/course_transcript.git
```

2. Create a `coursera-dl.conf` file as follow (or found [here](https://github.com/rmwkwok/course_transcript/tree/main/conf_file)) in the working directory that expects to place the created markdown. The CAUTH value is used for authentication to use Coursera's APIs, and may be found in Coursera's site cookies on a successful login. The cookies may be inspected in a web browser.

```
--subtitle-language en
--cauth <your_cauth_here>
```

3. Run the program. For how to specify the program arguments, run `course_transcript --help` and it will return `coursera-dl`'s help message. All arguments are processed by `cousera-dl`. The arguments may be appended to the `coursera-dl.conf` file in the step above.

```
# Below will create one markdown for all courses under the specialization data-analytics.
course_transcript data-analytics --specialization

# Below will create two markdowns for each of the courses.
course_transcript data-analytics-foundations applied-statistics-for-data-analytics
```

4. On complete, markdown file(s) will be available in the working directory, along with a directory named `course_transcript_temp_folder` that is created during the process and may be removed.

## How to develop

1. Clone this repo

```
git clone https://github.com/rmwkwok/course_transcript.git
cd course_transcript
```

2. Setup and activate virtual environment

```
virtualenv course_transcript_venv
source course_transcript_venv/bin/activate
```

3. Install requirements

```
pip install -r requirements.txt
```

## Tested environment

![python][python-shield]




[contributors-shield]: https://img.shields.io/github/contributors/rmwkwok/course_transcript.svg?style=for-the-badge
[contributors-url]: https://github.com/rmwkwok/course_transcript/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/rmwkwok/course_transcript.svg?style=for-the-badge
[forks-url]: https://github.com/rmwkwok/course_transcript/network/members
[stars-shield]: https://img.shields.io/github/stars/rmwkwok/course_transcript.svg?style=for-the-badge
[stars-url]: https://github.com/rmwkwok/course_transcript/stargazers
[issues-shield]: https://img.shields.io/github/issues/rmwkwok/course_transcript.svg?style=for-the-badge
[issues-url]: https://github.com/rmwkwok/course_transcript/issues
[license-shield]: https://img.shields.io/github/license/rmwkwok/course_transcript.svg?style=for-the-badge
[license-url]: https://github.com/rmwkwok/course_transcript/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/rmwkwok
[python-shield]: https://img.shields.io/badge/python-3.10.12-blue.svg?style=for-the-badge
[musictag-url]: https://pypi.org/project/music-tag/