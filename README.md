# A domain-specific language (DSL) for repeatitive DNA sequences

TATAT [CAG]20 [AAT]10 
==> 
TATAT
CAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAG
AATAATAATAATAATAATAATAATAATAAT

## Example: CODIS
The example listed is the complete reference set for the 13 loci of the CODIS panel (Combined DNA Index System).
References sequences crawled from NIST website: http://www.cstl.nist.gov/strbase/fbicore.htm

## Files
### `expand_sequence.py`
Single sequence. 
Output to fasta file or screen

### `expand_sequence_cfg.py`
From a config file

