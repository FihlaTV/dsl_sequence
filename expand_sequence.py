#!/usr/bin/env python
import argparse
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
    TA [CAG]20 --> [('TA', '', ''),
                    (''), 'CAG', '20')]

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
    AT [AGAT]5 GC --> AT AGAT AGAT AGAT AGAT AGAT GC (spaces for clarity only)

    Rules:
    * All sequences must be bounded by brackets, i.e. [...] or (...)
    * Spaces are ignored
    * Case insensitive
    * Letters: ATCGX (X is taken as an unnatural base by convention)

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

def main(args):
    """ Main function allows script execution with external args.
    Best to use `func:seq_expand()` with external calls.

    Why?: Side-effects...
    * Print to screen
    * Write to file
    """
    seq_struct = [('seq_fwd', seq_expand(args.seq_fwd)),
                  ('seq_repeat', seq_expand(args.seq_repeat)),
                  ('seq_rev', seq_expand(args.seq_rev)),
                 ]

    sequence=''
    for label, seq in seq_struct:
        sequence+=seq

    if args.output_fasta is not None:
        dirname = os.path.dirname(args.output_fasta)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        if args.output_header is None:
            args.output_header = os.path.basename(args.output_fasta)
        rec=SeqRecord.SeqRecord(seq=Seq.Seq(sequence), id=args.output_header, description=str((args.seq_fwd, args.seq_repeat, args.seq_rev)))

        with open(args.output_fasta, "w") as handle:
            SeqIO.write(rec, handle, "fasta")
    else:
        print sequence

if __name__ == '__main__':
    args = parser.parse_args()
    if args.seq_fwd=='' and args.seq_repeat=='' and args.seq_rev=='':
        parser.print_help()
    main(args)

