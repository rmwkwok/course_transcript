from setuptools import setup

from course_transcript import __version__

with open('requirements.txt', encoding='utf-8') as f:
    install_requires = f.read()

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='course_transcript',
    packages=['course_transcript'],
    version=__version__,
    install_requires=install_requires,

    license='MIT',
    keywords=['coursera', 'download', 'transcript'],
    description='A downloader for transcripts of courses on Cousera.',
    long_description=long_description,

    url='https://github.com/rmwkwok/course_transcript',
    author='Man Wai Kwok (Raymond)',
    author_email='rmwkwok@gmail.com',

    entry_points=dict(
        console_scripts=[
            'course_transcript=course_transcript.course_transcript:main'
        ]
    ),

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10.12',
    ],
)