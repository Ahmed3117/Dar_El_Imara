document.addEventListener('DOMContentLoaded', function () {
    function showCategoryWorkers(event) {
        var rowId = event.target.id.split('-')[1];
        var type = this.value;
        if (type) {
            var id_sub_category_detail = document.getElementById('id_expectedprojectcosts_set-' + rowId + '-sub_category_detail');
            fetch('/get_category_subs/?category=' + type)
                .then(response => response.json())
                .then(data => {
                    var initialValue = document.getElementById('id_expectedprojectcosts_set-' + rowId + '-sub_category_detail').value;

                    // Clear the category select menu
                    id_sub_category_detail.innerHTML = '';

                    // Add the new options to the category select menu
                    data.forEach(function (item) {
                        var option = document.createElement('option');
                        option.value = item.id;
                        option.text = item.sub_category;
                        id_sub_category_detail.appendChild(option);
                        id_sub_category_detail.value = initialValue;
                    });
                });
        }
    }

    // Attach event listener to a common parent element using event delegation
    document.body.addEventListener('change', function (event) {
        var targetId = event.target.id;

        if (targetId && targetId.includes('-main_category_detail')) {
            showCategoryWorkers.call(event.target, event);
        }
    });

    // Trigger the event for existing elements
    var selectElements = document.querySelectorAll('[id*="id_expectedprojectcosts_set-"][id*="-main_category_detail"]');
    selectElements.forEach(function (ele) {
        showCategoryWorkers.call(ele, { target: ele });
    });

    function showSubCategories(event) {
        console.log('llllllllllll');

        var rowId = event.target.id.split('-')[1];
        var type = this.value;

        if (type) {
            var id_sub_category_detail = document.getElementById('id_projectkhamatcosts_set-' + rowId + '-sub_category_detail');

            fetch('/get_category_subs/?category=' + type)
                .then(response => response.json())
                .then(data => {
                    var initialValue = document.getElementById('id_projectkhamatcosts_set-' + rowId + '-sub_category_detail').value;
                    // Clear the category select menu
                    id_sub_category_detail.innerHTML = '';

                    // Add the new options to the category select menu
                    data.forEach(function (item) {
                        var option = document.createElement('option');
                        option.value = item.id;
                        option.text = item.sub_category;
                        id_sub_category_detail.appendChild(option);
                        id_sub_category_detail.value = initialValue;
                    });
                });
        }
    }

    // Attach event listener to a common parent element using event delegation
    document.body.addEventListener('change', function (event) {
        var targetId = event.target.id;

        if (targetId && targetId.includes('-main_category_detail')) {
            showSubCategories.call(event.target, event);
        }
    });

    // Trigger the event for existing elements
    var selectElements = document.querySelectorAll('[id*="id_projectkhamatcosts_set-"][id*="-main_category_detail"]');
    selectElements.forEach(function (ele) {
        showSubCategories.call(ele, { target: ele });
    });
});
