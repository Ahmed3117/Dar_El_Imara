

document.addEventListener('DOMContentLoaded', function () {
  // Function to show/hide fields based on the value of 'who_paid' field
  console.log("kkkkkkkkkkkkk")
  function toggleFields(event) {
    var rowId = event.target.id.split('-')[1];
    
    var whoPaidValue = document.getElementById('id_projectcosts_set-' + rowId + '-who_paid').value;

    // Hide all fields initially
    var added_rowId = parseInt(rowId) + 1;
    var clientField = document.getElementsByClassName("field-client")[added_rowId];
    var engineersField = document.getElementsByClassName("field-engineers")[parseInt(rowId)];
    var workersField = document.getElementsByClassName("field-workers")[parseInt(rowId)];

    var clientcolumn = document.getElementsByClassName("column-client")[0];
    var engineerscolumn = document.getElementsByClassName("column-engineers")[0];
    var workerscolumn = document.getElementsByClassName("column-workers")[0];

    clientField.style.display = 'none';
    engineersField.style.display = 'none';
    workersField.style.display = 'none';

    clientcolumn.style.display = 'none';
    engineerscolumn.style.display = 'none';
    workerscolumn.style.display = 'none';

    // Show/hide fields based on 'who_paid' value
    if (whoPaidValue === 'c') {
      clientField.style.display = 'block';
      clientcolumn.style.display = 'block';
    } else if (whoPaidValue === 'e') {
      engineersField.style.display = 'block';
      engineerscolumn.style.display = 'block';
    } else if (whoPaidValue === 'w') {
      workersField.style.display = 'block';
      workerscolumn.style.display = 'block';
    }
  }

  // Function to show/hide fields based on the value of 'pay_reason_category' field
  function togglePayCategoryFields(event) {
    var rowId = event.target.id.split('-')[1];
    console.log(rowId)
    var pay_reason_category = document.getElementById('id_projectcosts_set-' + rowId + '-pay_reason_category').value;
    console.log(pay_reason_category)
    // Hide all fields initially
    var main_category_detail = document.getElementsByClassName("field-main_category_detail" )[parseInt(rowId)];
    var sub_category_detail = document.getElementsByClassName("field-sub_category_detail" )[parseInt(rowId)];
    var market = document.getElementsByClassName("field-market" )[parseInt(rowId)];

    var column_main_category_detail = document.getElementsByClassName("column-main_category_detail" )[0];
    var column_sub_category_detail = document.getElementsByClassName("column-sub_category_detail" )[0];
    var column_market = document.getElementsByClassName("column-market" )[0];

    main_category_detail.style.display = 'none';
    sub_category_detail.style.display = 'none';
    market.style.display = 'none';

    column_main_category_detail.style.display = 'none';
    column_sub_category_detail.style.display = 'none';
    column_market.style.display = 'none';

    // Show/hide fields based on 'pay_reason_category' value
    if (pay_reason_category === 'a') {
      main_category_detail.style.display = 'block';
      sub_category_detail.style.display = 'block';
      column_main_category_detail.style.display = 'block';
      column_sub_category_detail.style.display = 'block';
    } else if (pay_reason_category === 'b') {
      market.style.display = 'block';
      column_market.style.display = 'block';
    }
  }
  // Function to show/hide fields based on the value of 'pay_reason_category' field
  function showCategoryWorkers(event) {
    var rowId = event.target.id.split('-')[1];
      var type = this.value;
      var id_for_witch_worker = document.getElementById('id_projectcosts_set-' + rowId +'-for_witch_worker');
      var id_sub_category_detail = document.getElementById('id_projectcosts_set-' + rowId +'-sub_category_detail');
      fetch('/get_category_workers/?category=' + type)
          .then(response => response.json())
          .then(data => {
              // Clear the category select menu
              while (id_for_witch_worker.firstChild) {
                  id_for_witch_worker.removeChild(id_for_witch_worker.firstChild);
              }
              // Add the new options to the category select menu
              data.forEach(function(item) {
                  var option = document.createElement('option');
                  option.value = item.id;
                  option.text = item.name;
                  id_for_witch_worker.appendChild(option);
              });
          });
          fetch('/get_category_subs/?category=' + type)
          .then(response => response.json())
          .then(data => {
              // Clear the category select menu
              while (id_sub_category_detail.firstChild) {
                  id_sub_category_detail.removeChild(id_sub_category_detail.firstChild);
              }
              // Add the new options to the category select menu
              data.forEach(function(item) {
                  var option = document.createElement('option');
                  option.value = item.id;
                  option.text = item.sub_category;
                  id_sub_category_detail.appendChild(option);
              });
          });
  }
// Attach event listener to a common parent element using event delegation
document.body.addEventListener('change', function (event) {
  var targetId = event.target.id;
  console.log(targetId)
  if (targetId && targetId.includes('-main_category_detail')) {
      showCategoryWorkers.call(event.target, event);
      togglePayCategoryFields.call(event.target, event);
      toggleFields.call(event.target, event);
  }
});
document.body.addEventListener('change', function (event) {
  var targetId = event.target.id;
  if (targetId && targetId.includes('-who_paid')) {
    toggleFields.call(event.target, event);
  }
  if (targetId && targetId.includes('-pay_reason_category')) {
    togglePayCategoryFields.call(event.target, event);
  }
  if (targetId && targetId.includes('-main_category_detail')) {
    showCategoryWorkers.call(event.target, event);
  }
});

// Attach event listener to a common parent element (e.g., the form)
document.getElementById('project_form').addEventListener('change', function (event) {
  var targetId = event.target.id;
  // Check if the event target is a relevant element, and then call the appropriate function
  if (targetId && targetId.includes('-who_paid')) {
      toggleFields.call(event.target, event);
  } else if (targetId && targetId.includes('-pay_reason_category')) {
      togglePayCategoryFields.call(event.target, event);
  } else if (targetId && targetId.includes('-main_category_detail')) {
      showCategoryWorkers.call(event.target, event);
  }
});

  // Get all the rows in the inline formset
  var rows = document.querySelectorAll('.inline-group [id^="id_projectcosts_set-"][id$="-who_paid"]');
  // Attach event listeners to each row
  rows.forEach(function (row) {
    var rowId = row.id.split('-')[1];
    var ele1 = document.getElementById('id_projectcosts_set-' + rowId + '-who_paid');
    var ele2 = document.getElementById('id_projectcosts_set-' + rowId + '-pay_reason_category');
    var ele3 = document.getElementById('id_projectcosts_set-' + rowId +'-main_category_detail');
    ele1.addEventListener('change', toggleFields);
    ele2.addEventListener('change', togglePayCategoryFields);
    ele3.addEventListener('change', showCategoryWorkers);

    // Call the functions initially for each row
    toggleFields.call(row, { target: row });
    togglePayCategoryFields.call(row, { target: row });
    showCategoryWorkers.call(row, { target: row });
  });
});


  // Attach event listener to a common parent element using event delegation
document.body.addEventListener('change', function (event) {
  var targetId = event.target.id;
  if (targetId && targetId.includes('-who_paid')) {
    toggleFields.call(event.target, event);
  }
  if (targetId && targetId.includes('-pay_reason_category')) {
    togglePayCategoryFields.call(event.target, event);
  }
  if (targetId && targetId.includes('-main_category_detail')) {
    showCategoryWorkers.call(event.target, event);
  }
});

// Attach event listener to a common parent element (e.g., the form)
document.getElementById('project_form').addEventListener('change', function (event) {
  var targetId = event.target.id;
  // Check if the event target is a relevant element, and then call the appropriate function
  if (targetId && targetId.includes('-who_paid')) {
      toggleFields.call(event.target, event);
  } else if (targetId && targetId.includes('-pay_reason_category')) {
      togglePayCategoryFields.call(event.target, event);
  } else if (targetId && targetId.includes('-main_category_detail')) {
      showCategoryWorkers.call(event.target, event);
  }
});






///////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////


document.addEventListener('DOMContentLoaded', function () {
  console.log("kkkkkkkkkkkkk");

  // Function to show/hide fields based on the value of 'pay_reason_category' field
  function showCategoryWorkers(event) {
      console.log('llllllllllll');

      var rowId = event.target.id.split('-')[1];
      var type = this.value;

      if (type) {
          var id_sub_category_detail = document.getElementById('id_expectedprojectcosts_set-' + rowId + '-sub_category_detail');

          fetch('/get_category_subs/?category=' + type)
              .then(response => response.json())
              .then(data => {
                  // Clear the category select menu
                  id_sub_category_detail.innerHTML = '';

                  // Add the new options to the category select menu
                  data.forEach(function (item) {
                      var option = document.createElement('option');
                      option.value = item.id;
                      option.text = item.sub_category;
                      id_sub_category_detail.appendChild(option);
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
                  // Clear the category select menu
                  id_sub_category_detail.innerHTML = '';

                  // Add the new options to the category select menu
                  data.forEach(function (item) {
                      var option = document.createElement('option');
                      option.value = item.id;
                      option.text = item.sub_category;
                      id_sub_category_detail.appendChild(option);
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
