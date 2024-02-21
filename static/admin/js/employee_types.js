document.addEventListener('DOMContentLoaded', function() {
    var typeSelect = document.getElementById('id_type');
    var categorySelect = document.getElementById('id_category');

    typeSelect.addEventListener('change', function() {
        var type = this.value;
        // var categoryType = type == 'E' ? 'E' : 'T';
        var categoryType = 'G'
        if (type == "E"){
            categoryType = 'E'
        }
        if (type == "W"){
            categoryType = 'T'
        }

        fetch('/get_categories/?category_type=' + categoryType)
            .then(response => response.json())
            .then(data => {
                // Clear the category select menu
                while (categorySelect.firstChild) {
                    categorySelect.removeChild(categorySelect.firstChild);
                }

                // Add the new options to the category select menu
                data.forEach(function(item) {
                    var option = document.createElement('option');
                    option.value = item.id;
                    option.text = item.category;
                    categorySelect.appendChild(option);
                });
            });
    });
});
