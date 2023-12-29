function languagepiechart(Data,id){
      google.charts.load("current", {packages:["corechart"]});
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable(Data);

        var options = {
          title: (id=== "submissionChart") ? 'Submissions Data' : 'Language Data',
          is3D: true,
        };

        var chart = new google.visualization.PieChart(document.getElementById(id));
        chart.draw(data, options);
      }
}