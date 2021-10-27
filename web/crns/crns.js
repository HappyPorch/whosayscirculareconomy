
let rawData = {};

$(function(){
    setUp();
    $('#dataSet').change(function () {
        setUp();
    });
});


function setUp() {

    var datafile = "CE_Search_CRNS_20211027.json";
    $.getJSON( datafile, function( d ) {

        rawData = d;
        summaryDisplay(rawData);
        ungroupedDisplay(d.data);
        for (let c in rawData.meta.cats) {
            let cat = rawData.meta.cats[c];
            let opt = `<option value="${cat}">where Category includes ${cat}</option>`;
            $('#filterSummaryBy').append(opt);
            $('#filterByCategory').append(opt);
        }


        $('.runSummaryFilter').change(function () {
            summaryDisplay(rawData);
        });

        $('.runFilter').change(function () {
            filteredDisplay();
        });
        
    });

}

function summaryDisplay(rawData) {

    $('#searchDateDisplay').html(rawData.meta.search_date)
    $('#originalCountDisplay').html(rawData.meta.source_count)
    
    var d = rawData.data;
    var filter = $('#filterSummaryBy').val();
    if (filter) {
        d = filter_bycat(d, filter);
    }

    $('#countDisplay_total').html(d.length)
    termFoundCount = filter_found(d).length;
    $('#countDisplay_termfound').html(termFoundCount)
    $('#countDisplay_termfound_percent').html(asPercent(termFoundCount, d.length))
    $('#countDisplay_termnotfound').html(d.length-termFoundCount)
    $('#countDisplay_termnotfound_percent').html(asPercent(d.length-termFoundCount, d.length))

}


function filteredDisplay() {

    var groupByField = $('#filterGroup').val();
    var filterByCount = $('#filterByCount').val();

    results = rawData.data;
    var filter2 = $('#filterByCategory').val();
    if (filter2) {
        results = filter_bycat(results, filter2);
    }

    clearTable();
    if (groupByField == "location") {
        groupedResults = [];
        group = _.groupBy(results,function (r) {
            var loc = r["org"]["location"]["postal_code_info"]
            return loc ? loc["admin_district"] : "unknown";
        });
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
        //showChart(groupedResults);
    } else {
        ungroupedDisplay(filter_found(results, filterByCount));
    }
}
function ungroupedDisplay(d) {

    //hideChart();

    d.sort( function( a, b ) { return b.summary.results_count - a.summary.results_count; } )

    //clearTable();
    showHead()
    
    let template = {'html':$('#rowTemplate').html()};
    $('#resultsTable tbody').json2html(d,template);

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


function filter_bycat(d, cat) {
    return d.filter(function (x) {return x.org.categories.includes(cat)});
}
function filter_found(d, mincount) {
    if (mincount) {
        return d.filter(function (x) { return x.summary.search_term_found == 1 && x.summary.results_count >= mincount});
    }
    return d.filter(function (x) { return x.summary.search_term_found >= 1});
}
function filter_notfound(d) {
    if (mincount) {
        return d.filter(function (x) { return x.summary.search_term_found == 0});
    }
    return d.filter(function (x) { return x.summary.search_term_found == 0});
}

function getCategories(d) {
 var cats = d.data.map(item => item.age)
        filter((value, index, self) => self.indexOf(value) === index)
}