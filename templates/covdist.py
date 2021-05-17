#!/usr/bin/env python

import itertools as it
import json
import os
from collections import defaultdict
from operator import itemgetter


TEMPLATE = """<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8" />
    <meta name="author" content="Joe Brown" />
    <title>covdist</title>

    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.14.0/css/all.min.css" rel="stylesheet">
    <link href="https://raw.githack.com/ttskch/select2-bootstrap4-theme/master/dist/select2-bootstrap4.css" rel="stylesheet">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/css/select2.min.css">
    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/selectize.js/0.12.6/css/selectize.bootstrap3.min.css">
    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.13.12/css/bootstrap-select.min.css" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/dc/3.1.9/dc.min.css" rel="stylesheet" type="text/css" />

    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/js/select2.min.js"></script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/selectize.js/0.12.6/js/standalone/selectize.min.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/d3/5.15.0/d3.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/crossfilter2/1.5.2/crossfilter.min.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/dc/3.1.9/dc.min.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.13.12/js/bootstrap-select.min.js"></script>

    <script type="text/javascript"
    src="https://cdn.datatables.net/v/bs4/dt-1.10.20/b-1.6.1/b-colvis-1.6.1/b-html5-1.6.1/cr-1.5.2/r-2.2.3/rg-1.1.1/sc-2.0.1/sp-1.0.1/sl-1.3.1/datatables.min.js"></script>
    <link rel="stylesheet" type="text/css"
    href="https://cdn.datatables.net/v/bs4/dt-1.10.20/b-1.6.1/b-colvis-1.6.1/b-html5-1.6.1/cr-1.5.2/r-2.2.3/rg-1.1.1/sc-2.0.1/sp-1.0.1/sl-1.3.1/datatables.min.css" />

    <style type="text/css">

        body {
            height: 100%;
            margin: 0px;
            padding: 0px;
        }

        .brand {
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.8rem;
        }

        .filter-option {
            width: unset !important;
        }

        .form-control.dropdown-toggle {
            border-top-left-radius: 0rem !important;
            border-bottom-left-radius: 0rem !important;
        }

        #sample-select {
            width: 400px;
        }

        small {
            padding-left: 1rem !important;
        }

        table.dataTable thead th.sorting:after,
        table.dataTable thead th.sorting_asc:after,
        table.dataTable thead th.sorting_desc:after,
        table.dataTable thead th.sorting:before,
        table.dataTable thead th.sorting_asc:before,
        table.dataTable thead th.sorting_desc:before {
            font-family: FontAwesome !important;
        }

        .table-xsm {
            font-size: .8rem;
        }

        #cutoff-select {
            width: 80px !important;
        }
    </style>
</head>

<body>
    <nav class="navbar navbar-light bg-light border-bottom mx-0 p-1">
        <a class="navbar-brand brand text-decoration-none p-0 pl-2" href="https://github.com/brwnj/covdist">covdist</a>

        <form class="form-inline flex-nowrap my-2 my-lg-0" id="chromosome-ux-form">

            <div class="input-group flex-nowrap pr-2">
                <div class="input-group-prepend">
                    <span class="input-group-text">Samples</span>
                </div>
                <div class="" id="sample-select"></div>
            </div>

            <div class="input-group flex-nowrap pr-2">
                <div class="input-group-prepend">
                    <span class="input-group-text d-none d-xl-block">Chromosome</span>
                    <span class="input-group-text d-xl-none">Chr</span>
                </div>
                <select class="form-control" id="region-select"></select>
                <div class="input-group-append">
                    <button class="btn btn-primary" type="button" id="btn-previous" title="Previous region (&#8592;)"
                        data-toggle="tooltip"><i class="fas fa-caret-left"></i></button>
                </div>
                <div class="input-group-append">
                    <button class="btn btn-primary" type="button" id="btn-next" title="Next region (&#8594;)"
                        data-toggle="tooltip"><i class="fas fa-caret-right"></i></button>
                </div>
            </div>

            <div class="input-group flex-nowrap pr-2">
                <div class="input-group-prepend">
                    <span class="input-group-text">Target</span>
                </div>
                <input class="form-control" id="cutoff-select" type="number" value="30" min="0" max="10000" step="1"/>
            </div>
            <span class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button"
                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <span><i class="fas fa-download"></i></span>
                </a>
                <div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdown">
                    <h6 class="dropdown-header" id="download-preview"></h6>
                    <a class="dropdown-item" id="download-csv">CSV</a>
                    <a class="dropdown-item" id="download-copy">Copy</a>
                </div>
            </span>
        </form>

    </nav>

    <main role="main" class="container-fluid">
        <div class="row pr-4">
            <div class="col-12" id="dist-plot"></div>
        </div>
        <div class="row px-1 h-100 mb-4">
            <div class="col-12">
                <div class="table-responsive">
                    <table id="dist-table" class="table table-hover table-striped table-sm table-xsm table-bordered"
                        width="100%">
                    </table>
                </div>
            </div>
        </div>
    </main>
</body>

<script>
    const data = {{data}}
    let ndx = crossfilter(data.v50)
    let sample_select = dc.selectMenu("#sample-select")
    const colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf", "#7CB5EC", "#434348", "#90ED7D", "#F7A35C", "#8085E9", "#F15C80", "#E4D354", "#2B908F", "#F45B5B", "#91E8E1", "#4E79A7", "#F28E2C", "#E15759", "#76B7B2", "#59A14F", "#EDC949", "#AF7AA1", "#FF9DA7", "#9C755F", "#BAB0AB"]
    const sample_colors = (arr) => {
        let cols = {}
        for (const [i, sample] of arr.entries()) {
            cols[sample] = colors[i % colors.length]
        }
        return cols
    }
    const color_map = sample_colors(data.v50.map(i => {return i.sample}))
    let dist_table

    const add_proportion_data = (arr) => {
        let a = []
        let chr = \$('#region-select').find(':selected')[0].text
        let cutoff = parseInt(\$('#cutoff-select').val())

        arr.forEach(function (sample_obj) {
            let sample = sample_obj.sample

            let x_idx = data[chr][sample_obj.sample]["x"].indexOf(cutoff)
            let i = 0
            // occasionally x proportions have to be shifted slightly
            while (x_idx == -1 && i < 10) {
                i += 1
                x_idx = data[chr][sample_obj.sample]["x"].indexOf(cutoff + i)
            }

            let v;
            try {
                v = data[chr][sample_obj.sample]["y"][x_idx]
            } catch (err) {
                v = 0
            }

            a.push({
                sample: sample_obj.sample,
                v50: sample_obj.v50,
                proportion: v||0,
            })
        })
        return a
    }

    const update_table = (arr) => {
        reset_dist_plot()
        dist_table.clear()
        let chr = \$('#region-select').find(':selected')[0].text
        let cutoff = parseInt(\$('#cutoff-select').val())
        arr = add_proportion_data(arr)
        dist_table.rows.add(arr)
        \$( dist_table.column( 2 ).header() ).text( `Proportion of Bases (on \${chr}) >= \${cutoff}` )
        dist_table.draw()
    }

    const build_table = (arr) => {
        let cutoff = parseInt(\$('#cutoff-select').val())

        let cols = [
            {data: "sample", title: "Sample"},
            {data: "v50", title: "Median"},
            {data: "proportion", title: `Proportion of Bases (on total) >= \${cutoff}`},
        ]

        // add proportion data
        arr = add_proportion_data(arr)
        dist_table = \$("#dist-table").DataTable({
            data: arr,
            columns: cols,
            deferRender: true,
            scrollY: '600px',
            scrollX: true,
            // responsive: true,
            scrollCollapse: true,
            scroller: true,
            info: true,
            colReorder: true,
            buttons: [
                'copyHtml5', 'csvHtml5'
            ],
            dom: 'rt<"clear">',
            columnDefs: [
                {
                    targets: '_all',
                    render: function (d, type, row) {
                        if (type === 'display' && d != null) {
                            if (typeof d != "string") {
                                return d
                            }
                            d = d.replace(/<(?:.|\\\\n)*?>/gm, '')
                            if (d.length > 40) {
                                return `<span class="show-ellipsis" title="\${d}">\${d.substr(0, 40)}</span><span class="no-show">\${d.substr(40)}</span>`
                            } else {
                                return d
                            }
                        } else {
                            return d
                        }
                    }
                }
            ],
            infoCallback: (oSettings, iStart, iEnd, iMax, iTotal, sPre) => {
                \$("#download-preview").html(`Download \${iTotal} records as:`)
            },
            searching: true,
            lengthChange: false,
            // order: [[0, 'asc'], [1, 'asc']],
            order: [[2, 'asc']],
        })

        // register table clicks
        dist_table.on('click', 'tr', function () {
            if (\$(this).hasClass('selected')) {
                dist_table.\$('tr.selected').removeClass('selected')
                reset_dist_plot()
            }
            else {
                dist_table.\$('tr.selected').removeClass('selected')
                \$(this).addClass('selected')
                let sample_id = dist_table.rows('.selected').data()[0]["sample"]
                highlight_plot_traces(sample_id)
            }
        })
    }

    function remove_empty_bins(source_group) {
        return {
            all: function () {
                return source_group.all().filter(function (d) {
                    return d.value != 0
                })
            }
        }
    }

    // https://jsfiddle.net/gordonwoodhull/g34Ldwaz/8/
    // https://github.com/dc-js/dc.js/issues/348
    function index_group(group) {
        return {
            all: function () {
                return group.all().map(function (kv, i) {
                    return { key: i, value: kv.value }
                })
            }
        }
    }

    const build_filters = () => {
        let chr = \$('#region-select').find(':selected')[0].text
        let all = ndx.groupAll()
        let colors = { rows: d3.scaleOrdinal().range(["#ff7f0e"]) }

        let dim = ndx.dimension((d) => { return d["sample"] })
        let group = dim.group().reduceCount()
        let nonempty = remove_empty_bins(group)

        sample_select
            .dimension(dim)
            .group(nonempty)
            .multiple(true)
            .promptText('All')
            .controlsUseVisibility(true)
            .title(d => d.key)
            .order((a, b) => {
                let av = data.total[a.key].v50
                let bv = data.total[b.key].v50
                return bv < av ? 1 : av < bv ? -1 : 0
            })
            .on("postRender", function (e) {
                // for each option within this menu, update the value and
                var opts = \$("#sample-select.dc-chart select.dc-select-menu option.dc-select-option")
                for (let i=0; i < opts.length; ++i) {
                    let k = opts[i].text
                    opts[i].setAttribute("data-subtext", `v50: \${data.total[k].v50}`)
                }
                \$("#sample-select .dc-select-menu").selectpicker({
                    header: false,
                    liveSearch: true,
                    liveSearchStyle: "startsWith",
                    liveSearchPlaceholder: "Search",
                    actionsBox: true,
                    selectedTextFormat: "count > 2",
                    style: "",
                    styleBase: "form-control",
                    width: "100%",
                })
                draw_dist(e.dimension().top(Infinity))
                build_table(e.dimension().top(Infinity))
            })
            .on("postRedraw", function () {
                \$("#sample-select .dc-select-menu").selectpicker("refresh")
            })
            .on("filtered", function (e) {
                try {
                    // active filters
                    draw_dist(e.dimension().top(Infinity))
                    update_table(e.dimension().top(Infinity))
                } catch (err) {
                    // filters were reset
                    draw_dist(e.dimension().allFiltered())
                    update_table(e.dimension().allFiltered())
                }
            });

        dc.renderAll()
    }

    \$('#region-select').on("change", () => {
        draw_dist(sample_select.dimension().top(Infinity))
        update_table(sample_select.dimension().top(Infinity))
    })

    \$('#cutoff-select').on("change", () => {
        // draw_dist(sample_select.dimension().top(Infinity))
        update_table(sample_select.dimension().top(Infinity))
    })

    \$("#region-select").select2({
        data: data.chroms.map(i => {
            return { id: i, text: i }
        }),
        selectOnClose: true,
        width: 140,
        theme: 'bootstrap4',
    })

    const draw_dist = (arr) => {
        let traces = []
        let chr = \$('#region-select').find(':selected')[0].text
        arr.forEach(function (sample_obj) {
            let sample = sample_obj.sample
            traces.push({
                x: data[chr][sample]["x"],
                y: data[chr][sample]["y"],
                type: "scatter",
                mode: "lines",
                name: sample,
                marker: { "color": color_map[sample] },
            })
        })
        let layout = {
            showlegend: true,
            height: 500,
            hovermode: "closest",
            hoverlabel: {namelength :-1},
            xaxis: {
                title: "Coverage",
                showline: false,
                showgrid: false,
                showticklabels: true,
                zeroline: false,
            },
            yaxis: {
                title: "Proportion of bases at coverage",
                showline: true,
            },
            margin: {
                autoexpand: true,
                t: 20,
            },
        };


        let p = document.getElementById("dist-plot")
        Plotly.react(p, traces, layout, {displayModeBar: false})

        p.removeAllListeners("plotly_doubleclick")
        p.on("plotly_doubleclick", reset_dist_plot)
    }

    const highlight_plot_traces = (sample) => {
        let d = document.getElementById("dist-plot")
        let vals = d.data.map((t, i) => {
            if (sample == "") {
                return [1, 2]
            }
            if (t.name == sample) {
                return [1, 2]
            } else {
                return [0.15, 0.36]
            }
        })

        Plotly.restyle(d, {'opacity': vals.map(i => i[0]), 'line.width': vals.map(i => i[1])})
    }

    const reset_dist_plot = () => {
        dist_table.\$('tr.selected').removeClass('selected')
        highlight_plot_traces("")
    }

    document.addEventListener("keydown", function (e) {
        // allow cursor nav inside input elements
        if (document.activeElement.tagName.toLowerCase() == "input") {
            return
        }
        if (e.which == 37) {
            next_region(-1)
        } else if (e.which == 39) {
            next_region()
        } else {
            return
        }
    })

    const next_region = (offset = 1) => {
        let chr = \$('#region-select').find(':selected')[0].text
        let selected_index = data.chroms.indexOf(chr)
        let next_index
        // previous
        if (offset == -1) {
            if (selected_index == 0) {
                next_index = data.chroms.length - 1
            } else {
                next_index = selected_index - 1
            }
        } else {
            if (selected_index == data.chroms.length - 1) {
                next_index = 0
            } else {
                next_index = selected_index + 1
            }
        }
        chr = data.chroms[next_index]
        \$("#region-select").val(chr)
        \$("#region-select").trigger("change")
    }

    \$("#btn-previous").click(function () {
        next_region(-1)
    })

    \$("#btn-next").click(function () {
        next_region()
    })

    \$("#download-csv").click(function () {
        dist_table.button('.buttons-csv').trigger()
    })

    \$("#download-copy").click(function () {
        dist_table.button('.buttons-copy').trigger()
    })

    \$(document).ready(function () {
        build_filters(data.n50, ["sample", "n50"])
    })

</script>

</html>
"""


out = "covdist.html"
txts = "$txts".split(" ")

# chrom / sample / {x:, y:, v50:}
coords = defaultdict(dict)
coords["v50"] = []
chroms = ["total"]

for f in txts:
    sample = os.path.basename(f).replace(".mosdepth.global.dist.txt", "")
    gen = (x.rstrip().split("\t") for x in open(f))
    for chrom, data in it.groupby(gen, itemgetter(0)):
        if not chrom == "total" and chrom not in chroms:
            chroms.append(chrom)

        xs, ys = [], []
        v50 = 0
        found = False
        for _, x, y in data:
            y = float(y)
            if y < 0.01:
                continue
            if not found and y > 0.5:
                v50 = float(x)
                found = True

            xs.append(float(x))
            ys.append(y)

        if len(xs) > 100:
            xs = [x for i, x in enumerate(xs) if ys[i] > 0.02]
            ys = [y for y in ys if y > 0.02]
            if len(xs) > 100:
                xs = xs[::2]
                ys = ys[::2]

        coords[chrom][sample] = dict(
            x=[round(x, 3) for x in xs],
            y=[round(y, 3) for y in ys],
            v50=round(v50, 2))
        if chrom == "total":
            coords["v50"].append(dict(sample=sample, v50=round(v50, 2)))

coords["chroms"] = chroms
with open(out, "w") as fh:
    data_json = json.dumps(coords).encode("utf-8", "ignore").decode("utf-8")
    data_json = data_json.replace("NaN", "null")
    template = TEMPLATE.replace("{{data}}", data_json)
    print(template, file=fh)
