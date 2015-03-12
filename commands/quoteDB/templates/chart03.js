$(function () {
    var dataSum = {{len}};

    $('#container03').highcharts({
        chart: {
            type: 'column'
        },
        exporting: {
            enabled: false
        },
        title: {
            text: 'Most active submitter'
        },
        xAxis: {
            type: 'category'
        },
        yAxis: {
            labels: {
                format: '{value}'
            },
            title: {
                text: ''
            },
            plotLines: [{
                zindex: 1,
                value: {{avg}},
                width: 1,
                color: '#cf715e',
                dashStyle: 'longdashdot',
                label: {
                    text: 'Average per Submitter',
                    align: 'right',
                    y: 12,
                    x: 0,
                    style: {
                        color: '#cf715e'
                    }
                }
            }]
        },
        legend: {
            enabled: false
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            series: {
                borderWidth: 2,
                borderColor: '#A2CE52',
                column: {
                    fillOpacity: 0.1,
                },
                dataLabels: {
                    enabled: true,
                    formatter:function() {
                    var pcnt = (this.y / dataSum) * 100;
                    return Highcharts.numberFormat(pcnt) + '%';
                }
                }
            }
        },

        tooltip: {
            
            headerFormat: '<span style="font-size:12px; color:#A2CE52">{point.key}</span><br>',
            pointFormat: '<span style="font-size:11px"><b>{point.y}</b> total Submissions</span><br/>'
        },

        series: [{
            name: 'Submitter',
            color: 'rgba(162, 206, 82, 0.1)',
            data: {{data|safe}}
        }]
    });
});