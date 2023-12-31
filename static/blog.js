function excerpt() {
    var tableRows = document.querySelectorAll("#myTable tr");

    for (var i = 5; i < tableRows.length; i++) {
        tableRows[i].classList.toggle("hidden");
    }
}