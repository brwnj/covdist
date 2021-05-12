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

Under group “Mapping and Sequencing” and track “Gap” at:

https://genome.ucsc.edu/cgi-bin/hgTables

Choose BED as your output format.

## Autosomes

It is likely important for you to get accurate coverage estimates and to
communicate them with your sequencing center. That said, you likely want
to exclude sex chromosomes using:

```
--exclude "decoy,random,chrUn,alt,chrEBV,chrM,chrX,chrY"
```

# Report

Samples can be subset using the "Samples" filter, which is sorted by ascending median coverage.

You can browse covered on each chromosome or all chromosomes under the label "total".

Target coverage cutoff is set dynamically by the user and updates the table. The table
column is sortable and selections on the table can be made to highlight a given sample.
