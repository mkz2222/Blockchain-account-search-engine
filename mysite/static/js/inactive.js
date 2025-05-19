$(document).ready(function() {

  $('#resend_link').on('click', function(data){

    $(".p02ar_1").html('Sending...');
    var that =$(this),
    data = {
      csrfmiddlewaretoken: '{{ csrf_token }}',
      username: '{{ user }}',
    };
    

    $.ajax({
      url: "/a3",
      type: 'post',
      data: data,
      dataType: "json",

      success: function(response){

        if(response.chg == '1'){
          $(".p02ar_1").html('<p>The activation email has been sent.</p>').addClass("p11suc");
          
        }else{

          $(".p02ar_1").html(response.error);
          
        }
      }

    });

    return false;

  });

});