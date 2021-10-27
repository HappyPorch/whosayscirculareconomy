
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
        for (let c in rawData.meta.cats) {
            let cat = rawData.meta.cats[c];
            $('#filterSummaryBy').append(`<option value="${cat}">where Category includes ${cat}</option>`);
        }


        $('.runSummaryFilter').change(function () {
            summaryDisplay(rawData);
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