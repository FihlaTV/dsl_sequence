#!/usr/bin/env python

from distutils.core import setup

setup(name='dslseq',
    version='0.1',
    description=open('README.md').read(),
    author='Ryan M Harrison',
    author_email='ryan.m.harrison@gmail.com',
    url='https://github.com/rmharrison/dsl_sequence',
    scripts=['expand_sequence.py', 'expand_sequence_cfg.py', 'fasta_reverse_complement.py'],
    packages=[''],
    )
