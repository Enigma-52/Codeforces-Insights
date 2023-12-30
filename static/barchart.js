function ratingbarchart(rating_data, id){
    const headers = rating_data[0];
  const rows = rating_data.slice(1);

  // Extracting the Rating and Count lists
  const ratingList = rows.map(row => row[0]);
  const countList = rows.map(row => row[1]);

  var data = [
    {
      x: ratingList,
      y: countList,
      type: 'bar'
    }
  ];
  
  Plotly.newPlot(id, data);
  
}