
$(document).ready(function() {

  $('form.ajax_email').on('submit', function(data){

    $("#email_button").html('Updating...');
    var that =$(this),
    url = "/ajax/change_email",
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

      success: function(response){

        if(response.chg == '1'){
          $(".user_setting01").html('<div class="acct_setting01u"><p>A validation email has been sent, please check your email.</p></div>');
          
        }else if(response.login == '0'){

          window.location.replace("/login/") 

        }else{
          $("#email_chg").html(response.error);
          $("#email_button").html('Update');
        }
      }

    });

    return false;

  });

});





$(document).ready(function() {

  $('form.ajax_password').on('submit', function(data){

    $("#pass_button").html('Updating...');
    var that =$(this),
    url = "/ajax/change_password",
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

      success: function(response){

        if(response.chg == '1'){
          $(".user_setting02").html('Your password has been updated.').addClass("p11suc");
          $("#pass_button").html('Update');
          
        }else if(response.login == '0'){

          window.location.replace("/login/") 

        }else{

          var list_html = "";
          for( var i=0; i <response.error.length; i++) {
             list_html += "<li>" + response.error[i] + "</li>";
           }
          // list_html += "</li>"

          $("#pass_chg").html(list_html);
                
          // $("#pass_chg").html(response.error);
          
          $("#pass_button").html('Update');
        }
      }

    });

    return false;

  });

});