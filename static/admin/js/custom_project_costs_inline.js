
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>

document.addEventListener('DOMContentLoaded', function () {


    $(document).on('formset:added', function(event, $row, formsetName) {
        console.log("haaaaaaaaaaaaaaaaaaaay")
        if (formsetName === 'expectedprojectcosts_set') {
            var all_select_elements = document.querySelectorAll('[id^="id_expectedprojectcosts_set-"][id*="-main_category_detail"]');
            var new_select_element = all_select_elements[all_select_elements.length - 1];
            var last_select_element = all_select_elements[all_select_elements.length - 2];
    
            for (var i = 0; i < last_select_element.options.length; i++) {
                if (last_select_element.options[i].selected) {
                    var new_option = document.createElement("option");
                    new_option.value = last_select_element.options[i].value;
                    new_option.text = last_select_element.options[i].text;
                    new_select_element.appendChild(new_option);
                    new_option.selected = true;
                }
            }
        }
    });



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
