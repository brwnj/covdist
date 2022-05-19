nextflow.enable.dsl=2

params.help = false
if (params.help) {
    log.info """
    -----------------------------------------------------------------------

    covdist
    ===========

    Documentation and issues can be found at:
    https://github.com/brwnj/covdist

    Required arguments:
    -------------------
    --crams               Aligned sequences in .bam and/or .cram format.
                          Indexes (.bai/.crai) must be present.
    --reference           Reference FASTA. Index (.fai) must exist in same
                          directory.
    --gaps                Regions of known gaps in .bed format.

    Options:
    --------
    --outdir              Base results directory for output.
                          Default: '/.results'
    --exclude             Chromosomes to exclude as comma separated string.
                          Default: 'decoy,random,chrUn,alt,chrEBV,chrM'
    --cpus                Number of cpus dedicated to `mosdepth` calls.
                          Default: 4

    -----------------------------------------------------------------------
    """.stripIndent()
    exit 0
}

params.crams = false
params.reference = false
params.gaps = false
params.outdir = './results'
params.cpus = 4

params.idx = false

if(!params.crams) {
    exit 1, "--crams argument like '/path/to/*.cram' is required"
}
if(!params.reference) {
    exit 1, "--reference argument is required"
}
if(!params.gaps) {
    exit 1, "--gaps argument is required"
}

if(!params.idx) {
    idx = path("${params.reference}.fai")
} else {
    idx = path(params.idx)
}
if( !idx.exists() ) exit 1, "Missing reference index: ${idx}"


crams = channel.fromPath(params.crams)
crais = crams.map { it -> it + ("${it}".endsWith('.cram') ? '.crai' : '.bai') }
exclude = params.exclude.tokenize(",")
chroms = channel
    .fromPath("${params.reference}.fai")
    .splitCsv(sep: "\t", strip: true)
    .map { row -> "${row[0]}" }
    .filter( ~/(?!${exclude.collect {".*$it.*"}.join("|")})([a-zA-Z0-9_]+)/ )

process makebed {
    input:
    val chrs
    path(reference)

    output:
    path("include.bed"), emit: bed

    script:
    template "makebed.py"
}

process bedtools {
    input:
    path(genome)
    path(gaps)

    output:
    path("include_gaps.bed"), emit: bed

    script:
    """
    bedtools subtract -a ${genome} -b ${gaps} > include_gaps.bed
    """
}

process mosdepth {
    publishDir "${params.outdir}/mosdepth", mode: "copy"
    cpus params.cpus

    input:
    path(cram)
    path(crai)
    path(reference)
    path(bed)

    output:
    path("*global.dist.txt"), emit: txt

    script:
    """
    mosdepth -f ${reference} -b ${bed} -n -x -t ${task.cpus} ${cram.getSimpleName()} ${cram}
    """
}

process covdist {
    publishDir params.outdir, mode: "copy"

    input:
    path(txts)

    output:
    path("covdist.html"), emit: html

    script:
    template "covdist.py"
}

workflow {
    makebed(chroms.collect(), idx)
    bedtools(makebed.output.bed, params.gaps)
    mosdepth(crams, crais, params.reference, bedtools.output.bed)
    covdist(mosdepth.output.txt.collect())
}
