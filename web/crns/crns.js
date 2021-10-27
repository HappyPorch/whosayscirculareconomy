
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
        
    });

}

function summaryDisplay(d) {

    $('#searchDateDisplay').html(rawData.meta.search_date)
    $('#originalCountDisplay').html(rawData.meta.source_count)
    
    var d = rawData.data;

    $('#countDisplay_total').html(d.length)
    termFoundCount = filter_found(d).length;
    $('#countDisplay_termfound').html(termFoundCount)
    $('#countDisplay_termfound_percent').html(asPercent(termFoundCount, d.length))
    $('#countDisplay_termnotfound').html(d.length-termFoundCount)
    $('#countDisplay_termnotfound_percent').html(asPercent(d.length-termFoundCount, d.length))
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