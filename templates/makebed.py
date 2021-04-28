#!/usr/bin/env python

include = "$chrs".replace("[", "").replace("]", "").replace(" ", "").split(",")
ref = "$reference"

with open(ref) as ifh, open("include.bed", "w") as ofh:
    for line in ifh:
        toks = line.strip().split("\\t")
        if toks[0] in include:
            print(toks[0], 0, toks[1], sep="\\t", file=ofh)
