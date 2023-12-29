function prediction(allRatingsList, actualLength, num_predictions) {
    function generateArray(start, end) {
        return Array.from({
            length: end - start + 1
        }, (_, i) => start + i);
    }

    var ctx = document.getElementById('ratingChart').getContext('2d');
    var actualRatings = allRatingsList.slice(0, actualLength);
    var predictedRatings = allRatingsList.slice(actualLength);

    // Define colors for actual and predicted ratings
    var actualColor = 'blue';
    var predictedColor = 'red';

    // Create the data object for the chart
    var contestNumbers = Array.from({
        length: actualLength
    }, (_, i) => i + 1);
    var predictedContestNumbers = Array.from({
        length: num_predictions
    }, (_, i) => actualLength + i + 1);

    var chartData = {
        labels: [...contestNumbers, ...predictedContestNumbers],
        datasets: [{
                label: 'Actual Ratings',
                data: actualRatings,
                borderColor: actualColor,
                backgroundColor: actualColor,
                fill: false,
            },
            {
                label: 'Predicted Ratings',
                data: [...actualRatings, ...predictedRatings],
                borderColor: predictedColor,
                backgroundColor: predictedColor,
                fill: false,
            },
        ],
    };



    // Create the chart
    var ratingChart = new Chart(ctx, {
        type: 'line',
        data: chartData,
    });
}