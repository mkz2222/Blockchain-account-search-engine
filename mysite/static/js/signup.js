

$("#id_uname").change(function () {
  var uname = $(this).val();
  $.ajax({
    url: '/ajax/check_username',
    data: {
      'uname': uname
    },
    dataType: 'json',
    success: function (data) {
      if (data.pass == 1) {
        $("#username_er").html('')
      }else {
        $("#username_er").html(data.error);
      } 
    }
  });
});


$("#id_email").change(function () {
  var email = $(this).val();
  $.ajax({
    url: '/ajax/check_email',
    data: {
      'email': email
    },
    dataType: 'json',
    success: function (data) {
      if (data.pass == 1) {
        $("#email_er").html('')
      }else {
        $("#email_er").html(data.error);
      } 
    }
  });
});




$(document).ready(function() {

  $('form.ajax_signup').on('submit', function(data){

    $("#signup_button").html('Updating...');
    var that =$(this),
    url = that.attr('action'),
    type = that.attr('method'),
    data = {};
    
    that.find('[name]').each(function(index, value){
      var that =$(this),
      name = that.attr('name'),
      value = that.val();
      data[name] = value;
    });

    $.ajax({
      url: url,
      type: type,
      data: data,
      dataType: "json",

      success: function(data){

        if(data.pass == '1'){
          $(".p02ar_1").html('<span>A validation email has been sent, please check your email and confirm.</span>').css("text-align", "center");
          
        }else{
          
          var list_html = "";

          for( var i=0; i <data.error.length; i++) {
             list_html += "<li>" + data.error[i] + "</li>";
           }

          $("#signup_er").html(list_html);
          $("#signup_button").html('Register');

          $("#id_pass1").val('');
          $("#id_pass2").val('');
          
        }
      }

    });

    return false;

  });

});




