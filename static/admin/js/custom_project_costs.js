document.addEventListener('DOMContentLoaded', function () {
    // Function to show/hide fields based on the value of 'who_paid' field
    function toggleFields() {
      var whoPaidValue = document.getElementById('id_who_paid').value;
      console.log(whoPaidValue)
  
      // Hide all fields initially
      var clientField = document.getElementsByClassName("field-client")[0];
      var engineersField = document.getElementsByClassName("field-engineers")[0];
      var workersField = document.getElementsByClassName("field-workers")[0];
  
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
        console.log(pay_reason_category)
    
        // Hide all fields initially
        var pay_category_detail = document.getElementsByClassName("field-pay_category_detail")[0];
        var market = document.getElementsByClassName("field-market")[0];
    
    
        pay_category_detail.style.display = 'none';
        market.style.display = 'none';

    
        // Show/hide fields based on 'who_paid' value
        if (pay_reason_category === 'a') {
          pay_category_detail.style.display = 'block';
        } else if (pay_reason_category === 'b') {
          market.style.display = 'block';
        } 
      }

  
    // Call the functions initially
    toggleFields();
    togglePayCategoryFields();
  
    // Attach event listeners to the fields
    document.getElementById('id_who_paid').addEventListener('change', toggleFields);
    document.getElementById('id_pay_reason_category').addEventListener('change', togglePayCategoryFields);
  });