$(function() {
    var chart = new Highcharts.StockChart({
        chart: {
            renderTo: 'container01',
            type: 'areaspline'
        },
        exporting: {
            enabled: false,
        },
        title: {
            text: 'Quotes stored per day'
        },      
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: { // don't display the dummy year
                month: '%e. %b',
                year: '%b'
            },
            title: {
                text: ' '
            }
        },
        yAxis: {
            title: 'Quotes',
            min: 0,
            plotLines: [{
                value: {{avg}},
                width: 1,
                color: '#cf715e',
                dashStyle: 'longdashdot',
                label: {
                    text: 'Average Quotes per Day',
                    align: 'right',
                    y: 12,
                    x: 0,
                    style: {
                        color: '#cf715e'
                    }
                }
            }]
        },
        tooltip: {
            headerFormat: '',
            pointFormat: '{point.x:%e. %b}: {point.y:.0f}'
        },
        plotOptions: {
            areaspline: {
                fillOpacity: 0.1
            }
        },
        credits: {
            enabled: false
        },
         rangeSelector: {
            enabled: false
        },
        navigator: {
        enabled: true
    },
        series: [{
            dataGrouping: {
                approximation: "sum",
                enabled: true,
                forced: true,
                units: [['day', [1]], ['week',[1]]],
                groupPixelWidth: 100                
            },
            showInLegend: false,
            data: {{data}}
        }]
    });
});
        