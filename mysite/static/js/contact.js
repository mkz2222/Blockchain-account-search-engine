$(document).ready(function() {

  $('form.ajax_contact').on('submit', function(data){

    $("#email_button").html('Sending...');
    var that =$(this),
    url = "/a2",
    type = that.attr('method'),
    data = {};
    
    that.find('[name]').each(function(index, value){
      var that =$(this),
      name = that.attr('name'),
      value = that.val();
      data[name] = value;
      data['type'] = 'contact';
    });

    $.ajax({
      url: url,
      type: type,
      data: data,
      dataType: "json",

      success: function(response){

        if(response.chg == '1'){
          $(".user_setting01").html('<div class="acct_setting01u"><p>Thank you for contacting us! We will get back to you shortly.</p></div>');
          
        }else{
          $("#contact_er").html(response.error);
          $("#email_button").html('Send');
        }
      }

    });

    return false;
  });
});