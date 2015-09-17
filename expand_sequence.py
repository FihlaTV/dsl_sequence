#!/usr/bin/env python
import argparse
import doctest
import glob
import os
import re
import sys

from Bio import Seq, SeqIO, SeqRecord

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
        description="""Generate a fasta file from a sequence specification.

A sequence specification is a condensed way of representing a sequence, e.g.
[AGAT]5 --> AGAT AGAT AGAT AGAT AGAT (CODIS loci CSF1PO, allele)
[TCTA TCTG TCTA] [TCTG]4 [TCTA]3 --> TCTA TCTG TCTA TCTG TCTG TCTG TCTG TCTA TCTA TCTA (CODIS loci VWA, allele 10)
"""
)
group_seq = parser.add_argument_group('Sequences to expand', 'At least one is required, and all written along the complement')
group_seq.add_argument('--seq_fwd', type=str, default="", help="Sequence specfication of the forward flanking region")
group_seq.add_argument('--seq_repeat', type=str, default="", help="Sequence specfication of the repeat")
group_seq.add_argument('--seq_rev', type=str, default="", help="Sequence specfication of the reverse flanking region")

group_output = parser.add_argument_group('Output mode', 'All optional')
group_output.add_argument('--output_fasta', type=str, default=None, help="Output fasta filename, default: None (print to sequence screen (stdout))")
group_output.add_argument('--output_header', type=str, default=None, help="Header of the output fasta file, default: None (same as `output_filename`)")

def _spec_decomposition(seq_specification):
    """ Return a list of tuples decomposing the `seq_specification`.

    For example,
    >>> _spec_decomposition('TA [CAG]20')
    [('TA', '', ''), ('', 'CAG', '20')]

    Assumes that the seq_specification is properly cleaned, and follows
    the 'rules' outlines in func:`seq_expand`
    """
    pattern = re.compile(r'([ATCGX]+)|\[([ATCGX]+)\](\d+)',
                     flags=re.VERBOSE|re.IGNORECASE)
    spec_decomposition=re.findall(pattern, seq_specification)
    return spec_decomposition

def seq_expand(seq_specification):
    """
    Expand a `seq_specification` into a full sequence.

    For example,
    >>> seq_expand('AT [AGAT]5 GC')
    'ATAGATAGATAGATAGATAGATGC'

    or
    >>> seq_expand('AT (CAG)5 GC (GGC)10')
    'ATCAGCAGCAGCAGCAGGCGGCGGCGGCGGCGGCGGCGGCGGCGGCGGC'

    Rules:
    * All sequences must be bounded by brackets, i.e. [...] or (...)
    * Spaces are ignored
    * Case insensitive
    * Letters: ATCGX (X is taken as an unnatural base by convention)

    Nesting is not currently supported, so no:
    >>> seq_expand('AT ( (CAG)5 GC (GGC)10)5')
    'ATCAGCAGCAGCAGCAGGCGGCGGCGGCGGCGGCGGCGGCGGCGGCGGC'

    :param: seq_specification

    :return: seq
    """
    # Remove white space
    # TODO: pyparse
    seq_spec_clean = seq_specification
    seq_spec_clean = re.sub(r'\s*', '', seq_spec_clean)
    seq_spec_clean = re.sub(r'\(', '[', seq_spec_clean)
    seq_spec_clean = re.sub(r'\)', ']', seq_spec_clean)

    # Get decomposed specification
    spec_decomposition = _spec_decomposition(seq_spec_clean)

    # Create a sequence using the `spec_decomposition`
    seq=''
    for bases_nobracket, bases_bracket, count_bracket in spec_decomposition:
        seq+=bases_nobracket
        if count_bracket.isdigit():
            seq+=bases_bracket * int(count_bracket)
    return seq

def write_fasta(sequence, output_fasta, output_header=None):
    """ Write a fasta file """
    dirname = os.path.dirname(output_fasta)
    if not (os.path.isdir(dirname) or dirname==''):
        os.makedirs(dirname)
    if output_header is None:
        output_header = os.path.basename(output_fasta)
    rec=SeqRecord.SeqRecord(seq=Seq.Seq(sequence), id=output_header, description='')
    with open(output_fasta, "w") as handle:
        SeqIO.write(rec, handle, "fasta")
    return True

def seq_from_args(args):
    """ Probably best to use `func:seq_expand()` with external calls.
    Using the args directly is for convenience.

    >>> args = parser.parse_args(['--seq_fwd', '[ATA]2A', '--seq_repeat', '(GGC)11', '--seq_rev', 'AGTATA'])
    >>> seq_from_args(args)
    'ATAATAAGGCGGCGGCGGCGGCGGCGGCGGCGGCGGCGGCAGTATA'
    """
    seq_struct = [('seq_fwd', seq_expand(args.seq_fwd)),
                  ('seq_repeat', seq_expand(args.seq_repeat)),
                  ('seq_rev', seq_expand(args.seq_rev)),
                 ]
    sequence=''
    for label, seq in seq_struct:
        sequence+=seq
    return sequence

if __name__ == '__main__':
    args = parser.parse_args()
    if args.seq_fwd=='' and args.seq_repeat=='' and args.seq_rev=='':
        parser.print_help()
    sequence = seq_from_args(args)

    if args.output_fasta is not None:
        write_fasta(sequence, args.output_fasta, output_header=args.output_header)
    else:
        print sequence

