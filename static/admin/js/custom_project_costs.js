document.addEventListener('DOMContentLoaded', function() {
  // Function to show/hide fields based on the value of 'who_paid' field
  function toggleFields() {
    var whoPaidValue = document.getElementById('id_who_paid').value;
    var clientField = document.querySelector(".field-client");
    var engineersField = document.querySelector(".field-engineers");
    var workersField = document.querySelector(".field-workers");
    // Hide all fields initially
    clientField.style.display = 'none';
    engineersField.style.display = 'none';
    workersField.style.display = 'none';

    // Show/hide fields based on 'who_paid' value
    if (whoPaidValue === 'c') {
      clientField.style.display = 'block';
    } else if (whoPaidValue === 'e') {
      engineersField.style.display = 'block';
    } else if (whoPaidValue === 'w') {
      workersField.style.display = 'block';
    }
  }



  // Function to show/hide fields based on the value of 'pay_reason_category' field
  function togglePayCategoryFields() {
    var pay_reason_category = document.getElementById('id_pay_reason_category').value;
    var main_category_detail = document.querySelector(".field-main_category_detail");
    var sub_category_detail = document.querySelector(".field-sub_category_detail");
    var for_witch_worker = document.querySelector(".field-for_witch_worker");
    var market = document.querySelector(".field-market");

    // Hide all fields initially
    main_category_detail.style.display = 'none';
    sub_category_detail.style.display = 'none';
    for_witch_worker.style.display = 'none';
    market.style.display = 'none';

    // Show/hide fields based on 'pay_reason_category' value
    if (pay_reason_category === 'a') {
      main_category_detail.style.display = 'block';
      sub_category_detail.style.display = 'block';
      for_witch_worker.style.display = 'block';
    } else if (pay_reason_category === 'b') {
      market.style.display = 'block';
    }
  }

  var id_main_category_detail = document.getElementById('id_main_category_detail');
  var id_sub_category_detail = document.getElementById('id_sub_category_detail');
  var id_for_witch_worker = document.getElementById('id_for_witch_worker');
  id_main_category_detail.addEventListener('change', function() {
      var type = this.value;
      
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
          
      
  });




  // Call the functions initially
  toggleFields();
  togglePayCategoryFields();

  // Attach event listeners to the fields
  document.getElementById('id_who_paid').addEventListener('change', toggleFields);
  document.getElementById('id_pay_reason_category').addEventListener('change', togglePayCategoryFields);

});