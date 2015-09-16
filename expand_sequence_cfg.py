#!/usr/bin/env python
import argparse
import ConfigParser
import glob
import os
import re
import sys

from Bio import Seq, SeqIO, SeqRecord

import expand_sequence

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
description="""Generate a list of reference sequences from a config file

Format...
    [DEFAULT]
    seq_fwd = ...
    seq_ref = ...
    loci_name = ...

    [1] # Alele 1
    seq_repeat = ...

    [2] # Alele 2
    seq_repeat = ...

    ...
    [N] # Alele N
    seq_repeat = ...

where `seq_fwd`, `seq_rev` and `seq_repeat` are any expanded or unexpanded (see `expand_sequence.py`) sequence string
            """
)
parser.add_argument('config_file', type=str, help="Config file")
parser.add_argument('--output_dir', type=str, default='ref', help="Output folder")

if __name__ == '__main__':
    args = parser.parse_args()
    if not os.path.isfile(args.config_file):
        raise Exception("File does not exist: {}".format(args.config_file))

    config = ConfigParser.ConfigParser()
    config.read(args.config_file)

    seq_fwd = config.get('DEFAULT', 'seq_fwd')
    seq_rev = config.get('DEFAULT', 'seq_rev')
    loci_name = config.get('DEFAULT', 'loci_name')

    for allele in config.sections():
        seq_repeat = config.get(allele, 'seq_repeat')
        output_header = "REF_{}_{}".format(loci_name, allele)
        expand_sequence_args = expand_sequence.parser.parse_args([
                                                  '--seq_fwd', seq_fwd, 
                                                  '--seq_repeat', seq_repeat, 
                                                  '--seq_rev', seq_rev,
                                                  '--output_fasta', os.path.join(args.output_dir, "{}.fasta".format(output_header)),
                                                  '--output_header', output_header])
        expand_sequence.main(expand_sequence_args)
