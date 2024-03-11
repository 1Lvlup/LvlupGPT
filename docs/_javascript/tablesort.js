// Subscribes to the document$ observable stream
document$.subscribe(function () {
    // Selects all <table> elements within <article> elements that do not have a defined class attribute
    var tables = document.querySelectorAll("article table:not([class])");

    // Iterates over the selected <table> elements using the forEach method
    tables.forEach(function (table) {
        // For each <table> element, a new instance of the Tablesort class is created and initialized with the current <table> element as its argument
        new Tablesort(table);
    });
});
