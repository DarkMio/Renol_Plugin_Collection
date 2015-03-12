$(function () {
    $('#container02').highcharts({
        chart: {
            type: 'areaspline'
        },
        exporting: {
            enabled: false,
        },
        title: {
            text: 'Quotes stored per hour'
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
                    text: 'Average Quotes per Hour',
                    align: 'right',
                    y: 12,
                    x: 0,
                    style: {
                        color: '#cf715e'
                    }
                }
            }]
        },
        xAxis: {
            categories: [
            ],
        },
        tooltip: {
            headerFormat: '',
            formatter: function() {
                var text = this.x+':00: <b>';
                if(this.y == 1) {
                    text = text + this.y + '</b> Quote'
                   } else {
                    text = text + this.y + '</b> Quotes'
                   }
                    return text;}
        },
        plotOptions: {
            areaspline: {
                fillOpacity: 0.1
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            showInLegend: false,
            data: {{data}}
        }]
    });
});