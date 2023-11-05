document.addEventListener('DOMContentLoaded', function () {
    // Function to show/hide fields based on the value of 'who_paid' field
    function toggleFields(event) {
      var rowId = event.target.id.split('-')[1];
      
      var whoPaidValue = document.getElementById('id_projectcosts_set-' + rowId + '-who_paid').value;

      // Hide all fields initially
      var added_rowId = parseInt(rowId) + 1;
      console.log('mmmmmmmmmmmmmmmmmmmmmmmmmm')
      console.log(rowId)
      console.log(added_rowId)
      console.log('mmmmmmmmmmmmmmmmmmmmmmmmmm')
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
      var pay_category_detail = document.getElementsByClassName("field-pay_category_detail" )[parseInt(rowId)];
      var market = document.getElementsByClassName("field-market" )[parseInt(rowId)];
  
      var column_pay_category_detail = document.getElementsByClassName("column-pay_category_detail" )[0];
      var column_market = document.getElementsByClassName("column-market" )[0];
  
      pay_category_detail.style.display = 'none';
      market.style.display = 'none';
  
      column_pay_category_detail.style.display = 'none';
      column_market.style.display = 'none';
  
      // Show/hide fields based on 'pay_reason_category' value
      if (pay_reason_category === 'a') {
        pay_category_detail.style.display = 'block';
        column_pay_category_detail.style.display = 'block';
      } else if (pay_reason_category === 'b') {
        market.style.display = 'block';
        column_market.style.display = 'block';
      }
    }
  
    // Get all the rows in the inline formset
    var rows = document.querySelectorAll('[id^="id_projectcosts_set-"][id$="-who_paid"]');
  
    // Attach event listeners to each row
    rows.forEach(function (row) {
      var rowId = row.id.split('-')[1];
      console.log("lllllllllllllllllllllllllllll")
      console.log(rowId)
      var ele1 = document.getElementById('id_projectcosts_set-' + rowId + '-who_paid');
      var ele2 = document.getElementById('id_projectcosts_set-' + rowId + '-pay_reason_category');
      console.log(ele1)
      console.log(ele2)
      ele1.addEventListener('change', toggleFields);
      ele2.addEventListener('change', togglePayCategoryFields);
  
      // Call the functions initially for each row
      toggleFields({ target: row });
      togglePayCategoryFields({ target: row });
    });
  });