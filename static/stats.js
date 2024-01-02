function stats(data,head,id){
    function updateTable(leftColumnContent, rightColumnContent) {
        var tableBody = document.getElementById(id).getElementsByTagName("tbody")[0];
  
        // Create a new row
        var newRow = tableBody.insertRow();
  
        // Insert cells into the row
        var leftCell = newRow.insertCell(0);
        var rightCell = newRow.insertCell(1);
  
        // Set content for the cells
        leftCell.style.width = "70%";
        leftCell.style.padding = "15px";
        leftCell.style.textAlign = "left";
        leftCell.style.borderBottom = "1px solid #ddd";
        leftCell.textContent = leftColumnContent;
  
        rightCell.style.padding = "15px";
        rightCell.style.textAlign = "center";
        rightCell.style.borderBottom = "1px solid #ddd";
        rightCell.textContent = rightColumnContent;
      }

      // Call the function to update the table with the data
      for (var i = 0; i < data.length; i++) {
        updateTable(head[i], data[i]);
      }

}