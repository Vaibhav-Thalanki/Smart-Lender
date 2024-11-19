$(document).ready(function() {
  $('#loanForm').on('submit', function(e) {
      let valid = true;
      $('input[required], select[required]').each(function() {
          if ($(this).val() === '') {
              valid = false;
              $(this).css('border', '1px solid red');
          } else {
              $(this).css('border', '1px solid #ccc');
          }
      });
      if (!valid) {
          e.preventDefault();
          alert('Please fill in all required fields.');
      }
  });

  if (
    document.querySelector("div#result>b").textContent ==
    "Prediction: rejected"
  ) {
    document.querySelector("div#pic>img").src = "./static/images/reject.png";
  } else {
    document.querySelector("div#pic>img").src = "./static/images/accept.png";
  }
});