function heatmap(submissions,id){
    google.charts.load('current', {'packages':['calendar']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn({ type: 'date', id: 'Date' });
        data.addColumn({ type: 'number', id: 'Submissions' });

        var rows = [];

        for (var date in submissions) {
            rows.push([new Date(date), submissions[date]]);
        }

        data.addRows(rows);

        // Calculate dynamic height based on the number of years and specified rowHeight
        var rowHeight = 152;  // Adjust this value based on the desired row height
        var uniqueYears = [...new Set(rows.map(row => row[0].getFullYear()))];  // Get unique years
        var dynamicHeight = uniqueYears.length * rowHeight;

        var chart = new google.visualization.Calendar(document.getElementById(id));

        var options = {
            height: dynamicHeight,
            outerWidth: 100,
            colorAxis: { minValue: 0, maxValue: 5, colors: ['#FFFFFF', '#4b96dd'] }  // Use light green color,
        };

        chart.draw(data, options);

        // Add an input area to set the max submissions
        var maxSubmissionsInput = document.getElementById('maxSubmissions');
        var submitButton = document.getElementById('submitMaxSubmissions');

        submitButton.addEventListener('click', function() {
            var maxSubmissionsValue = parseInt(maxSubmissionsInput.value);

            // Check if the entered value is a valid number
            if (!isNaN(maxSubmissionsValue)) {
                // Redraw the chart with the new max submissions value
                options.colorAxis.maxValue = maxSubmissionsValue;
                chart.draw(data, options);

                // Update the dynamic height based on the number of years and specified rowHeight
                dynamicHeight = uniqueYears.length * rowHeight;
                chart.getContainer().style.height = dynamicHeight + 'px';
            } else {
                alert('Please enter a valid number for max submissions.');
            }
        });
    }
}