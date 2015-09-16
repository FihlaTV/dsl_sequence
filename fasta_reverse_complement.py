#!/usr/bin/env python
import argparse
import glob
import os.path

from Bio import SeqIO


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""Reverse complement a fasta file
                    """
    )
    parser.add_argument('file_glob', type=str, help="Input fasta glob, e.g. '*fa'")
    parser.add_argument('--output_dir', type=str, default='.', help="Output directory, default: current dir, '.'")
    args = parser.parse_args()

file_list=glob.glob(args.file_glob)
record_list = []
for filename in file_list:
    for rec in SeqIO.parse(filename,'fasta'):
        rec.seq=rec.seq.reverse_complement()
        record_list.append(rec)
    with open(os.path.join(args.output_dir, os.path.basename(filename)), "w") as handle:
        SeqIO.write(record_list, handle, "fasta")

