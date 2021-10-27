
let rawData = {};

$(function(){
    setUp();
    $('#dataSet').change(function () {
        setUp();
    });
});

function setUp() {

    var datafile = $("#dataSet").val()
    $.getJSON( datafile, function( d ) {

        rawData = d;
        summaryDisplay(rawData);
        ungroupedDisplay(d.data);
        enableSort();
        
        });

        $('.runFilter').change(function () {
        filteredDisplay();
    });
    $('.runSummaryFilter').change(function () {
        summaryDisplay(rawData);
    });

}

var chart;
function showChart(d) {
    cols = d.filter(x => x.count_found > 0).map(function (x) { return [x.group, x.count_found]})
    chart = c3.generate({
        bindto: '#pieChart',
        data: {
            columns: cols,
            type : 'pie',
            onclick: function (d, i) { console.log("onclick", d, i); },
            onmouseover: function (d, i) { console.log("onmouseover", d, i); },
            onmouseout: function (d, i) { console.log("onmouseout", d, i); }
        }
    });
}
function hideChart() {
    if (chart)
        chart = chart.destroy();
}

function summaryDisplay(rawData) {
    $('#searchDateDisplay').html(rawData.meta.search_date)
    $('#originalCountDisplay').html(rawData.meta.source_count)
    
    var d = rawData.data;
    var filter = $('#filterSummaryBy').val();
    if (filter) {
        d = filter_bypurpose(d, filter);
    }
    $('#countDisplay_total').html(d.length)
    termFoundCount = filter_found(d).length;
    $('#countDisplay_termfound').html(termFoundCount)
    $('#countDisplay_termfound_percent').html(asPercent(termFoundCount, d.length))
    $('#countDisplay_termnotfound').html(d.length-termFoundCount)
    $('#countDisplay_termnotfound_percent').html(asPercent(d.length-termFoundCount, d.length))
}
function asPercent(num, total){
    return ((num/total)*100).toFixed(2);
}
var tableSort;
function enableSort() {
    
}

function clearTable() {
    $('#resultsTable tbody').html("");
}
function showHead(g) {
    heads = (g == "group") ?
        {"col1": "Group", "col2": "Sites with", "col3": "Sites without", "col4": "Total"} :
        {"col1": "Domain", "col2": "Search Count", "col3": "", "col4": ""};

    $('#col1_head').text(heads.col1);
    $('#col2_head').text(heads.col2);
    $('#col3_head').text(heads.col3);
    $('#col4_head').text(heads.col4);

}

function filter_bypurpose(d, purpose) {
    return d.filter(function (x) {return x.charity_purposes.includes(purpose)});
}
function filter_found(d, mincount) {
    if (mincount) {
        return d.filter(function (x) { return x.search_term_found == 1 && x.results_count >= mincount});
    }
    return d.filter(function (x) { return x.search_term_found >= 1});
}
function filter_notfound(d) {
    if (mincount) {
        return d.filter(function (x) { return x.search_term_found == 0});
    }
    return d.filter(function (x) { return x.search_term_found == 0});
}

function ungroupedDisplay(d) {

    hideChart();

    d.sort( function( a, b ) { return b.results_count - a.results_count; } )

    //clearTable();
    showHead()
    
    let template = {'html':$('#rowTemplate').html()};
    $('#resultsTable tbody').json2html(d,template);

}

function filteredDisplay() {

    var groupByField = $('#filterGroup').val();
    var filterByCount = $('#filterByCount').val();

    results = rawData.data;
    var filter2 = $('#filterByPurpose').val();
    if (filter2) {
        results = filter_bypurpose(results, filter2);
    }

    clearTable();
    if (groupByField) {
        groupedResults = [];
        group = _.groupBy(results,groupByField);
        _.each(group, function(v,k,l) {
            var f = filter_found(v, filterByCount).length;
            var c = v.length;
            groupedResults.push({
                "group": k,
                "count_found": f,
                "percent_found": asPercent(f, c),
                "count_notfound": c-f,
                "percent_notfound": asPercent(c-f, c),
                "total": c
            });
        });
        groupedResults.sort( function( a, b ) { return b.group - a.group; } )
        
        //render
        showHead("group");
        let rowTemplate = {'html':$('#rowTemplate_Group').html()};
        $('#resultsTable tbody').json2html(groupedResults, rowTemplate);
        showChart(groupedResults);
    } else {
        ungroupedDisplay(filter_found(results, filterByCount));
    }
}
