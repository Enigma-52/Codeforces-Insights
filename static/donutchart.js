function tagdonutchart(tagdata,id){
    google.charts.load("current", {packages:["corechart"]});
        google.charts.setOnLoadCallback(drawChart);

        function drawChart() {
            var data = google.visualization.arrayToDataTable([['Tag', 'Count']].concat(tagdata));

            var options = {
                pieHole: 0.4,
                legend: {
                    position: 'labeled',
                    labeledValueText: 'both',
                    textStyle: {
                        fontSize: 14
                    }
                }
            };

            var chart = new google.visualization.PieChart(document.getElementById(id));
            chart.draw(data, options);
        }
}