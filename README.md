# covdist
Perform simple coverage profiling of aligned samples. Admittedly this is
a very simple tool, but is quite useful for sequencing center feedback and
topoffs.

Interactive example: https://brwnj.github.io/covdist/

## Note

This is an extension of mosdepth's plot-dist.py script. See:
https://github.com/brentp/mosdepth/blob/master/scripts/plot-dist.py

Here we run `mosdepth` and generate a very similar report.

# Usage

```
nextflow run brwnj/covdist -revision main -profile docker
    --crams '*.cram'
    --reference GRCh38.fasta
    --gaps GRCh38_gaps.bed
```

## Gap info

A simple way to grab this info, to omit region of known gaps in coverage, is
to head over to:

https://genome.ucsc.edu/cgi-bin/hgTables

1. Under `group:` select `Mapping and Sequencing`.
2. For `track:` select `Gap`
3. Set `output format:` as `BED` and define the file name.

## Autosomes

It is likely important for you to get accurate coverage estimates and to
communicate them with your sequencing center. That said, you likely want
to exclude sex chromosomes using:

```
--exclude "decoy,random,chrUn,alt,phix,chrEBV,chrM,chrX,chrY"
```

# Report

Samples can be subset using the "Samples" filter, which is sorted by ascending median coverage.

You can browse covered on each chromosome or all chromosomes under the label "total".

Target coverage cutoff is set dynamically by the user and updates the table. The table
column is sortable and selections on the table can be made to highlight a given sample.
